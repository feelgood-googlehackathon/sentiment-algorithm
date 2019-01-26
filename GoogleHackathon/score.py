# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import json

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
            s += " "
            s += j
            s += " "
        tweets.append(s)

    score = []
    for text in tweets:
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        sentiment = client.analyze_sentiment(document=document).document_sentiment
        score.append(sentiment.score)

    average = sum(score)/len(score)

    # score ranges between -1 and 1
    if average > 0.2:
        print("The user is having a good day")
    elif average < -0.2:
        print("The user is having a bad day")
    else:
        print("The user is having a neutral day")

    return average

print("Your score is: ", score("data.json"))
