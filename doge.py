import json
import SocketServer

from flask import Flask, request
import requests

app = Flask(__name__)

DOGE_API = ('http://pubapi.cryptsy.com/api.php?method=singlemarketdata'
            '&marketid=182')
API_VERSION = '1.0'
ssl_enable = False


@app.route("/")
def main():
    return 'Hello world! o/'


@app.route("/alexa/api", methods=['GET', 'POST'])
def apicalls():
    if request.method == 'POST':
        data = request.get_json()
        if data.get('type') == 'IntentRequest':
            return _intent(data)
        elif data.get('type') == 'LaunchRequest':
            return _launch(data)
        elif data.get('type') == 'SessionEndedRequest':
            return _end(data)

            # sessionId = myApp.data_handler(data)
            # return sessionId + "\n"


@app.route("/doge/price")
def doge_price():
    return _get_current_doge_price()


def _intent(data):
    print "Intent", data
    price = _get_current_doge_price() * 1000000

    response = AlexaResponse(
        'One million Doge coins are worth {.2f} dollars.'.format(price))
    return response.to_json()

def _launch(data):
    print "Launch", data


def _end(data):
    print "End", data


def _get_current_doge_price():
    response = requests.get(DOGE_API)
    return response.json()['return']['markets']['DOGE']['lasttradeprice']


def run_app():
    # SocketServer.BaseServer.handle_error = close_stream
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    _run(app)


def _run(app):
    try:
        if ssl_enable:
            # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            # context.load_cert_chain('yourserver.crt', 'yourserver.key')
            '''
            Generate a private key:
                openssl genrsa -des3 -out server.key 1024

                Generate a CSR
                openssl req -new -key server.key -out server.csr

                Remove Passphrase from key
                cp server.key server.key.org openssl rsa -in server.key.org
                -out server.key

                Generate self signed certificate
                openssl x509 -req -days 365 -in server.csr -signkey
                server.key -out server.crt
            '''

            app.run(debug=True,
                    port=5000,
                    threaded=True,
                    use_reloader=False,
                    use_debugger=True,
                    ssl_context='adhoc',
                    # ssl_context=('yourserver.crt', 'yourserver.key')
                    host='0.0.0.0'
                    )
        else:
            app.run(debug=True,
                    port=5000,
                    threaded=True,
                    use_reloader=True,
                    use_debugger=True,
                    host='0.0.0.0'
                    )
    finally:
        print "Disconnecting clients"

    print "Done"


class AlexaResponse(object):
    def __init__(self, speech):
        self.speech = speech

    def to_json(self):
        response = {
            "version": API_VERSION,
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": self.speech
                }
            }
        }

        return json.dumps(response)


if __name__ == "__main__":
    run_app()
