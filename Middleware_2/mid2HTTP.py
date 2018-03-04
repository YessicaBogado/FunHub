# mid2XMPP
# (derived from basexmppbot.py / ported to python3-nbxmpp)

from flask import Flask
from flask import jsonify
from flask import request
import mid2XMPP as xmpp

app = Flask(__name__)

jidparams = {}
jidparams['jid'] = "midFH@localhost"
jidparams['password'] = "7777"
jidparams['to_jid'] = "midSnafu@localhost"


@app.route('/listFun', methods=['GET'])
def listFun():
    """Request from FunctionHub."""
    text = "listFun"
    con = xmpp.init(jidparams, text)
    msg = con.worksafely()
    # msg = xmpp.Connector.get_msg()
    return (msg.encode('utf-8').decode())


@app.route('/function-download/<function>.zip', methods=['GET'])
def download_function(function):
    """Request from FunctionHub."""
    text = "download " + str(function)
    con = xmpp.init(jidparams, text)
    msg = con.worksafely()
    # msg = xmpp.Connector.get_msg()
    return (msg.encode('utf-8').decode())


@app.route('/test/<function>', methods=['GET'])
def test(function):
    """Request from FunctionHub."""
    text = "test " + str(function)
    con = xmpp.init(jidparams, text)
    msg = con.worksafely()
    # msg = xmpp.Connector.get_msg()
    return (msg.encode('utf-8').decode())


@app.route('/test/<function>/<args>', methods=['GET'])
def test_args(function, args):
    """Request from FunctionHub."""
    text = "test " + str(function) + " " + str(args)
    con = xmpp.init(jidparams, text)
    msg = con.worksafely()
    # msg = xmpp.Connector.get_msg()
    return (msg.encode('utf-8').decode())


if __name__ == '__main__':
    app.run(host='localhost', port=5006)
