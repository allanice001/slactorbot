# slactorbot

A slack bot that uses lightweights actors and dynamic module imports for plugins

# Usage

Copy the config.yaml.example to config.example and update the settings

Then `./run_bot.py`

# Plugins

Create or modify any file with a .py extension in the slactorbot/plugins directory. slactorbot will reload
them without needing to restart.

The plugins are little actors that get dynamically imported. They each need a class called `Main` and
a `receiveMessage` function.

Every actor will get passed the firehose of messages from Slack. You'll need to put a regex on the `msg`
and then you can perform actions and send back the result.

If in doubt have a look at the example.py plugin.

# Todo

Needs more slack stuff. Currently it just listens and prints the messages to stdout. I'll add the slack
integrations next.