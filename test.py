import sqlite3
import pandas as pd

def check_my_data():
    print(" Fetching data from SQLite using standard SQL...\n")
    
    # 1. Database se connect kar rahe hain
    conn = sqlite3.connect("market_data.db")

    # --- Query 1: Commodity Table ---
    # Dekho, yeh ekdum standard MySQL wali SELECT query hai!
    sql_query_1 = "SELECT * FROM commodity_metrics;"
    
    # Pandas ka jaadu: read_sql_query seedha SQL chalata hai aur result DataFrame mein de deta hai
    df_commodities = pd.read_sql_query(sql_query_1, conn)
    
    print(" TABLE 1: Commodity Prices")
    print(df_commodities)
    print("-" * 50)

    # --- Query 2: News Sentiment Table ---
    # Ek aur standard SQL query: ORDER BY aur LIMIT lagakar top headlines nikal rahe hain
    sql_query_2 = """
        SELECT date, headline, sentiment_score 
        FROM news_sentiment 
        ORDER BY sentiment_score DESC 
        LIMIT 5;
    """
    df_news = pd.read_sql_query(sql_query_2, conn)
    
    print(" TABLE 2: Top News Headlines (Sorted by Sentiment)")
    print(df_news)
    print("-" * 50)

    # Connection band karna best practice hai
    conn.close()

if __name__ == "__main__":
    check_my_data()