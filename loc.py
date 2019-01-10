# Script to find current geolocation for use in app

def func(): #find current city
    import urllib2
    import json
    f = urllib2.urlopen('https://ipinfo.io')
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    l=[]
    for key, val in location.iteritems():
        l.append(key)
    city=location[l[1]]
    return city
def box(): #find bounding box of current area
    import urllib2
    import json
    f = urllib2.urlopen('https://ipinfo.io')
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    l = []
    for key, val in location.iteritems():
        l.append(key)
    coords = location[l[0]]
    lon=float(coords.split(',')[1])
    lat=float(coords.split(',')[0])
    box=str(lon-0.5)+','+str(lat-0.5)+','+str(lon+0.5)+','+str(lat+0.5)
    return box
