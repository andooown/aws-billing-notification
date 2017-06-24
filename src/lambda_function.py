#!/usr/bin/env python
# encoding: utf-8

import json
import datetime
import requests
import boto3
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数を読み取り
SLACK_POST_URL = os.environ['slackWebhookUrl']
SLACK_CHANNEL = os.environ['slackChannel']

response = boto3.client('cloudwatch', region_name='us-east-1')
# Cloud Watchのメトリクスを取得
get_metric_statistics = response.get_metric_statistics(
    Namespace='AWS/Billing',
    MetricName='EstimatedCharges',
    Dimensions=[
        {
            'Name': 'Currency',
            'Value': 'USD'
        }
    ],
    StartTime=datetime.datetime.today() - datetime.timedelta(days=1),
    EndTime=datetime.datetime.today(),
    Period=86400,
    Statistics=['Maximum'])
# 情報を抽出
cost = get_metric_statistics['Datapoints'][0]['Maximum']    # 料金
date = get_metric_statistics['Datapoints'][0]['Timestamp'].strftime('%Y/%m/%d')    # 日時


def build_message(cost):
    # メッセージの色を判定
    if float(cost) >= 10.0:     # 10 ドル以上の料金が発生
        color = "#ff0000" #red
    elif float(cost) > 0.0:     # 料金が発生
        color = "warning" #yellow
    else:
        color = "good"    #green
    # テキストを作成
    text = "AWS %s: $%s" % (date, cost)
    # メッセージを出力
    return {"text": text, "color": color}


def lambda_handler(event, context):
    # メッセージを作成
    content = build_message(cost)

    # Slack に POST する内容をセット
    slack_message = {
        'channel': SLACK_CHANNEL,
        "attachments": [content],
    }

    # Slack に POST
    try:
        req = requests.post(SLACK_POST_URL, data=json.dumps(slack_message))
        logger.info("Message posted to %s", slack_message['channel'])
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)