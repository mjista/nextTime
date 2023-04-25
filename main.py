import requests
import json
import pandas as pd
from datetime import datetime
from geopy.geocoders import Nominatim
import folium
import webbrowser

def req(url):
    response = requests.get(url)
    lat = response.json()['iss_position']['latitude']
    long = response.json()['iss_position']['longitude']
    times = response.json()['timestamp']
    time1 = datetime.fromtimestamp(times)
    global hour
    hour = pd.Timestamp(time1).strftime('%d-%m-%Y, %H:%M:%S')
    coordinate(lat, long)

def coordinate(lat, long):
    locator = Nominatim(user_agent="myGeocoder")
    coordinates = lat, long
    location = locator.reverse(coordinates)
    html = f" <b> La Station Spatiale Internationale(ISS) survole cet endroit :</b> <br>"
    if location:
        address = location.address

        c = folium.Map(location=[lat, long], zoom_start=7)
        iframe = folium.IFrame(html + address + " <br> <b>Le: </b>" + hour.split(',')[0] + "<br> " + "<b> A: </b>" + hour.split(',')[1])
        popup = folium.Popup(iframe,
                             min_width=200,
                             max_width=500)
        folium.Marker([lat, long], popup=popup).add_to(c)
    else:
        c = folium.Map(location=[lat, long], zoom_start=5)
        iframe = folium.IFrame(html + "<br><b>Le : </b>  " + hour.split(',')[0] + "<br> " +" <b> A: </b>" + hour.split(',')[1])
        popup = folium.Popup(iframe,
                             min_width=200,
                             max_width=500)
        folium.Marker([lat, long], popup=popup).add_to(c)
    c.save('carte1.html')
    webbrowser.open_new_tab('carte1.html')


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


if __name__ == '__main__':
    req('http://api.open-notify.org/iss-now.json')
