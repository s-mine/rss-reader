#!/usr/bin/env python
import cgi
import cgitb
import feedparser

# エラー内容をブラウザに表示x
cgitb.enable()
# RSS取得対象
RSS_URL = "https://gigazine.net/news/rss_2.0/"
# 表示用フォーマット
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
    <h1>GIGAZINE RSSReader</h1>
    <hr>
    <div>
    <form action="/cgi-bin/rss-reader.py" method="POST">
        カテゴリ：
        <select name="category" required>
            <option value=""></option>
            <option value="アート">アート</option>
            <option value="アニメ">アニメ</option>
            <option value="インタビュー">インタビュー</option>
            <option value="ウェブアプリ">ウェブアプリ</option>
            <option value="お知らせ">お知らせ</option>
            <option value="ゲーム">ゲーム</option>
            <option value="コラム">コラム</option>
            <option value="サイエンス">サイエンス</option>
            <option value="セキュリティ">セキュリティ</option>
            <option value="ソフトウェア">ソフトウェア</option>
            <option value="デザイン">デザイン</option>
            <option value="ネットサービス">ネットサービス</option>
            <option value="ハードウェア">ハードウェア</option>
            <option value="ピックアップ">ピックアップ</option>
            <option value="ヘッドライン">ヘッドライン</option>
            <option value="マンガ">マンガ</option>
            <option value="メモ">メモ</option>
            <option value="モバイル">モバイル</option>
            <option value="レビュー">レビュー</option>
            <option value="映画">映画</option>
            <option value="試食">試食</option>
            <option value="取材">取材</option>
            <option value="乗り物">乗り物</option>
            <option value="食">食</option>
            <option value="生き物">生き物</option>
            <option value="動画">動画</option>
        </select>
        <input type="submit" value="取得">
        <input type="button" onclick="location.href='/cgi-bin/rss-reader.py'" value="リセット">
    </form>
    </div>
    <div id="result">
        [[result]]
    </div>
    <div>
        <!-- <input type="button" onclick="location.href='/index.html'" value="TOPへ"> -->
    </div>
</body>
</html>
'''
DISP_STAT = '<b>[[category]]</b>について、<b>[[count]]</b>件の記事が見つかりました。\n\t\t'
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
            count += 1
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

print("Content-Type: text/html")
print(DISP_HTML.replace('[[result]]', result))
