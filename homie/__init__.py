import gc
import sys
import utime
from ucollections import namedtuple
from umqtt.simple import MQTTClient

from homie import utils

__version__ = b'0.1.2'


RETRY_DELAY = 10


Property = namedtuple('Property', (
    'topic',
    'payload',
    'retain',
))


class HomieDevice:

    """ MicroPython implementation of the homie v2 convention. """

    def __init__(self, settings):
        self.errors = 0
        self.settings = settings

        self.nodes = []
        self.node_ids = []
        self.topic_callbacks = {}

        self.start_time = utime.time()
        self.next_update = utime.time()
        self.stats_interval = self.settings.DEVICE_STATS_INTERVAL

        # base topic
        self.topic = b'/'.join((self.settings.MQTT_BASE_TOPIC,
                                self.settings.DEVICE_ID))

        # setup wifi
        utils.setup_network()
        utils.wifi_connect()

        try:
            self._umqtt_connect()
        except Exception:
            print('ERROR: can not connect to MQTT')
            # self.mqtt.publish = lambda topic, payload, retain, qos: None

    def _umqtt_connect(self):
        # mqtt client
        self.mqtt = MQTTClient(
            self.settings.DEVICE_ID,
            self.settings.MQTT_BROKER,
            port=self.settings.MQTT_PORT,
            user=self.settings.MQTT_USERNAME,
            password=self.settings.MQTT_PASSWORD,
            keepalive=self.settings.MQTT_KEEPALIVE,
            ssl=self.settings.MQTT_SSL,
            ssl_params=self.settings.MQTT_SSL_PARAMS)

        self.mqtt.DEBUG = True

        # set callback
        self.mqtt.set_callback(self.sub_cb)

        # set last will testament
        self.mqtt.set_last_will(self.topic + b'/$state', b'lost',
                                retain=True, qos=1)

        self.mqtt.connect()

        # The first message
        self.publish(b'state', b'init')

        # subscribe to device topics
        self.mqtt.subscribe(self.topic + b'/$stats/interval/set')
        self.mqtt.subscribe(self.topic + b'/$broadcast/#')

    def disconnect(self):
        """call this method if before disconnect the device"""
        self.publish(b'state', b'disconnected')

    def deepsleep(self, timeout):
        """call this method if before device deepsleep"""
        self.publish(b'state', b'sleeping')

    def add_node(self, node):
        """add a node class of HomieNode to this device"""
        self.nodes.append(node)

        # add node_ids
        try:
            self.node_ids.extend(node.get_node_properties())
        except NotImplementedError:
            raise
        except Exception:
            print('ERROR: getting Node')

        # subscribe node topics
        for topic in node.subscribe:
            topic = b'/'.join((self.topic, topic))
            self.mqtt.subscribe(topic)
            self.topic_callbacks[topic] = node.callback

    def sub_cb(self, topic, message):
        # device callbacks
        print('MQTT SUBSCRIBE: {} --> {}'.format(topic, message))

        if b'$stats/interval/set' in topic:
            self.stats_interval = int(message.decode())
            self.publish(b'$stats/interval', self.stats_interval)
            self.next_update = utime.time() + self.stats_interval
        elif b'$broadcast/#' in topic:
            for node in self.nodes:
                node.broadcast(topic, message)
        else:
            # node property callbacks
            if topic in self.topic_callbacks:
                self.topic_callbacks[topic](topic, message)

    def publish(self, topic, payload, retain=True, qos=1):
        # try wifi reconnect in case it lost connection
        utils.wifi_connect()

        if not isinstance(payload, bytes):
            payload = bytes(str(payload), 'utf-8')
        t = b'/'.join((self.topic, topic))
        done = False
        while not done:
            try:
                print('MQTT PUBLISH: {} --> {}'.format(t, payload))
                self.mqtt.publish(t, payload, retain=retain, qos=qos)
                done = True
            except Exception as e:
                # some error during publishing
                done = False
                done_reconnect = False
                utime.sleep(RETRY_DELAY)
                # tries to reconnect
                while not done_reconnect:
                    try:
                        self._umqtt_connect()
                        self.publish_properties()  # re-publish
                        done_reconnect = True
                    except Exception as e:
                        done_reconnect = False
                        print('ERROR: cannot connect, {}'.format(str(e)))
                        utime.sleep(RETRY_DELAY)

    def publish_properties(self):
        """publish device and node properties"""
        # node properties
        properties = (
            Property(b'$homie', b'3.0.0', True),
            Property(b'$name', self.settings.DEVICE_NAME, True),
            Property(b'$fw/name', self.settings.DEVICE_FW_NAME, True),
            Property(b'$fw/version', __version__, True),
            Property(b'$implementation', bytes(sys.platform, 'utf-8'), True),
            Property(b'$localip', utils.get_local_ip(), True),
            Property(b'$mac', utils.get_local_mac(), True),
            Property(b'$stats', b'uptime,freeheap,signal', True),
            Property(b'$stats/interval', self.stats_interval, True),
            Property(b'$nodes', b','.join(self.node_ids), True)
        )

        # publish all properties
        for prop in properties:
            self.publish(*prop)

        # device properties
        for node in self.nodes:
            try:
                for prop in node.get_properties():
                    self.publish(*prop)
            except NotImplementedError:
                raise
            except Exception:
                self.node_error(node)

        # all setup - publish device ready state
        self.publish(b'state', b'ready')

    def publish_data(self):
        """publish node data if node has updates"""
        self.publish_device_stats()
        # node data
        for node in self.nodes:
            try:
                if node.has_update():
                    for prop in node.get_data():
                        self.publish(*prop)
            except NotImplementedError:
                raise
            except Exception:
                self.node_error(node)

    def publish_device_stats(self):
        if utime.time() > self.next_update:
            # uptime
            uptime = utime.time() - self.start_time
            self.publish(b'$stats/uptime', uptime, True)
            # freeheap
            self.publish(b'$stats/freeheap', gc.mem_free(), True)
            # wifi signal
            self.publish(b'$stats/signal', utils.get_wifi_signal(), True)
            # set next update
            self.next_update = utime.time() + self.stats_interval

    def node_error(self, node):
        self.errors += 1
        print('ERROR: during publish_data for node: {}'.format(node))
        self.publish(b'state', b'alert')
