import requests
import json
import datetime
import dateparser

url = "https://cyware.com/api-social/job-openings/usa/"
r = requests.get(url)

with open("cyware.json", "w") as f:
    json.dump(r.json(), f)

today = datetime.datetime.now(datetime.timezone.utc)
data = []
for office in r.json()["offices"]:
    location = office["name"]
    for department in office["departments"]:
        team = department["name"]
        for job in department["jobs"]:
            title = job["title"]
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

