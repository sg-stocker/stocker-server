import os
import json
from openai import OpenAI
import mysql.connector
from collections import defaultdict


def process_weekly_data(cursor, ticker, articles):
    pass


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
