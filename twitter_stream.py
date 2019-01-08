import requests, json, re, datetime, os.path, csv,config
from datetime import date
from textblob import TextBlob
from requests_oauthlib import OAuth1
from requests.exceptions import ConnectionError
counts={'GB':[0,0,0,0], 'US':[0,0,0,0],'JP':[0,0,0,0]}


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
if not os.path.isfile('data/'+tday+'_tweets.csv'):
    with open('data/'+tday+'_tweets.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "GB_Pos", "GB_Neg", 'GB_Neu', 'GB_Total', "US_Pos", "US_Neg", 'US_Neu', 'US_Total',"JP_Pos", "JP_Neg", 'JP_Neu', 'JP_Total'])

coords={'London':'-0.428467,51.342623,0.211487,51.629952','NYC':'-74,40,-73,41','Tokyo':'139.574432,35.496456,140.005646,35.789969'}

key=config.key
secret=config.secret
token=config.token_key
token_secret=config.token_secret

auth = OAuth1(key, secret,token, token_secret)
r=requests.get('https://stream.twitter.com/1.1/statuses/filter.json?locations='+coords['NYC']+'&locations='+coords['Tokyo']+'&locations='+coords['London'],stream=True, auth=auth,timeout=5)

prev_date=date = datetime.datetime.now()
epsilon=datetime.timedelta(seconds=5)


for line in r.iter_lines():
    try:
        if line:
            tday = str(date.today())[:10]
            curr_date = datetime.datetime.now()
            if not yday==tday:
                with open('data/'+ tday +'_tweets.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["time", "GB_Pos", "GB_Neg", 'GB_Neu', 'GB_Total', "US_Pos", "US_Neg", 'US_Neu', 'US_Total',"JP_Pos", "JP_Neg", 'JP_Neu', 'JP_Total'])
            if curr_date-prev_date>epsilon:
                with open('data/'+tday+'_tweets.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([str(prev_date), str(counts['GB'][0]), str(counts['GB'][1]),str(counts['GB'][2]),str(counts['GB'][3]),str(counts['US'][0]),str(counts['US'][1]),str(counts['US'][2]),str(counts['US'][3]), str(counts['JP'][0]),str(counts['JP'][1]),str(counts['JP'][2]),str(counts['JP'][3])])
                prev_date=curr_date
                print prev_date
                counts = {'GB': [0, 0, 0, 0], 'US': [0, 0, 0, 0], 'JP': [0, 0, 0, 0]}
            decoded_line = line.decode('utf-8')
            print decoded_line
            sentiment=get_tweet_sentiment(json.loads(decoded_line)['text'])
            key = (json.loads(decoded_line))['place']['country_code']
            counts[key][3] += 1
            if sentiment=='positive':
                counts[key][0]+=1
            elif sentiment=='negative':
                counts[key][1] += 1
            else:
                counts[key][2] += 1
            print 'Country '+key+' Positive ', counts[key][0], ' Negative: ', counts[key][1], ' Neutral ', counts[key][2]
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