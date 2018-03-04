# mid1XMPP
# (derived from basexmppbot.py / ported to python3-nbxmpp)

import os
import io
import nbxmpp
import configparser
import urllib.parse
import urllib.request
import requests
import zipfile
from gi.repository import GObject as gobject


class BaseXMPPBot:
    def __init__(self, botname, jid, password, target, debug=True):
        self.initinternal(botname, jid, password, target)
        self.readystep = 0
        self.debug = debug
        self.lasttime = 0

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
        self.connect()
        ml = gobject.MainLoop()
        ml.run()

    def post(self, msg):
        tojid = "haydee@localhost"
        text = ' '.join("listFun")

        self.client.send(nbxmpp.protocol.Message(self.target, msg,
                                                 "groupchat"))


class Connector(BaseXMPPBot):
    def __init__(self, connectconfig, port, debug):
        u = urllib.parse.urlparse(connectconfig)
        password = u.password
        jid = u.username + "@" + u.hostname
        self.port = port
        target = None
        botname = None
        BaseXMPPBot.__init__(self, botname, jid, password, target, debug=debug)

    def messageroutine(self, sender, msg):
        """Snafu response."""
        if self.debug:
            print(":: (xmpp connector) message received...", msg)

        if (msg == "listFun"):
            response = urllib.request.urlopen(
                "http://0.0.0.0:{}/functions/funHub".format(self.port)).read()

        else:
            msg = msg.split(" ")
            if msg[0] == "download":
                fun = "http://0.0.0.0:{}/function-download/{}.zip".format(
                    self.port, msg[1])
            # response = zipfile.ZipFile(io.BytesIO(fun.content))
                response = urllib.request.urlopen(fun).read()
            if msg[0] == "test":
                if len[msg] == 3:
                    args = msg[2]
                    function_test = msg[1]
                    fun = "http://0.0.0.0:{}/invoke/{}/{}".format(
                        self.port, args, function_test)
                elif len[msg] == 2:
                    function_test = msg[1]
                    fun = "http://0.0.0.0:{}/invoke/{}/".format(
                        self.port, function_test)
                else:
                    fun = "http://0.0.0.0:{}/invoke/".format(self.port)
                response = urllib.request.urlopen(fun).read()

        self.client.send(nbxmpp.protocol.Message(sender, response, typ="chat"))


def initinternal(function, configpath):
    debug = True

    connectconfig = None
    if not configpath:
        configpath = "mid1.ini.dist"
    if not function:
        function = "mid1"
    if os.path.isfile(configpath):
        config = configparser.ConfigParser()
        config.read(configpath)
        if function in config and "connector.xmpp" in config[function]:
            connectconfig = config[function]["connector.xmpp"]
            port = config[function]["port"]

    if debug:
        print(":: (xmpp url)", connectconfig)
        connector = Connector(connectconfig, port, debug)

    if connectconfig:
        connector.worksafely()


def init(function=None, configpath=None):
    initinternal(function, configpath)


if __name__ == '__main__':
    init()
