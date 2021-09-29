from flask import Flask, request
from germansentiment import SentimentModel

app = Flask(__name__)
model = SentimentModel()

@app.route('/')
def hello():
    return 'Hello World'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''
    query_result = req.get('queryResult')
    phrase = req.get('phrase')
    result = model.predict_sentiment(phrase)

    if query_result.get('action') == 'DefaultWelcomeIntent.DefaultWelcomeIntent-yes':
        if result == 'positive':
            fulfillmentText = 'Dein Kommentar ist positiv!'
        if result == 'neutral':
            fulfillmentText = 'Dein Kommentar ist neutral!'
        if result == 'negative':
            fulfillmentText = 'Dein Kommentar ist negativ!'
    
    return {
        'fulfillmentText': fulfillmentText,
        'source': 'webhookdata'
    }

if __name__ == '__main__':
    app.run(debug=True)