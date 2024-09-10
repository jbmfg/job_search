import requests
import json
from math import ceil

url = "https://crowdstrike.wd5.myworkdayjobs.com/wday/cxs/crowdstrike/crowdstrikecareers/jobs"
pd = {
    "appliedFacets":{
        "locationCountry":["bc33aa3152ec42d4995f4791a106ed09"],
        "locations":["20feac86ebdd0102586dc95b42138d6f"]},
    "limit":20,
    "offset":0,
    "searchText":""
}
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US",
    "Cache-Control": "no-cache",
    "Origin": "https://crowdstrike.wd5.myworkdayjobs.com"
}
r = requests.post(url, json=pd, headers=headers)
total = r.json()["total"]

x = 0
pages = ceil(total / 20)
results = []
for _ in range(pages):
    r = requests.post(url, json=pd, headers=headers)
    results += r.json()["jobPostings"]
    pd["offset"] += 20
    print(pd["offset"])

with open("crowdstrike.json", "w") as f:
    json.dump(results, f)

sorted_jobs = []

for i in results:
    post_date = i["postedOn"].split("Posted ")[1].split(" Days Ago")[0]
    if post_date == "Yesterday":
        post_date = "1"
    if post_date == "Today":
        post_date = "0"
    elif "+" in post_date:
        post_date = post_date.strip("+")
    i["age"] = post_date

results.sort(key=lambda x: int(x["age"]), reverse=True)

for i in results:
    print("-" * 30)
    print(i["title"])
    print(i["age"])
    print(f"https://crowdstrike.wd5.myworkdayjobs.com/en-US/crowdstrikecareers{i['externalPath']}")
    print()
