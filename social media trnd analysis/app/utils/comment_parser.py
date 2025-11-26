import re
from textblob import TextBlob

def clean_comment(text: str) -> str:
    """Remove unwanted characters, links, mentions, etc."""
    text = re.sub(r"http\S+", "", text)         # remove URLs
    text = re.sub(r"@\w+", "", text)            # remove @mentions
    text = re.sub(r"#\w+", "", text)            # remove hashtags
    text = re.sub(r"[^A-Za-z0-9\s]+", "", text) # remove special chars
    return text.strip()

def analyze_sentiment(text: str) -> dict:
    """Perform simple sentiment analysis using TextBlob."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (negative) to +1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)

    if polarity > 0:
        sentiment = "positive"
    elif polarity < 0:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity
    }

def parse_comment(raw_comment: str) -> dict:
    """Clean + analyze a comment before inserting to DB."""
    cleaned = clean_comment(raw_comment)
    sentiment_data = analyze_sentiment(cleaned)
    return {
        "original": raw_comment,
        "cleaned": cleaned,
        "analysis": sentiment_data
    }
