# -*- coding: utf-8 -*-
'''
Created on 16.04.2013

@author: bova
'''
import logging
import sleekxmpp

XMPP_SERV = 'jabber.fido.uz'
XMPP_PORT = 5222
XMPP_USER = 'wpump@fido.uz'
XMPP_PASS = 'Q1w3tre'

class SendMsgBot(sleekxmpp.ClientXMPP):

    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid=XMPP_USER, password=XMPP_PASS):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = ''
        self.msg = ''

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)

    def chat(self, recipient, msg):
        self.recipient = recipient
        self.msg = msg
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping

        if self.connect((XMPP_SERV, XMPP_PORT)):
            self.process(block=True)
            print("Done")
        else:
            print("Unable to connect.")
            
if __name__ == '__main__':

    # Setup logging.
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-8s %(message)s')
    
    xmpp = SendMsgBot()
    xmpp.chat(u'Владимир@fido.uz', 'Hello!')
