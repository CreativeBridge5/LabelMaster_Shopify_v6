import sqlite3
import csv

# 1. データベース接続
conn = sqlite3.connect('customer_master.db')
cursor = conn.cursor()

# 2. テーブル作成（既存IDを活かしつつ、ない場合は自動採番できるように設計）
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

# 3. CSVからデータを取り込んで登録
# ファイル名は実際のものに合わせてください
csv_file = 'uploads/sampleData.csv' 

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cursor.execute('''
            INSERT INTO customers (zip_code, address, company_name, position, name)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            row['郵便番号'], 
            row['住所結合'], 
            row['会社名'], 
            row['役職'], 
            row['氏名(敬称)']
        ))

conn.commit()
conn.close()
print("データベースへの移行が完了しました！")
