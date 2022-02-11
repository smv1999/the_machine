from googlesearch import search
import webbrowser


def search_google(query):
    for item in search(str(query), tld="co.in", num=10, stop=10, pause=2):
        webbrowser.open_new(item)
