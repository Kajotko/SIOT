#start a twitter stream for meteoPATH app
import requests, json, re, datetime, os.path, csv,config,loc
from datetime import date
from textblob import TextBlob
from requests_oauthlib import OAuth1
from requests.exceptions import ConnectionError
counts=[0,0,0,0]


###Sentiment analysis by Nikhil Kumar.
###source: 
def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

tday = str(date.today())
print tday
yday=tday
if not os.path.isfile('data_app/'+tday+'_app_tweets.csv'):
    with open('data_app/'+tday+'_app_tweets.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "Pos", "Neg", 'Neu', 'Total'])

city=str(loc.func())
box=loc.box()

key=config.key
secret=config.secret
token=config.token_key
token_secret=config.token_secret

auth = OAuth1(key, secret,token, token_secret)
r=requests.get('https://stream.twitter.com/1.1/statuses/filter.json?locations='+box,stream=True, auth=auth,timeout=5)

prev_date=date = datetime.datetime.now()
epsilon=datetime.timedelta(seconds=5)


for line in r.iter_lines():
    try:
        if line:
            tday = str(date.today())[:10]
            curr_date = datetime.datetime.now()
            if not yday==tday:
                with open('data_app/'+tday+'_app_tweets.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["time", "Pos", "Neg", 'Neu', 'Total'])
            if curr_date-prev_date>epsilon:
                with open('data_app/'+tday+'_app_tweets.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    row=[str(prev_date), str(counts[0]), str(counts[1]),str(counts[2]),str(counts[3])]
                    writer.writerow(row)
                prev_date=curr_date
                print prev_date
                counts = [0, 0, 0, 0]
            decoded_line = line.decode('utf-8')
            print decoded_line
            sentiment=get_tweet_sentiment(json.loads(decoded_line)['text'])
            counts[3] += 1
            if sentiment=='positive':
                counts[0]+=1
            elif sentiment=='negative':
                counts[1] += 1
            else:
                counts[2] += 1
            print city+' Positive ', counts[0], ' Negative: ', counts[1], ' Neutral ', counts[2]
            #if ':)' in json.loads(decoded_line)['text']:
            print(json.loads(decoded_line))['place']['country_code']
            yday=tday
    except KeyError:
        continue
    except ConnectionError:
       continue
    except TypeError:
        continue
    except:
        continue