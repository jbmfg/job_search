import requests
import json
import datetime
import dateparser

url = "https://boards-api.greenhouse.io/v1/boards/snyk/departments"
r = requests.get(url)

with open("snyk.json", "w") as f:
    json.dump(r.json(), f)

data = []
today = datetime.datetime.now(datetime.timezone.utc)
for department in r.json()["departments"]:
    team = department["name"]
    for job in department["jobs"]:
        url = job["absolute_url"]
        location = job["location"]["name"]
        title = job["title"]
        posted_datetime = job["updated_at"]
        posted_dt = dateparser.parse(posted_datetime)
        age = (today - posted_dt).days
        data.append([team, url, location, title, age])

data.sort(key=lambda x: x[4], reverse=True)
for row in data:
    team, url, location, title, age = row
    print("*"*30)
    print()
    print(f"{location} - {team} - {title} (posted {age} day(s) ago) {url}")
    print()
print("*"*30)
