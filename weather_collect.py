import requests, time, json, csv, datetime, os.path, config
from datetime import date
from requests.exceptions import ConnectionError

today = str(date.today())
yesterday=today
print today
if not os.path.isfile('data/'+today+'_weather.csv'): #add column titles if the data is collected for the first time
    with open('data/'+today+'_weather.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "city", "pressure", 'temperature', 'descrption'])

cities=['London,uk','New+York,us', 'Tokyo,jp']
key=config.weather_key
print key
while True: #keep getting data for each city every 6 seconds
    for city in cities:
        try:
            r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+key)
            print r.status_code
            desc=r.json()['weather'][0]['description']
            main=r.json()['main']
            print main
            today = str(date.today())
            if yesterday!=today:
                with open('data/' + today + '_weather.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["time", "city", "pressure", 'temperature', 'description'])
            with open('data/'+today+'_weather.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile)
                timestamp = str(datetime.datetime.now())
                row=[timestamp,city[:-3],str(main['pressure']),str(main['temp']),desc]
                writer.writerow(row)
            #print weather('pressure')
            yesterday=today
            time.sleep(2)

        except ConnectionError:
            continue
        except KeyError:
            continue