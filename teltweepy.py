# -*- coding: utf-8 -*-

import tweepy
import requests
from bs4 import BeautifulSoup
import openai
import re
import sys
import random
sys.setrecursionlimit(10000)

//Twitter APIキーを設定
consumer_key = "kiLKotlMC3r3RecPEgqnoa1ML"
consumer_secret = "nbKRSFO2hATG6sGEXn82nL6SR7Jne0l6w9LWSdQRI82vtrxfeN"
access_token = "72690686-ppSkeWdfCR7sLmH6nNZyG2xlTpbJeTV4oZwATLt5q"
access_token_secret = "0dkFEOTHGtgSISptH415l2pZwhW9ZnGs2N9Q80hgQUEaH"

# Tweepyを使用してTwitter APIにアクセス
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ブログのURLとカテゴリー（スラッグ）を指定する
url = "https://www.taka-fortune.com/"

# ページのHTMLを取得する
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# 除外するURL
excluded_urls = ["https://www.taka-fortune.com/about", 
                 "https://www.taka-fortune.com/contact", 
                 "https://www.taka-fortune.com/fortune-menu",
                 "https://www.taka-fortune.com/category",
                 "https://www.taka-fortune.com/inquiry",
                 "https://www.taka-fortune.com/taka-fortune-writing-manual",
                 "https://www.taka-fortune.com/profile",
                 "https://www.taka-fortune.com/fortune-telling-ranking-attension",]

# カテゴリーに属するブログ記事のURLを取得する
article_links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href.startswith(url) and href not in excluded_urls:
            article_links.append(href)

# ランダムに記事のURLを選択する
if article_links:
    random_link = random.choice(article_links)
    print(random_link)
    article_url = random_link
else:
    print("記事が見つかりませんでした。")
    

# OpenAI APIキーを設定
openai.api_key = "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"

# 電話占いに関する情報を生成
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "「電話占い」というテーマで、ツイート文章を考えて下さい。日本語で100文字以内でお願いします。"},
    ],
)
info = response.choices[0]["message"]["content"].strip()

# 生成された情報と過去記事のURLをツイート
tweet = f"過去記事：{article_url}\n電話占い情報：{info}"
api.update_status(tweet)
