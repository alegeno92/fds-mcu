import logging
import queue
from threading import Thread, Event
import time

import paho.mqtt.client as mqtt


class MqttLocalClient(Thread):

    def __init__(self, client_id=None, host='localhost', port=1883, subscription_paths=None, message_callback=None):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.client_id = client_id
        self.subscription_paths = subscription_paths
        self.message_queue = queue.Queue()
        self.client = mqtt.Client(client_id=self.client_id)
        self.callback = message_callback
        self.logger = logging.getLogger(__name__)
        self.is_connecting = Event()
        self.exit = Event()

    def publish(self, topic, payload, ):
        self.logger.debug('Publish to ' + topic + ' payload: ' + payload)
        while not self.is_connecting.wait(0.3) or self.exit.isSet():
            self.logger.debug('disconnected.. wait')

        self.client.publish(topic, payload)

    def publish_on_many_topics(self, topics, payload):
        for topic in topics:
            self.logger.debug('Publish to ' + topic + ' payload: ' + payload)
            self.client.publish(topic, payload)

    def run(self):
        self.logger.info('Connecting to mqtt -> ' + self.host + ':' + str(self.port))
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_message(self, client, obj, msg):
        if msg is not None:
            if self.callback is None:
                self.message_queue.put(msg)
            else:
                self.callback(msg)

    def subscribe_all(self, subscription_paths=None, qos=1):
        if subscription_paths is None:
            subscription_paths = []
        for path in subscription_paths:
            self.logger.debug('Subscribe to ' + path)
            self.client.subscribe(path, qos=qos)
            time.sleep(1)

    def set_callback(self, callback):
        self.callback = callback

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.logger.info('Connected to mqtt -> ' + self.host + ':' + str(self.port))
            self.subscribe_all(self.subscription_paths)
            self.is_connecting.set()

    def on_disconnect(self, client, userdata, rc):
        self.logger.info('disconnected')
        self.is_connecting.clear()

    def stop(self):
        self.client.loop_stop()
        self.exit.set()
