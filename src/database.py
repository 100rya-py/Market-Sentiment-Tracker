import sqlite3
import pandas as pd
import os

DB_NAME = "market_data.db"

def setup_database():
    """
    Connects to the SQLite database and creates the necessary tables 
    ('news_sentiment' and 'commodity_metrics') if they do not exist.
    """

    #sqlite connection
    conn = sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    #table 1 : Commodity Metrics 
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS commodity_metrics(
                   date TEXT PRIMARY KEY,
                   gold_price REAL,
                   silver_price REAL
                   )
    ''')

    #table 2 : News Sentiment
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_sentiment(
                   date TEXT,
                   headline TEXT,
                   sentiment_score REAL,
                   PRIMARY KEY(date,headline)
                   )
    ''')

    conn.commit()
    conn.close()

    print("Database Schema initialized Successfully.")

def save_market_data(df):
        """
        Takes the merged Pandas DataFrame and safely upserts the data into 
        the SQLite tables using conflict handling to prevent duplication crashes.
        """
        
        conn=sqlite3.connect(DB_NAME)
        cursor=conn.cursor()

        if not df.empty:

           
            today = df.iloc[0]['date']
            gold = float(df.iloc[0]['gold_price'])
            silver=float(df.iloc[0]['silver_price'])

             #upsert for commodity_metrics
            cursor.execute('''
                INSERT INTO commodity_metrics(date,gold_price,silver_price)
                VALUES(?,?,?)
                ON CONFLICT(date) DO UPDATE SET
                           gold_price = excluded.gold_price,
                           silver_price=excluded.silver_price
            
            ''',(today,gold,silver))
        
        #upsert for news_segment
        for index,row in df.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO news_sentiment (date,headline,sentiment_score)
                VALUES(?,?,?)
        ''',(row['date'],row['headline'],row['sentiment_score']))
            
        conn.commit()
        conn.close()

        print("Data Successfully UPSERTED to SQLite Database")

if __name__ == "__main__":
    setup_database()


    


