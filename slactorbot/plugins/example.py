from thespian.actors import *


class Main(Actor):
    def receiveMessage(self, msg, sender):
        self.send(sender, 'Example Reply')