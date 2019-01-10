##Collect weathe data for use in app
import requests, time, json, csv, datetime, os.path, config
from datetime import date
from requests.exceptions import ConnectionError
import loc

today = str(date.today())
yesterday=today
if not os.path.isfile('data_app/'+today+'_app_weather.csv'): #add column titles if the data is collected for the first time
    with open('data_app/'+today+'_app_weather.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time", "city", "pressure", 'temperature', 'description'])
city=loc.func()
print city
key=config.weather_key
while True: #keep getting data for each city every 6 seconds
    try:
        r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+key)
        print r.status_code
        desc=r.json()['weather'][0]['description']
        main=r.json()['main']
        print main
        today = str(date.today())
        if yesterday!=today:
            with open('data_app/' + today + '_app_weather.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["time", "city", "pressure", 'temperature', 'description'])
        with open('data_app/'+today+'_app_weather.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile)
                timestamp = str(datetime.datetime.now())
                row=[timestamp,city,str(main['pressure']),str(main['temp']),desc]
                writer.writerow(row)
        #print weather('pressure')
        yesterday=today
        time.sleep(2)

    except ConnectionError:
        continue
    except KeyError:
        continue