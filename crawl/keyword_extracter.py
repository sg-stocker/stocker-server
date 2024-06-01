import os
import json
from openai import OpenAI
import mysql.connector
from collections import defaultdict

OPEN_AI_INSTRUCTION = os.getenv('OPEN_AI_INSTRUCTION')
client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

db_config = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_DATABASE')
}
GET_COMPANY_ID_QUERY = os.getenv('GET_COMPANY_ID_QUERY')
ADD_KEYWORD_QUERY = os.getenv('ADD_KEYWORD_QUERY')
ADD_NEWS_QUERY = os.getenv('ADD_NEWS_QUERY')

script_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(script_dir, 'data')


def get_company_id(cursor, ticker):
    cursor.execute(GET_COMPANY_ID_QUERY, (ticker,))
    result = cursor.fetchone()
    if result is not None:
        return result[0]
    else:
        raise ValueError(f"Company with ticker {ticker} not found")


def extract_keyword(articles):
    headlines = ""
    date_frequency = defaultdict(int)
    for n, article in enumerate(articles):
        headlines += f"{n}. {article['title']}\n"
        date_frequency[article['date']] += 1

    ai_response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": OPEN_AI_INSTRUCTION},
            {"role": "user", "content": headlines}
        ]
    )
    keyword_name = ai_response.choices[0].message.content
    keyword_date = max(date_frequency, key=lambda x: date_frequency[x])

    return keyword_name, keyword_date


def create_keyword_entity(cursor, keyword_name, keyword_date, company_id):
    cursor.execute(ADD_KEYWORD_QUERY, (keyword_name, keyword_date, company_id))


def create_news_entity(cursor, article, keyword_id):
    cursor.execute(ADD_NEWS_QUERY, (article['title'], article['summary'],
                                    article['url'], article['date'],
                                    article['image_url'], keyword_id))


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
