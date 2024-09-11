import requests
import json
import datetime
import dateparser

url = "https://boards-api.greenhouse.io/v1/boards/gitlab/departments"
r = requests.get(url)

with open("gitlabs.json", "w") as f:
    json.dump(r.json(), f)

today = datetime.datetime.now(datetime.timezone.utc)
data = []
for department in r.json()["departments"]:
    team = department["name"]
    for job in department["jobs"]:
        title = job["title"]
        location = job["location"]["name"]
        posted_datetime = job["updated_at"]
        posted_dt = dateparser.parse(posted_datetime)
        age = (today - posted_dt).days
        url = job["absolute_url"]
        data.append([location, team, title, age, url])

data.sort(key=lambda x: x[3], reverse=True)
for row in data:
    location, team, title, age, url = row
    print("-" * 30)
    print(f"{location} - {team} - {title} (posted {age} day(s) ago) {url}")
    print()

