import sys
import network
# only native python (not esp32-loba) can reach this code.
# Micropython doesn't have typing module.
if sys.implementation.name not in ('micropython'):
  from typing import Optional, Callable, Tuple

class Mqtt:
  def __init__(
    self,
    name: str,
    server: str,
    user: Optional[str] = "",
    password: Optional[str] = "",
    port: Optional[int] = 1883,
    autoreconnect: Optional[bool] = False,
    clientid: Optional[str] = "mpy_mqtt_client",
    cleansession: Optional[bool] = False,
    keepalive: Optional[int] = 120,
    lwt_topic: Optional[str] = None,
    lwt_msg: Optional[str] = None,
    lwt_retain: Optional[bool] = 0,
    lwt_qos: Optional[0, 1, 2] = 0,
    cert: Optional[str] = None,
    connected_cb: Optional[Callable[[str], None]] = lambda x: None,
    disconnected_cb: Optional[Callable[[str], None]] = lambda x: None,
    subscribed_cb: Optional[Callable[[str, str], None]] = lambda x, y: None,
    unsubscribed_cb: Optional[Callable[[str, str], None]] = lambda x, y: None,
    published_cb: Optional[Callable[[str, bool], None]] = lambda x, y: None,
    data_cb: Optional[Callable[[str, int, [str, bytes]], None]] = lambda x, y, z: None
  ):
    pass
  
  def config(
    self,
    user: Optional[str] = "",
    password: Optional[str] = "",
    port: Optional[int] = 1883,
    autoreconnect: Optional[bool] = False,
    clientid: Optional[str] = "mpy_mqtt_client",
    cleansession: Optional[bool] = False,
    keepalive: Optional[int] = 120,
    lwt_topic: Optional[str] = None,
    lwt_msg: Optional[str] = None,
    lwt_retain: Optional[bool] = 0,
    lwt_qos: Optional[0, 1, 2] = 0,
    cert: Optional[str] = None,
    connected_cb: Optional[Callable[[str], None]] = lambda x: None,
    disconnected_cb: Optional[Callable[[str], None]] = lambda x: None,
    subscribed_cb: Optional[Callable[[str, str], None]] = lambda x, y: None,
    unsubscribed_cb: Optional[Callable[[str, str], None]] = lambda x, y: None,
    published_cb: Optional[Callable[[str, bool], None]] = lambda x, y: None,
    data_cb: Optional[Callable[[str, int, [str, bytes]], None]] = lambda x, y, z: None
  ) -> None:
    pass

  def status(self) -> Tuple[[int, str]]:
    pass
  
  def subscribe(
    self,
    topic: str,
    qos: Optional[0, 1, 2] = 0
  ) -> bool:
    pass
  
  def unsubscribe(self, topic: str) -> bool:
    pass
  
  def publish(self, topic: str, msg: [str, bytes], qos: [0, 1, 2] = 0) -> bool:
    pass
  
  def stop(self) -> None:
    pass
  
  def start(self) -> None:
    pass
  
  def free(self) -> None:
    pass
  
network.mqtt = Mqtt