import sys

from bs4 import BeautifulSoup as BS
import requests

if len(sys.argv) == 1:
    sys.exit("Need an event id as token")
event_id = sys.argv[1]
if not event_id:
    event_id = "C3609FAB18A44210BC284F3D8EA8A976"
url = f"https://www.fencingtimelive.com/tournaments/eventSchedule/{event_id}"

content = requests.get(url).content

soup = BS(content, 'html.parser')

#table = soup.find("table")
events = soup.find_all(class_="clickable-row")
for event in events:
    print(event['id'])
    print(event.a['href'])
    print(event.a.strong.string.strip())
    print(event.contents)
    
