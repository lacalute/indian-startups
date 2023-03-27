


# That isn't working !!!!


import requests
from bs4 import BeautifulSoup
from user_agents import parse

def get_address(key: str):
  global soup
  url = f"https://www.bing.com/search?q={key}"
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
  soup = BeautifulSoup(
      requests.get(url, headers=headers).content, "html.parser"
  )
  nosp = key.replace(" ", "")
  nosp2 = ""
  for j in range(0, len(nosp)):
    if nosp[j].isalpha() == False and nosp[j].isnumeric == False:
      nosp2 = nosp2 + ""
    else:
      nosp2 = nosp2 + nosp[j]
  t = f"www.{nosp2.lower()}"
  t2 = f"https://{nosp2.lower()}"


  for a in soup.findAll('a', {"class": "sh_favicon"}):
    print(a)
    # res = a['href']
    # if t in res or t2 in res:
    #   print(res)

    # else:
    #   print(res)
get_address('UpGrad')