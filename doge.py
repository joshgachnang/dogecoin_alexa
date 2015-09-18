import json
import SocketServer

from flask import Flask, request
import requests

app = Flask(__name__)

DOGE_API = ('http://pubapi.cryptsy.com/api.php?method=singlemarketdata'
            '&marketid=182')
API_VERSION = '1.0'


@app.route("/")
def main():
    return 'Hello world! o/'


@app.route("/alexa/api", methods=['GET', 'POST'])
def apicalls():
    if request.method == 'POST':
        data = request.get_json()
        print data
        if data['request'].get('type') == 'IntentRequest':
            return _intent(data)
        elif data['request'].get('type') == 'LaunchRequest':
            return _launch(data)
        elif data['request'].get('type') == 'SessionEndedRequest':
            return _end(data)


@app.route("/doge/price")
def doge_price():
    return _get_current_doge_price()


def _intent(data):
    print "Intent", data
    if data['request'].get('intent', {}).get('name') == 'HelpIntent':
        return _help(data)
    elif data['request'].get('intent', {}).get('name') == 'DogeCoin':
        return _dogecoin(data)


def _dogecoin(data):
    price = float(_get_current_doge_price()) * 1000000

    response = AlexaResponse(
        'One million Doge coins are worth {0:.2f} dollars. Wow!'.format(price))
    return response.to_json()


def _help(data):
    return AlexaResponse(
        'Just ask what the current price is. Much easy. Wow.').to_json()


def _launch(data):
    print "Launch", data


def _end(data):
    print "End", data
    return json.dumps({'response': 'ok'})


def _get_current_doge_price():
    response = requests.get(DOGE_API)
    return response.json()['return']['markets']['DOGE']['lasttradeprice']


def run_app():
    # SocketServer.BaseServer.handle_error = close_stream
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    app.run(debug=True,
            port=5000,
            threaded=True,
            use_reloader=True,
            use_debugger=True,
            host='0.0.0.0')


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
