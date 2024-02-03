from django.test import TestCase
import requests
import datetime
date = datetime.datetime.now()
curr = str(date.date())
curr = curr.strip()
prev = date - datetime.timedelta(days=10)
prev = str(prev.date()).strip()
print(prev)
name = "036-MDBURLA"
url = f"https://ffs.india-water.gov.in/iam/api/new-entry-data/specification/sorted?sort-criteria=%7B%22sortOrderDtos%22:%5B%7B%22sortDirection%22:%22ASC%22,%22field%22:%22id.dataTime%22%7D%5D%7D&specification=%7B%22where%22:%7B%22where%22:%7B%22where%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.stationCode%22,%22operator%22:%22eq%22,%22value%22:%22{name}%22%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.datatypeCode%22,%22operator%22:%22eq%22,%22value%22:%22HHS%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22dataValue%22,%22operator%22:%22null%22,%22value%22:%22false%22%7D%7D%7D,%22and%22:%7B%22expression%22:%7B%22valueIsRelationField%22:false,%22fieldName%22:%22id.dataTime%22,%22operator%22:%22btn%22,%22value%22:%22{prev}T22:39:53.368,{curr}T22:39:53.368%22%7D%7D%7D"
print(url)
# url = url.split(" ")
# url = url[0] + "T" + url[1]
# print(url)
response = requests.get(url)
print(response.json())

