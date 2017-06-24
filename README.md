# aws-billing-notification
AWSの利用料金をSlackに通知するLambda関数です。
Python3で書かれています。

## 参考
[LambdaでAWSの料金を毎日Slackに通知する（Python3） - Qiita](http://qiita.com/tomohiko_isobe/items/88e8e0dcb0ee224a31e4)

## 使い方
リポジトリをクローンしたら必要なモジュールを以下のコマンドでローカルにインストールします。
~~~
pip3 install -r requirements.txt -t ./src/
~~~

インストールしたモジュールごと以下のコマンドでzipファイルに纏めます。
~~~
cd src
zip -r upload.zip *
~~~

完成したzipファイルをLambdaにアップロードし、以下の2つの環境変数を設定して下さい。
- slackWebhookUrl
    - SlackのPOST先のURL
- slackChannel
    - POST先のチャンネル名(例: #aws)