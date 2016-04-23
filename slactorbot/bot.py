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
    slack_channel = config['slack_channel']
    bot_name = config['bot_name']

    slack_client = SlackClient(slack_token)
    actor_system = ActorSystem()
    plugin_actors = {}

    if slack_client.rtm_connect():
        print "bot started"
        channel = slack_client.server.channels.find(slack_channel)
        while True:
            try:
                plugin_actors = plugins.load_plugins(actor_system, plugin_actors)
                message = slack_client.rtm_read()
                if isinstance(message, list) and len(message) > 0:
                    message = message[0]
                    if 'type' in message.keys():
                        if message['type'] == 'message':
                            if 'text' in message.keys():
                                if message['text'].startswith(bot_name):
                                    commands = message['text'].split()
                                    if len(commands) == 1:
                                        channel.send_message('please specify a command or help')
                                    else:
                                        try:
                                            actor = commands[1]
                                            reply = actor_system.ask(plugin_actors[actor]['actor'], commands[2:], 1.5)
                                            channel.send_message(reply)
                                        except KeyError:
                                                channel.send_message('unknown command')
                time.sleep(1)
            except KeyboardInterrupt:
                actor_system.shutdown()
                sys.exit(0)
    else:
        print "Connection Failed, invalid token?"