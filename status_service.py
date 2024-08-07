from flask import Flask, render_template, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from datetime import datetime

DB_NAME = 'pet_kafka_1'
engine = create_engine(f"postgresql+psycopg2://user2:123@localhost:5432/{DB_NAME}")

metadata = MetaData()
task_table = Table(
    'tasks', metadata,
    Column('id', Integer(), primary_key=True),
    Column('hash', String(200), nullable=False),
    Column('name', String(100), nullable=False),
    Column('duration', Integer(), nullable=False),
    Column('status', String(50), default='Created'),
    Column('created_on', DateTime(), default=datetime.now),
    Column('result', String(200))
)

app = Flask(__name__)


@app.route("/status/<hash>")
def status_page(hash):
    s = task_table.select().where(hash==task_table.c.hash)
    with engine.connect() as conn:
        r = conn.execute(s).fetchone()
        return render_template('status.html', hash=hash, name=r.name, status=r.status, result=r.result)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
