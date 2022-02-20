from bs4 import BeautifulSoup
import requests
import json
import datetime

USER_CITY = "Kraków"
escape_rooms = {}
for number in range(0, 10):
    page = requests.get(f"https://lock.me/pl/polska/ranking-escape-room?page={number}&incremental=1").text
    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find_all(name="div", class_="data")
    for er in data:
        name = er.find("a").getText().strip()
        city = er.find("a", class_="city").getText().strip()
        escape_rooms[name] = {
            "Link": "http://lock.me" + er.find("a").get("href"),
            "Rating": er.find("span", class_="full_rating").getText().strip(),
            "City": city,
            "Distance": requests.get(f"https://www.dystans.org/route.json?stops={USER_CITY}|{city}").json()["distances"][0],
        }

visited_er = ["Lokalizacja", "Cicha Noc", "Serce Ozyrysa", "Moriarty sp. z o.o.", "Turniej Magiczny",
              "Sekret Profesora Lipnitzkiego", "Statek kosmiczny - Kamień akumulacyjny 2.0",
              "Świątynia 2.0 - Wynalazek przeszłości", "Plugawy HOTel", "Escape DaVinci", "Statek Piratów",
              "Tajemnica Alchemika", "Upiorny Teatrzyk Lalek", "Psychopata", "Testament", "Seria Niefortunnych Zagadek",
              "Świątynia 2.0 - Wynalazek Tesli"]

for value in list(escape_rooms):
    if (escape_rooms[value]["Distance"] > 120) or (value in visited_er):
        escape_rooms.pop(value)

with open(f'{datetime.date.today()}.json', 'w', encoding='utf-8') as file:
    json.dump(escape_rooms, file, ensure_ascii=False, indent=4)


