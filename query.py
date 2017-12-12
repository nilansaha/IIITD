from pymongo import MongoClient
import pandas as pd
from textblob import TextBlob
import sys
from plotly.offline import plot
from plotly.graph_objs import Bar, Pie
reload(sys)
sys.setdefaultencoding('UTF8')

client = MongoClient('localhost:27017')
db = client.IIITD

neutral = 0
positive = 0
negative = 0
my_plot_div = ""
retweetspie = ""
users = ""
sentimentbar = ""


def sentimentscore(text):
    global neutral, positive, negative
    text = TextBlob(text)
    if text.sentiment.polarity == 0:
        neutral = neutral + 1
    elif text.sentiment.polarity > 0:
        positive = positive + 1
    elif text.sentiment.polarity < 0:
        negative = negative + 1


def datainit(collection):
    if collection=="delhi":
        dbs = db.delhi
    elif collection=="mumbai":
        dbs = db.mumbai
    global my_plot_div, retweetspie, users, sentimentbar
    hashtags = []
    users = []
    for document in dbs.find():
        sentimentscore(document['text'])
        for x in document['entities']['hashtags']:
            hashtags.append(x['text'])
        users.append(document['user']['screen_name'])

    hashtags = pd.Series(hashtags)
    #print hashtags
    hashtags=hashtags[hashtags != 'nan'].value_counts().iloc[:5].to_frame().reset_index()
    hashtags.columns = ['Hashtags','Count']
    print hashtags

    users=pd.Series(users)
    users = users[users!='nan'].value_counts().iloc[:10].to_frame().reset_index()
    users.columns = ['Users','Count']


    retweets = dbs.find({"text" : {'$regex': 'RT @'}}).count();
    totaltweets = dbs.find().count();
    original = int(totaltweets) - int(retweets)
    print retweets

    print neutral,positive,negative

    my_plot_div = plot([Bar(x=hashtags.Hashtags,
        y=hashtags.Count,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))], output_type='div', config = {'showLink':False,'displayModeBar':False})

    retweetspie = plot([Pie(labels=['Original Tweets','Retweets'],values = [original, retweets],
    marker=dict(colors=['rgb(158,202,225)','rgba(241,129,100,0.7)'],line=dict(
        color='rgb(8,48,107)',
        width=1.5,
    )))],output_type='div', config = {'showLink':False,'displayModeBar':False})


    users = plot([Bar(x=users.Count,
        y=users.Users,orientation='h',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))], output_type='div', config = {'showLink':False,'displayModeBar':False})


    sentimentbar = plot([Bar(x=['Neutral','Positive','Negative'],
        y=[neutral, positive, negative],
        marker=dict(
            color=['rgb(158,202,225)','rgba(50,171,96,0.7)','rgba(219,64,82,0.7)'],
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ))], output_type='div', config = {'showLink':False,'displayModeBar':False})
    return [my_plot_div,retweetspie,users,sentimentbar]


# print hashtags.columns[0]
# print hashtags.columns[1]
