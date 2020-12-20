【インターン準備用】
同ディレクトリ内の「rss-reader.bat」のショートカットを作成してデスクトップに配置して下さい。
そのショートカットをダブルクリックすることで、立ち上げに必要な操作が実行されます。
・サーバ「cgiserver.py」の起動
・Webブラウザの新規タブにてRSSReaderのページ（http://localhost:8000/index.html）を開く


【インターン参加者に試してもらう課題】
●プルダウンにカテゴリを追加すると、対応した情報が新たに検索できることの確認
　手順：
　1. cgi-bin/rss-reader.py を開く
　2. プルダウンを定義している箇所に以下の項目を追加する
　・サイエンス
　・ソフトウェア
　※「<option value=""></option>」を直下にコピペして他の項目を参考に値を設定させる
　
●（予備）実際にコードを書き換えて動きが変わることの確認
　例）18行目の「sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')」を削除してみる
　→標準出力の文字コードのままだと文字化けしてしまうことが分かる


Webアプリ版(Version 1.0)
１．cgiserver.py を実行しサーバを立てる
２．http://localhost:8000/index.htmlにアクセスする
