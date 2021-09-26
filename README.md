# covid19-graph-db2

このリポジトリの使い方はQiitaの記事「[IBM CloudのCodeEngineでDb2 on Cloudを使ったグラフ表示Webサイトの作成](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d)」で説明されています。

CodeEngineではなくLoca環境で動作させたい場合は、以下の手順に従ってkださい。

# Loacalでの動作方法
**想定レベル:** git, node, flaskを使える方を想定しています。

**想定環境:**
Macのコマンドで以下は記載していますが、Windowsでも環境変数設定等を同様のコマンドに変換すれば実施可能です。

## 前提
1. 以下のSWが導入されていることが前提です
    - git
    - node
    - python 

2. Db2 on Cloudのインスタンスとデータ準備
 - [「1. 前準備　Db2 on Cloud」を参照](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#1-%E5%89%8D%E6%BA%96%E5%82%99db2-on-cloud)


## 手順
### 1. ターミナルを開き、git cloneします。
```
git clone https://github.com/kyokonishito/covid19-graph-db2.git
```

最初にreact部分を実行します。

### 2. フロントエンド用のreactのソースが入っている`covid19-graph-db2/frontend`にcdします。
```
cd covid19-graph-db2/frontend
```

### 3. `npm install` して必要なパッケージを導入します。
```
npm install
```

4. `.env`の2行目のコメントを外し、4行目をコメントアウトし、保存します。これはflaskのlocal実行用のendpointを設定しています。
修正前:
```
#For Development
#REACT_APP_API_ENDPOINT=http://localhost:5000
#For Production
REACT_APP_API_ENDPOINT=
```

修正後：
```
#For Development
REACT_APP_API_ENDPOINT=http://localhost:5000
#For Production
#REACT_APP_API_ENDPOINT=
```

### 5. frontend部分のreactを開始します。
```
npm start
```

次に新しいターミナルを開き、Flask部分を実行します。

### 6. flaskモジュールにcdします。
```
cd <git cloneしたディレクトリ>
cd covid19-graph-db2/flask
```
### 7. 必要なライブラリをinstallします。
```
pip install -r requirements.txt
```

### 8. 環境変数のファイルを作成します。
```
cp .env_local_sample .env
```

Db2 on Cloudの接続情報を`.env`ファイルに設定し、保存します。
設定内容は以下です。
取得方法は[こちらの「1.4　Db2 on Cloud接続情報の取得」](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#14db2-on-cloud%E6%8E%A5%E7%B6%9A%E6%83%85%E5%A0%B1%E3%81%AE%E5%8F%96%E5%BE%97)を参照してください。

| 環境変数名 | 値 |  
|----------|------|
|DBNAME|[1.4.1](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#141-%E3%81%BE%E3%81%9A%E3%81%AF%E4%BB%A5%E4%B8%8B%E3%81%AE3%E3%81%A4%E3%82%92%E5%8F%96%E5%BE%97%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84)で取得した`database`の値|
|USERID|[1.4.1](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#141-%E3%81%BE%E3%81%9A%E3%81%AF%E4%BB%A5%E4%B8%8B%E3%81%AE3%E3%81%A4%E3%82%92%E5%8F%96%E5%BE%97%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84)で取得した`username`の値|
|PASSWD|[1.4.1](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#141-%E3%81%BE%E3%81%9A%E3%81%AF%E4%BB%A5%E4%B8%8B%E3%81%AE3%E3%81%A4%E3%82%92%E5%8F%96%E5%BE%97%E3%81%97%E3%81%A6%E3%81%8F%E3%81%A0%E3%81%95%E3%81%84)で取得した`password`の値|
|URL|[1.4.2](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#142-次にrest-api-host-name情報を取得してください)で取得した`REST API host name`の値|
|CRN|[1.4.3](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#143-最後にcrn情報を取得してください)で取得した`CRN情報`の値|
|TABLENAME|[1.2](https://qiita.com/nishikyon/items/1bea871982d38b6ca02d#12-東京都-新型コロナウイルス陽性患者発表詳細テーブルの作成)で取得した`<スキーマ名>.<テーブル名>`の値|

入力例:
```
DBNAME=BLUDB
USERID=xxxxxx
PASSWD=yyyyy
URL=https://zzzzzzzzzz.db2.cloud.ibm.com
CRN=crn:v1:bluemix:public:xxxxxx::
TABLENAME=NISHITO.COVID_19_TOKYO
```

### 9. Flask Local実行用の環境変数をセットします。
```
export FLASK_CONFIG=DEV
```
これによりソースの中でCORS対応を行うようになります。

### 10. Flaskアプリの実行
```
python app.py
```

以上でFlaskアプりが稼働しました。

### 11. Web画面の表示
ブラウザーで以下のURLにアクセスします。
```
http://localhost:3000/
```



# ちょっと変更してみたい人向けのヒント

## 画面
- 画面は[bootswatch](https://bootswatch.com/)を使用しています。スタイルを変更したい場合は[covid19-graph-db2/frontend/src/App.jsx](https://github.com/kyokonishito/covid19-graph-db2/blob/main/frontend/src/App.jsx)の`import "bootswatch/dist/cerulean/bootstrap.min.css";`の`cerulean`を違うテーマ名に変えてみてください。

- グラフは[Chart.jsx](https://github.com/kyokonishito/covid19-graph-db2/blob/main/frontend/src/components/Chart.jsx)で描いています。

## Flaskバックエンド

- [Db2 REST API](https://cloud.ibm.com/apidocs/db2-on-cloud/db2-on-cloud-v4)を使ってDb2にアクセスしてます。

- SQLは[covid19-graph-db2/flaskapp/db2data.py](https://github.com/kyokonishito/covid19-graph-db2/blob/main/flaskapp/db2data.py)の中の`sqlstr`で設定しています。

- [covid19-graph-db2/flaskapp/app.py](https://github.com/kyokonishito/covid19-graph-db2/blob/main/flaskapp/app.py)の`def apply_caching`でLocal用のCORS対応をしています。

## CodeEngineにデプロイする時
- エンドポイントの設定はオリジナルの[covid19-graph-db2/frontend/.env](https://github.com/kyokonishito/covid19-graph-db2/blob/main/frontend/.env)を使用してください。

- githubに[covid19-graph-db2/flaskapp/.env_local_sample](https://github.com/kyokonishito/covid19-graph-db2/blob/main/flaskapp/.env_local_sample)をコピーした.envはアップしないように気を付けてください。オリジナルの[.gitignore](https://github.com/kyokonishito/covid19-graph-db2/blob/main/.gitignore)はアップロードしない様に指定していますので、これを使うようにしてください。