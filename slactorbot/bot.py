#!/usr/bin/env python
import sys
import time
import yaml
from lib import plugins
from slackclient import SlackClient
from thespian.actors import *


def start(config_file):
    with open(config_file, 'r') as stream:
        config = yaml.load(stream)

    slack_token = config['slack_token']

    slack_client = SlackClient(slack_token)
    actor_system = ActorSystem()
    plugin_actors = {}

    if slack_client.rtm_connect():
        print "bot started"
        while True:
            try:
                plugin_actors = plugins.load_plugins(actor_system, plugin_actors)
                message = slack_client.rtm_read()
                if isinstance(message, list) and len(message) > 0:
                    message = message[0]
                    if message['type'] == 'message':
                        for plugin_name, plugin_actor in plugin_actors.iteritems():
                            print actor_system.ask(plugin_actor['actor'], message['text'], 1.5)
                time.sleep(1)
            except KeyboardInterrupt:
                actor_system.shutdown()
                sys.exit(0)
    else:
        print "Connection Failed, invalid token?"