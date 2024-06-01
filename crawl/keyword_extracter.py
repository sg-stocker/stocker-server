import os
import json
from openai import OpenAI
import mysql.connector
from collections import defaultdict

db_config = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE')
}
GET_COMPANY_ID_QUERY = os.getenv('GET_COMPANY_ID_QUERY')ㅎ


def get_company_id(cursor, ticker):
    cursor.execute(GET_COMPANY_ID_QUERY, (ticker,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        raise ValueError(f"Company with ticker {ticker} not found")


def create_keyword_entity(cursor, keyword_name, keyword_date, company_id):
    pass


def create_news_entity(cursor, article, keyword_id):
    pass


def process_weekly_data(cursor, ticker, articles):
    company_id = get_company_id(cursor, ticker)
    keyword_name, keyword_date = extract_keyword(articles)
    create_keyword_entity(cursor, keyword_name, keyword_date, company_id)
    keyword_id = cursor.lastrowid
    for article in articles:
        create_news_entity(cursor, article, keyword_id)


cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()

try:
    for subdir in os.listdir(data_folder):
        subdir_path = os.path.join(data_folder, subdir)
        if os.path.isdir(subdir_path):
            ticker = subdir
            for filename in os.listdir(subdir_path):
                filepath = os.path.join(subdir_path, filename)
                with open(filepath, 'r', encoding='utf-8') as file:
                    articles = json.load(file)
                    process_weekly_data(cursor, ticker, articles)
    cnx.commit()
except Exception as e:
    cnx.rollback()
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    cnx.close()
