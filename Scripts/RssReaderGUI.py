import feedparser
import time
import tkinter as tk


# RSS取得処理(指定されたカテゴリに一致する記事を取得)
def read_RSS_info(param):
    RSS_URL = "https://gigazine.net/news/rss_2.0/"
    articles = feedparser.parse(RSS_URL)

    rss = []
    count = 0
    for e in articles.entries:
        if len(e.tags) == 0:
            categories = ''
        else:
            categories = e.tags[0]['term'].rstrip(',')

        if param in categories:
            count = count + 1
            rss.append(
                '[' + str(count) + ']\n' + time.strftime('%Y/%m/%d %H:%M:%S', e.updated_parsed)  + '\n'
                + e.title + '(' + categories + ')\n' + e.description[:e.description.find('<p>')] + '\n' + e.link + '\n'
                )
    return rss


def main():
    # メインウィンドウ作成
    root = tk.Tk()
    root.geometry("640x480")
    root.title("GIGAZINE RSS取得")

    def SearchValue(event):
        rss = []
        value = serchBox.get()
        rss = read_RSS_info(value)
        resultBox.delete('1.0', tk.END)

        for r in rss:
            resultBox.insert(tk.END, r + '\n')

    # タイトルラベル
    titleLbl = tk.Label(text='GIGAZINE RSS取得ツール', foreground='#4682b4',font=("",20))
    titleLbl.place(x=40, y=10)

    # 入力エントリー
    serchBox = tk.Entry()
    serchBox.pack()
    serchBox.place(x=210, y=50)

    # 出力エントリー
    resultBox = tk.Text(width=80, height=25)
    resultBox.pack(side=tk.TOP)
    resultBox.place(x=40, y=100)

    # 取得ボタン
    getBtn = tk.Button(text='取得', width=10)
    getBtn.bind("<Button-1>", SearchValue)
    # 左クリック（<Button-1>）されると，SearchValue関数を呼び出すようにバインド
    getBtn.pack()
    getBtn.place(x=340, y=50)

    root.mainloop()


if __name__ == "__main__":
    main()
