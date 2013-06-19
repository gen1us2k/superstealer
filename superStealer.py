# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup

regex = re.compile('<a href="/media/audio/\d+/">.*</a>')
superUrl='http://www.super.kg/media/audio/?pg='
superHost='http://www.super.kg'
urlex = re.compile('<source.*/>')
def grabLinks():
  counter = 1
  hrefs = []
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}
  while counter < 195:
    print "Processing page: %s%s" % (superUrl, counter)
    response = requests.get("%s%s" % (superUrl, counter), headers=headers)
    hrefs += regex.findall(response.text)
    counter += 1
  return hrefs

def grabFile(link):
  print "Parsing page: www.super.kg%s" % link
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}
  response = requests.get("%s%s" % (superHost, link))
  return urlex.findall(response.text)[0].split("\"")[1]

if __name__ == '__main__':
  print "Starting grab links from super.kg/media/audio"
  hrefs = grabLinks()
  f = open('superLinks', 'w+')
  f.write("\n".join(hrefs).encode('utf-8'))
  print "Finished grabbing links from super.kg, results in superLinks file"
  hrefs = open('superLinks').read().splitlines()
  for href in hrefs:
    soup = BeautifulSoup(href)
    url = grabFile(soup.a.get('href'))
    title = soup.a.i.getText()
    artist = soup.a.getText().split(title)[0]
    print "Downloading file.... Artist: %s, Title: %s, url: %s...." %(artist, title.split("\"")[1], url)
    with open('Music/superkg/%s - %s.mp3' % (artist, title.split("\"")[1]), 'wb') as handle:
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}
      request = requests.get(url, headers=headers,  stream=True)
      for block in request.iter_content(1024):
        if not block:
          break
        handle.write(block)

