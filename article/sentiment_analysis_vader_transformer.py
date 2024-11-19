import joblib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import psutil

# Load the pre-trained model and vectorizer
sentiment_model = joblib.load('sentiment_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Initialize VADER Sentiment Analyzer
vader_analyzer = SentimentIntensityAnalyzer()

try:
    sentiment_pipeline = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    print("Failed to load the transformer model:", e)
    sentiment_pipeline = None

def analyze_sentiment_vader(text):
    vader_score = vader_analyzer.polarity_scores(text)
    if vader_score['compound'] >= 0.1:
        return 'positive'
    elif vader_score['compound'] <= -0.1:
        return 'negative'
    else:
        return 'neutral'

def analyze_sentiment_transformer(text):
    if sentiment_pipeline:
        result = sentiment_pipeline(text)[0]
        return result['label'].lower()  # 'LABEL_0' = negative, 'LABEL_1' = positive
    else:
        return 'neutral'

def map_sentiment_to_emotions(sentiment):
    emotion_map = {
        'positive': [
            'Acceptance', 'Affection', 'Amusement', 'Euphoria', 'Excitement', 'Empowerment',
            'Joy', 'Love', 'Optimism', 'Pride', 'Gratitude', 'Hope', 'Contentment',
            'Trust', 'Curiosity', 'Cheerfulness'
        ],
        'negative': [
            'Sadness', 'Grief', 'Fear', 'Anger', 'Frustration', 'Disgust', 'Anxiety',
            'Guilt', 'Shame', 'Embarrassment', 'Boredom', 'Helplessness', 'Regret'
        ],
        'neutral': [
            'Indifference', 'Calmness', 'Serenity', 'Confusion', 'Nostalgia', 'Surprise', 'Uncertainty'
        ],
        'mixed': [
            'Bittersweet', 'Ambivalence', 'Mixed Feelings', 'Satisfaction', 'Resentment'
        ]
    }
    if sentiment in emotion_map:
        return emotion_map[sentiment]
    else:
        return []

def analyze_sentiment(text):
    available_memory = psutil.virtual_memory().available
    if available_memory < 100 * 1024 * 1024:
        print("Warning: Low memory, sentiment analysis may fail.")

    # Use the pre-trained RandomForest model with TF-IDF vectorizer
    text_tfidf = tfidf_vectorizer.transform([text])
    rf_sentiment = sentiment_model.predict(text_tfidf)[0]

    # Get sentiment from VADER
    vader_sentiment = analyze_sentiment_vader(text)

    # Get sentiment from transformer model
    transformer_sentiment = analyze_sentiment_transformer(text)

    sentiment_votes = {
        'positive': 0,
        'negative': 0,
        'neutral': 0
    }

    # Voting mechanism to determine final sentiment
    sentiment_votes[vader_sentiment] += 1
    sentiment_votes[transformer_sentiment] += 1
    sentiment_votes[rf_sentiment] += 1  # Include RandomForest model in the voting

    # Determine final sentiment based on the most votes
    final_sentiment = max(sentiment_votes, key=sentiment_votes.get)

    # Handle ties (if both positive and negative votes are equal and neutral is zero)
    if sentiment_votes['positive'] == sentiment_votes['negative'] and sentiment_votes['neutral'] == 0:
        final_sentiment = 'neutral'

    # Map the final sentiment to emotion categories
    emotion_categories = map_sentiment_to_emotions(final_sentiment)

    return final_sentiment, emotion_categories

# Example usage
text = "I received the product, but there was nothing particularly outstanding about the experience. It was just okay."
final_sentiment, emotion_categories = analyze_sentiment(text)

print(f"Final Sentiment: {final_sentiment}")
print(f"Emotion Categories: {emotion_categories}")