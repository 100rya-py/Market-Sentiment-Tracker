import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import pandas as pd

nltk.download('vader_lexicon',quiet=True)

def analyze_headline_sentiment(headline):
    """
    This function will take an English headline and return a mathematical sentiment score.
    
    """

    sia = SentimentIntensityAnalyzer()
    #calling polarity_scores which returns a dictionary with 4 metrics:
    #'neg' (negative), 'neu' (neutral), 'pos' (positive), aur 'compound'.
    sentiment_dict = sia.polarity_scores(headline)

    #compound is the normalized aggregate mathematical score of the other 3
    final_score = sentiment_dict['compound']
    return final_score


def create_market_dataframe(headlines,gold_price,silver_price):
    """
    Converts lists of text headlines and float commodity prices into a structured Pandas DataFrame.
    Iterates through the headlines to calculate the NLTK VADER compound sentiment score for each,
    and broadcasts the daily date, gold price, and silver price across all rows for time-series analysis.
    """

    data_rows=[]

    today_date = datetime.now().strftime("%Y-%m-%d")
    
    for text in headlines:
        score = analyze_headline_sentiment(text)
        row={
            'date':today_date,
            'headline':text,
            'sentiment_score':score,
            'gold_price':gold_price,
            'silver_price':silver_price
        }
        data_rows.append(row)
    
    df=pd.DataFrame(data_rows)
    return df
