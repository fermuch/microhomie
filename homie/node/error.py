"""
This node implements all required functions of a node but it will also always
raise Exceptions to test the devices
"""

from homie.node import HomieNode


class Error(HomieNode):

    def has_update(self):
        return True

    def __str__(self):
        return "ErrorNode"

    def get_properties(self):
        raise Exception('ErrorNode Test Exception - get_properties')

    def get_data(self):
        raise Exception('ErrorNode Test Exception - get_data')

    def update_data(self):
        raise Exception('ErrorNode Test Exception - update_data')

    def callback(self, topic, payload):
        raise Exception('ErrorNode Test Exception - callback')

    def broadcast_callback(self, payload):
        raise Exception('ErrorNode Test Exception - broadcast_callback')

    def get_node_properties(self):
        raise Exception('ErrorNode Test Exception - get_node_id')
