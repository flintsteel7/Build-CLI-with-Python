#!/usr/bin/env python

import requests
from pyfancy.pyfancy import pyfancy

url = "https://quotes.rest/qod"

res = requests.get(url)
data = res.json()
if res.status_code == 200:
  quote = data["contents"]["quotes"][0]["quote"]
  author = data["contents"]["quotes"][0]["author"]
  print(pyfancy().green(quote + " - " + author).get())
else:
  print(pyfancy().red(data["error"]["message"]).get())