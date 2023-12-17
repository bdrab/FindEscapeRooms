import time
import geopy.distance
from bs4 import BeautifulSoup
import requests
import json
import datetime


USER_CITY = "Krakow"
data = requests.get(f"https://geocode.maps.co/search?q={USER_CITY}").json()[0]
cities = {USER_CITY: [float(data["lat"]), float(data["lon"])] }
start_time = time.time()


def distance_between_cities(city):
    distance = geopy.distance.geodesic(cities[USER_CITY], cities[city]).km
    return int(distance)


escape_rooms = {}
for number in range(0, 10):
    page = requests.get(f"https://lock.me/pl/poland/ranking-escape-room?page={number}").text
    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find_all(name="div", class_="data")
    for er in data:
        name = er.find("a").getText().strip()
        er_city = er.find("a", class_="city").getText().strip()

        if er_city not in cities:

            while time.time() - start_time < 1:
                pass

            data = requests.get(f"https://geocode.maps.co/search?q={er_city}").json()[0]
            cities[er_city] = [float(data["lat"]), float(data["lon"])]
            start_time = time.time()

        escape_rooms[name] = {
            "Link": "http://lock.me" + er.find("a").get("href"),
            "Rating": er.find("span", class_="full_rating").getText().strip(),
            "City": er_city,
            "Distance": distance_between_cities(er_city),
        }

visited_er = ["Lokalizacja", "Cicha Noc", "Serce Ozyrysa", "Moriarty sp. z o.o.", "Turniej Magiczny",
              "Sekret Profesora Lipnitzkiego", "Statek kosmiczny - Kamień akumulacyjny 2.0",
              "Świątynia 2.0 - Wynalazek przeszłości", "Plugawy HOTel", "Escape DaVinci", "Statek Piratów",
              "Tajemnica Alchemika", "Upiorny Teatrzyk Lalek", "Psychopata", "Testament", "Seria Niefortunnych Zagadek",
              "Świątynia 2.0 - Wynalazek Tesli", "Niepokój", "Ale Sztuka!", "Kopalnia Złota", "Powstanie Warszawskie"]


for value in list(escape_rooms):
    if (escape_rooms[value]["Distance"] > 120) or (value in visited_er):
        escape_rooms.pop(value)

with open(f'{datetime.date.today()}.json', 'w', encoding='utf-8') as file:
    json.dump(escape_rooms, file, ensure_ascii=False, indent=4)
