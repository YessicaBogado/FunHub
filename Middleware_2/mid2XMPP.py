# mid2XMPP
# (derived from basexmppbot.py / ported to python3-nbxmpp)

import os
import nbxmpp
import threading
import configparser
import urllib.parse
try:
    from gi.repository import GObject as gobject
except Exception:
    import gobject


global response


class BaseXMPPBot:
    def __init__(self, botname, jid, password, target, to_jid, text, debug=True):
        self.initinternal(botname, jid, password, target)
        self.readystep = 0
        self.debug = debug
        self.lasttime = 0
        self.to_jid = to_jid
        self.text = text

    def initinternal(self, botname, jid, password, target):
        self.botname = botname
        self.jid = jid
        self.password = password
        self.target = target

    def presenceHandler(self, conn, presence_node):
        if self.debug:
            print(":: xmpp presence")

    def iqHandler(self, conn, iq_node):
        if self.debug:
            print(":: xmpp iq")

        reply = iq_node.buildReply('result')
        conn.send(reply)
        raise nbxmpp.NodeProcessed

    def messageHandler(self, conn, mess_node):
        if self.debug:
            print(":: xmpp handler", "[" + str(mess_node.getFrom()) + "]",
                  mess_node.getBody())

        if self.readystep == 0:
            self.readystep = 1

        print("---------------mess_node.getFrom: ", str(mess_node.getFrom()))
        if "messageroutine" in dir(self):
            self.messageroutine(str(mess_node.getFrom()),
                                str(mess_node.getBody()))

    def on_auth(self, con, auth):
        if not auth:
            if self.debug:
                print(":: xmpp could not authenticate!")
            return
        if self.debug:
            print(":: xmpp authenticated using " + auth)

        self.client.RegisterHandler('presence', self.presenceHandler)
        self.client.RegisterHandler('iq', self.iqHandler)
        self.client.RegisterHandler('message', self.messageHandler)

        self.client.sendPresence()
        if self.target:
            self.client.sendPresence(self.target + "/" + self.botname)
        self.send_message(self.to_jid, self.text)

    def get_password(self, cb, mech):
        cb(self.password)

    def on_connect(self, con, con_type):
        if self.debug:
            print(":: xmpp connected", con, con_type)
        auth = self.client.auth(self.jidproto.getNode(), self.password,
                                resource=self.jidproto.getResource(), sasl=1,
                                on_auth=self.on_auth)

    def on_failure(self):
        if self.debug:
            print(":: xmpp connection failed")

    def connect(self):
        self.readystep = 0

        self.client_cert = None
        self.sm = nbxmpp.Smacks(self)

        self.jidproto = nbxmpp.protocol.JID(self.jid)
        self.client = nbxmpp.NonBlockingClient(
            self.jidproto.getDomain(), nbxmpp.idlequeue.get_idlequeue(),
            caller=self)
        self.client.connect(self.on_connect, self.on_failure,
                            secure_tuple=('tls', '', '', None, None))

    def _event_dispatcher(self, realm, event, data):
        if self.debug:
            print(":: xmpp dispatcher >> realm:", realm, "event:", type(event),
                  event, "data:", type(data), data)
        pass

    def worksafely(self):
        """Create Thread."""
        self.connect()
        ml = gobject.MainLoop()
        self.save_ml(ml)
        gobject.timeout_add(20000, ml.quit)
        ml.run()
        return self.get_msg()

    def send_message(self, to_jid, text):
        id_ = self.client.send(nbxmpp.protocol.Message(to_jid, text, typ='chat'))
        print('sent message with id ' + id_)



class Connector(BaseXMPPBot):
    def __init__(self, jid, password, to_jid, text, debug):
        target = None
        botname = None

        BaseXMPPBot.__init__(self, botname, jid, password, target, to_jid,
                             text, debug)

    def save_ml(self, ml):
        self.ml = ml

    def messageroutine(self, sender, msg):
        if self.debug:
            print(":: (xmpp connector) message received...", msg)
            print("--------sender: ", sender)
            print("--------msg: ", msg)
            gobject.timeout_add(10, self.ml.quit)
            # self.client.send(nbxmpp.protocol.Message(sender, response, typ="chat"))
            self.msg = msg

    def get_msg(self):
        return self.msg


def initinternal(jid, to_jid, password, text):
    debug = True
    connector = None
    if debug:
        print(":: (xmpp url) debug on")
    connector = Connector(jid, password, to_jid, text, debug)
    return connector


def init(jid_params, text):
    jid = jid_params['jid']
    password = jid_params['password']
    to_jid = jid_params['to_jid']
    a = initinternal(jid=jid, to_jid=to_jid, password=password, text=text)
    return a
