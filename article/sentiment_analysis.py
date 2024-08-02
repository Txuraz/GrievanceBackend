from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

nltk.download('wordnet')
nltk.download('sentiwordnet')
nltk.download('punkt')
nltk.download('stopwords')

NEGATION_WORDS = {'not', 'no', 'never', 'nothing', 'none', 'neither', 'nor'}

vader_analyzer = SentimentIntensityAnalyzer()

def get_sentiwordnet_score(word):
    synsets = list(swn.senti_synsets(word))
    if not synsets:
        return 0
    score = sum(synset.pos_score() - synset.neg_score() for synset in synsets) / len(synsets)
    return score

def handle_negations(text):
    words = word_tokenize(text.lower())
    negated = False
    sentiment = []
    for word in words:
        if word in NEGATION_WORDS:
            negated = not negated
        else:
            sentiment.append(word if not negated else f"NOT_{word}")
    return ' '.join(sentiment)

def analyze_sentiment(text):
    # Analyze sentiment using VADER
    vader_score = vader_analyzer.polarity_scores(text)
    vader_sentiment = 'neutral'
    if vader_score['compound'] >= 0.1:
        vader_sentiment = 'positive'
    elif vader_score['compound'] <= -0.1:
        vader_sentiment = 'negative'

    # Analyze sentiment using SentiWordNet
    words = [word for word in word_tokenize(handle_negations(text).lower()) if word.isalnum()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]

    sentiwordnet_scores = [get_sentiwordnet_score(word) for word in filtered_words]
    if not sentiwordnet_scores:
        sentiwordnet_sentiment = 'neutral'
    else:
        avg_score = sum(sentiwordnet_scores) / len(sentiwordnet_scores)
        if avg_score > 0.05:
            sentiwordnet_sentiment = 'positive'
        elif avg_score < -0.05:
            sentiwordnet_sentiment = 'negative'
        else:
            sentiwordnet_sentiment = 'neutral'

    # Combine VADER and SentiWordNet results with weighted votes
    sentiment_votes = {
        'positive': 0.2,
        'negative': 0.5,  # Increased weight for negative
        'neutral': 0.3
    }

    sentiment_votes[vader_sentiment] += 0.7
    sentiment_votes[sentiwordnet_sentiment] += 0.3

    # Determine final sentiment based on the most votes
    final_sentiment = max(sentiment_votes, key=sentiment_votes.get)

    return final_sentiment
