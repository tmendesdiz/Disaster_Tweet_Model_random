import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


web = 'https://twitter.com/Top_Disaster'
path = './chromedriver/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()
time.sleep(10)

close_notif_button = driver.find_element('xpath','//div[@role="button"]')
close_notif_button.click()


def get_tweet(element):
    try:
        user = element.find_element('xpath',".//span[contains(text(), '@')]").text
        text = element.find_element('xpath','.//div[@lang]').text
        tweets_data = [user, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data

user_data = []
text_data = []
tweet_ids = set()

last_len=None
scrolling = True

# SCROLL AND SCRAPE
while len(user_data)<50:
    if driver.execute_script("return document.body.scrollHeight")!= 0:
        last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//article[@role='article']")))
    #tweets = driver.find_elements('xpath', "//article[@role='article']")
    last_len=len(user_data)
    for tweet in tweets[-5:]:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            text_data.append(" ".join(tweet_list[1].split()))
    print(last_len)
    print(len(user_data))
    if last_len==len(user_data):
        driver.execute_script(f"window.scrollTo(0, 0);")
        time.sleep(1)

driver.quit()


df_tweets = pd.DataFrame({'user': user_data, 'text': text_data})
dict_tweets = df_tweets.to_dict(orient='records')


# PYMONGO
collection_name = 'Scraped_Tweets'
client = pymongo.MongoClient("[CREDENTIALS FOR CLIENT HERE]")
db = client['Cluster0']
db[collection_name].insert_many(dict_tweets)
client.close()









