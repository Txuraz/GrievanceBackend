# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from transformers import pipeline
# import psutil
#
# # Initialize VADER
# vader_analyzer = SentimentIntensityAnalyzer()
#
# # Initialize transformer-based sentiment analysis pipeline
# try:
#     sentiment_pipeline = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")
# except Exception as e:
#     print("Failed to load the transformer model:", e)
#     sentiment_pipeline = None
#
#
# def analyze_sentiment_vader(text):
#     vader_score = vader_analyzer.polarity_scores(text)
#     if vader_score['compound'] >= 0.1:
#         return 'positive'
#     elif vader_score['compound'] <= -0.1:
#         return 'negative'
#     else:
#         return 'neutral'
#
#
# def analyze_sentiment_transformer(text):
#     if sentiment_pipeline:
#         result = sentiment_pipeline(text)[0]
#         return result['label'].lower()
#     else:
#         return 'neutral'
#
#
# def analyze_sentiment(text):
#     # Check available memory before processing
#     available_memory = psutil.virtual_memory().available
#     if available_memory < 100 * 1024 * 1024:  # Less than 100MB
#         print("Warning: Low memory, sentiment analysis may fail.")
#
#     # Get VADER sentiment
#     vader_sentiment = analyze_sentiment_vader(text)
#
#     # Get transformer-based sentiment
#     transformer_sentiment = analyze_sentiment_transformer(text)
#
#     # Combine results (simple voting mechanism)
#     sentiment_votes = {
#         'positive': 0,
#         'negative': 0,
#         'neutral': 0
#     }
#
#     sentiment_votes[vader_sentiment] += 1
#     sentiment_votes[transformer_sentiment] += 1
#
#     # Determine final sentiment based on the most votes
#     final_sentiment = max(sentiment_votes, key=sentiment_votes.get)
#
#     # Handle ties (if both positive and negative votes are equal and neutral is zero)
#     if sentiment_votes['positive'] == sentiment_votes['negative'] and sentiment_votes['neutral'] == 0:
#         final_sentiment = 'neutral'
#
#     return final_sentiment
