from flask import Flask
import tensorflow_hub as hub
import tensorflow as tf
import random
import pymongo
from tensorflow.keras.models import model_from_json


# load json and create model
json_file = open('./model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json, custom_objects={"KerasLayer": hub.KerasLayer})
# load weights into new model
model.load_weights("./model/model.h5")


app = Flask(__name__)

def get_random_tweet():
    client = pymongo.MongoClient("[CREDENTIALS AND CLIENT GO HERE]")
    db = client['Cluster0']
    tweet_db = db.Scraped_Tweets
    tw_list = list(tweet_db.find())
    tw_choice = random.choice(tw_list)
    user = tw_choice.get('user')
    text = tw_choice.get('text')
    client.close()
    return user, text


def pred_tweet(texto, model=model):
    pred = round(model.predict([texto])[0][0])
    return pred
   

@app.route('/')
def index():
    user, text = get_random_tweet()
    pred_value = pred_tweet(text)
    pred = 'IS' if pred_value else 'is NOT'
    return f'''<div>
                    <p>The user:</p>
                    <p> {user}</p> 
                    <p>Tweeted:</p>
                    <p> {text}</p>
                    <p> The prediction is: </p>
                    <p> The tweet {pred} talking about a disaster or catastrophe.</p>
                </div>'''



if __name__ == "__main__":
    app.run(debug=True, host= '0.0.0.0')


