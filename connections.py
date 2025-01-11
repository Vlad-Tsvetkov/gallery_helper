import slack
import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter
from flask import Flask
from contextlib import contextmanager

app = Flask(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)

db_params = {
    'dbname': os.environ['DB_DATABASE'],
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'port': os.environ['DB_PORT']
}


@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        yield conn
    finally:
        if conn:
            conn.close()
