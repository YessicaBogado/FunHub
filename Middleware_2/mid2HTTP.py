# mid2XMPP
# (derived from basexmppbot.py / ported to python3-nbxmpp)

from flask import Flask
from flask import jsonify
import mid2XMPP0 as xmpp

app = Flask(__name__)


@app.route('/listFun', methods=['GET'])
def listFun():
    """Request from FunctionHub."""
    jidparams = {}
    jidparams['jid'] = "midFH@localhost"
    jidparams['password'] = "7777"
    jidparams['to_jid'] = "midSnafu@localhost"
    text = "listFun"
    con = xmpp.init(jidparams, text)
    msg = con.worksafely()
    # msg = xmpp.Connector.get_msg()
    return (msg.encode('utf-8').decode())


if __name__ == '__main__':
    app.run(host='localhost', port=5006)
