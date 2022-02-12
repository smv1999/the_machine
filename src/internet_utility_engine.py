from googlesearch import search
import webbrowser
from bs4 import BeautifulSoup
import requests


def search_google(query):
    for item in search(str(query), tld="co.in", num=10, stop=10, pause=2):
        webbrowser.open_new(item)


def get_weather_info(coordinates):
    url = "https://weather.com/en-IN/weather/today/l/{},{}".format(
        coordinates[0], coordinates[1])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    temp = soup.find(
        class_="CurrentConditions--tempValue--3a50n").get_text()
    condition = soup.find(
        class_="CurrentConditions--phraseValue--2Z18W").get_text()
    return temp, condition
