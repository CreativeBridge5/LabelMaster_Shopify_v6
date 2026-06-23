from flask import Flask, render_template, request, Response
import io
import csv
import re

app = Flask(__name__)

def parse_line(line):
    # 1. 郵便番号抽出
    zip_match = re.search(r'\d{3}-\d{4}', line)
    zip_code = zip_match.group() if zip_match else ""
    
    # 2. 郵便番号以外を処理
    text = line.replace(zip_code, "").strip()
    
    # 3. 住所結合(JP-XX以降の文字を住所と仮定して取得)
    # ※シンプルに「最初の空白まで」を住所とするロジック
    parts = text.split(' ', 1)
    address = parts[0] if len(parts) > 0 else ""
    
    # 4. 残りを会社名/氏名に
    remaining = parts[1] if len(parts) > 1 else ""
    
    # ここで会社名と氏名を分ける（かなり強引ですが、まずはこれで！）
    name_and_company = remaining
    
    return [zip_code, address, "", "", "", name_and_company]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    raw_data = request.form['raw_data']
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['郵便番号', '住所結合', '番地', '会社名', '役職', '氏名(敬称)'])
    
    # 改行コードで強引に分割
    for line in raw_data.replace('\r\n', '\n').split('\n'):
        if line.strip():
            writer.writerow(parse_line(line))
            
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=label_data.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
