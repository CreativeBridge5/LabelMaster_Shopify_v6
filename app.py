import os
import sqlite3
import csv
from flask import Flask, render_template

app = Flask(__name__)

# データベースファイルのパス
DB_PATH = 'database.db'
CSV_PATH = 'uploads/sampleData.csv' # お手元のCSVファイル名に合わせてください

def init_db():
    """テーブル作成とCSVからのデータ取り込み"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. テーブル作成
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip_code TEXT,
            address TEXT,
            company_name TEXT,
            position TEXT,
            name TEXT,
            segment TEXT DEFAULT 'general'
        )
    ''')
    
    # 2. まだデータがなければCSVからインポート
    cursor.execute('SELECT count(*) FROM customers')
    if cursor.fetchone()[0] == 0:
        if os.path.exists(CSV_PATH):
            with open(CSV_PATH, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT INTO customers (zip_code, address, company_name, position, name)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        row.get('郵便番号', ''), 
                        row.get('住所結合', ''), 
                        row.get('会社名', ''), 
                        row.get('役職', ''), 
                        row.get('氏名(敬称)', '')
                    ))
            conn.commit()
    conn.close()

# アプリ起動時に実行
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    customers = cursor.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('index.html', customers=customers)

if __name__ == '__main__':
    app.run(debug=True)
