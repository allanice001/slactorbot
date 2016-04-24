from thespian.actors import *


class Main(Actor):
    def receiveMessage(self, msg, sender):
        if isinstance(msg, list) and len(msg) == 0:
            self.send(sender, 'usage: dlbot example kitten')
        elif msg[0] == 'kitten':
            self.send(sender, 'I bet you expected a kitten picture')
        else:
            self.send(sender, 'unknown example command')