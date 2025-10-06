import sys
import os

from dotenv import load_dotenv

from bs4 import BeautifulSoup as BS
import requests

load_dotenv()

event_id = os.getenv("EVENT_ID")

url = f"https://www.fencingtimelive.com/tournaments/eventSchedule/{event_id}"

content = requests.get(url).content

soup = BS(content, 'html.parser')

#table = soup.find("table")
events = soup.find_all(class_="clickable-row")
for event in events:
    category = event.a.strong.string.strip()
    print(category)
    print(event['id'])
    print(event.a['href'])
#    print(event.contents)

con = requests.get("https://www.fencingtimelive.com/tableaus/scores/BC3F472E57E4409699137062C0AC2595/AA2FEBBBA3124A73B23EEC9304DAF57C").content
soup = BS(con, 'html.parser')
scores = soup.find_all(class_="elimPanel")
print(scores)
