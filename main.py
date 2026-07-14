import src.scraper as scraper
import src.analyzer as analyzer
import src.database as database

def run_pipeline():
    """
    Executes the ETL (Extract, Transform, Load) pipeline.
    Currently orchestrates Phase 1 (Extraction) and Phase 2 (Transformation).
    """
    print("Starting Data Pipeline....")

    #extracting raw data
    print("Scraping live market data....")

    news_url = "https://economictimes.indiatimes.com/industry/banking/finance/banking"
    raw_news_data = scraper.scrape_financial_news(news_url)
    raw_prices_data=scraper.scrape_commodity_prices()

    headlines_list = [item['Headline'] for item in raw_news_data]

    
    gold_price = 0.0
    silver_price =0.0

    for item in raw_prices_data:
        if item['Asset'] == 'Gold':
            gold_price = item['Price']
            
        elif item['Asset'] == 'Silver':
            silver_price = item['Price']

    print(f"-> Scraped {len(headlines_list)} banking headlines.")
    print(f"-> Gold ETF: Rs {gold_price}, Silver ETF: Rs {silver_price}")

    #transforming into dataframe
    final_market_df=analyzer.create_market_dataframe(
        headlines=headlines_list,
        gold_price =gold_price,
        silver_price = silver_price
    )
    
    #loading the data into database
    print("Saving Data to SQLite Database.....")
    database.setup_database()
    database.save_market_data(final_market_df)

    return final_market_df


if __name__ == "__main__":
    df = run_pipeline()
    print("\n PIPELINE EXECUTION COMPLETE! Data safely stored in market_data.db")