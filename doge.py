import json
import SocketServer

from flask import Flask, request
import requests

app = Flask(__name__)

DOGE_API = ('http://pubapi.cryptsy.com/api.php?method=singlemarketdata'
            '&marketid=182')

ALEXA_API_VERSION = '1.0'

intents = []
launch_intent = None
end_intent = None


@app.route("/")
def main():
    return 'Hello world! o/'


@app.route("/alexa/api", methods=['POST'])
def apicalls():
    # global intents
    # global launch_intent

    if request.method == 'POST':
        data = request.get_json()
        print "Received POST: {}".format(data)
        if data['request'].get('type') == 'IntentRequest':
            intent_name = data['request'].get('intent', {}).get('name')
            for intent in intents:
                if intent.name == intent_name:
                    return intent.handle(data)
        elif data['request'].get('type') == 'LaunchRequest':
            return launch_intent.handle(data)
        elif data['request'].get('type') == 'SessionEndedRequest':
            return end_intent.handle(data)


def run_app():
    # SocketServer.BaseServer.handle_error = close_stream
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    app.run(debug=True,
            port=5000,
            threaded=True,
            use_reloader=True,
            use_debugger=True,
            host='0.0.0.0')


def _get_current_doge_price():
    response = requests.get(DOGE_API)
    return response.json()['return']['markets']['DOGE']['lasttradeprice']


class Intent(object):
    # The IntentName to respond to
    name = None

    def handle(self, data):
        """Handles an IntentRequest.

        :param data: the JSON data sent by Amazon
        """
        raise NotImplementedError()


class NoopIntent(object):
    def handle(self, data):
        print 'Noop'
        return json.dumps({})


class DogeCoinIntent(Intent):
    name = 'DogeCoin'

    def handle(self, data):
        price = float(_get_current_doge_price()) * 1000000

        response = AlexaResponse('One million Doge coins are worth {0:.2f} '
                                 'dollars. Wow!'.format(price))
        return response.to_json()


class USDtoDoge(Intent):
    name = 'USDtoDOGE'

    def handle(self, data):
        price = float(_get_current_doge_price())
        dollars = int(data['request']['intent']['slots']['dollars']['value'])
        return AlexaResponse('{0} dollars is worth {1:.2f} dogecoins'.format(
            dollars, dollars / price)).to_json()


class DogeToUSD(Intent):
    name = 'DOGEtoUSD'

    def handle(self, data):
        price = float(_get_current_doge_price())
        coins = int(data['request']['intent']['slots']['coins']['value'])
        return AlexaResponse(
            '{0} dogecoins is worth {1:} dollars and {2} cents'.format(
                coins,
                int(coins * price),
                int((coins * price - int(coins * price)) * 100))).to_json()


class HelpIntent(Intent):
    name = 'HelpIntent'

    def handle(self, data):
        return AlexaResponse(
            'Just ask what the current price is. Much easy. Wow.').to_json()


class AlexaResponse(object):
    def __init__(self, speech):
        self.speech = speech

    def to_json(self):
        # TODO(pcsforeducation) add card support
        response = {
            "version": ALEXA_API_VERSION,
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": self.speech
                }
            }
        }

        return json.dumps(response)


if __name__ == "__main__":
    # Each of these intent classes name attrs will be matched against intent
    # name sent by Amazon
    ENABLED_INTENTS = [
        DogeCoinIntent,
        DogeToUSD,
        USDtoDoge,
        HelpIntent,
    ]

    # The intent to handle launch events like 'Open Dogecoin'
    launch_intent = DogeCoinIntent()

    # The intent to handle event at the end of a session
    end_intent = NoopIntent

    for intent in ENABLED_INTENTS:
        intents.append(intent())

    run_app()
