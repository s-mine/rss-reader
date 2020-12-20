#!/usr/bin/env python
# ライブラリの読み込み
import cgi
import cgitb
import io
import sys

import feedparser

# エラー内容をブラウザに表示
cgitb.enable()
# CGI上での標準出力のエンコーディングをUTF-8に設定
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
# RSS取得対象（ローカルデータを使用）
# RSS_URL = 'https://gigazine.net/news/rss_2.0/' 
RSS_URL = './data/gigazine_rss_20201220.xml'
## 表示用フォーマット
# 全体構成用HTML
DISP_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>GIGAZINE RSSReader</title>
    <link rel="icon" type="image/x-icon" href="/image/icon.png">
    <link rel="stylesheet" type="text/css" href="/css/style.css"/>
</head>
<body>
    <a href="../index.html">
        <h1>GIGAZINE RSSReader</h1>
    </a>
    <hr>
    <div>
    <form action="/cgi-bin/rss-reader.py" method="POST">
        カテゴリ：
        <select name="category" required>
            <option value=""></option>
            <option value="ウェブアプリ">ウェブアプリ</option>
            <option value="ゲーム">ゲーム</option>
            <option value="セキュリティ">セキュリティ</option>
            <option value="ネットサービス">ネットサービス</option>
            <option value="ヘッドライン">ヘッドライン</option>
            <option value="メモ">メモ</option>
            <option value="レビュー">レビュー</option>
            <option value="生き物">生き物</option>
        </select>
        <input type="submit" value="取得">
        <input type="button" onclick="location.href='/cgi-bin/rss-reader.py'" value="リセット">
    </form>
    </div>
    <div id="result">
        [[result]]
    </div>
</body>
</html>
'''
# 取得結果の件数表示用HTML
DISP_STAT = '<b>[[category]]</b>について、<b>[[count]]</b>件の記事が見つかりました。\n\t\t'
# 取得結果の詳細表示用HTML
DISP_RESULT = ''' 
<h3><a href="[[link]]"  target="_blank" rel="noopener noreferrer">[[title]]</a>([[categories]])</h3>\n\t\t
<p>[[description]]</p><br>\n\t\t
'''


# RSS取得&整形処理(指定されたカテゴリに一致する記事を取得)
def read_rss_info(param):
    articles = feedparser.parse(RSS_URL)
    ret_rss = DISP_STAT
    count = 0
    for e in articles.entries:
        if len(e.tags) == 0:
            categories = ''
        else:
            categories = e.tags[0]['term'].rstrip(',')

        if param in categories:
            count = count + 1
            ret_rss = ret_rss + DISP_RESULT
            ret_rss = ret_rss.replace('[[link]]', e.link)
            ret_rss = ret_rss.replace('[[title]]', e.title)
            ret_rss = ret_rss.replace('[[categories]]', categories)
            ret_rss = ret_rss.replace('[[description]]', e.description[:e.description.find('<p>')])

    ret_rss = ret_rss.replace('[[category]]', param).replace('[[count]]', str(count))
    return ret_rss


# 画面表示&取得ボタン押下時処理
form = cgi.FieldStorage()
if form:
    category = form.getvalue('category').capitalize()
    result = read_rss_info(category)

else:
    result = ''

print('Content-Type: text/html')
print(DISP_HTML.replace('[[result]]', result))
