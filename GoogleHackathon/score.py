# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json
import falcon
from falcon.http_status import HTTPStatus

# Instantiates a client
client = language.LanguageServiceClient()

def score(filename):
    '''
        method returning score indicating how positive (or negative) a
        sentence is i.e. sentiment of the text
    '''
    with open(filename, 'r') as data_file:
        data = json.load(data_file)

    tweets = []
    for item in data['data']:
        s = item['text']
        for j in item['entities']['hashtags']:
            s += " " + j + " "
        tweets.append(s)

    score = []
    for text in tweets:
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment = client.analyze_sentiment(document=document).document_sentiment
        score.append(sentiment.score)

    average = sum(score)/len(score)

    return average

# things.py

# Let's get this party started!

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = str(score("data.json"))


class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')

app = falcon.API(middleware=[HandleCORS() ])


# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/things', things)
