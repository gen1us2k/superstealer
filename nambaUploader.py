#/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import os
import json

nambaIds = []
mp3count = 0
playlistCount = 1
username = ""
password = ""
session = requests.session()
session.post("http://login.namba.kg/login.php", params={'login': username, 'password': password})
for filename in os.listdir("."):
  if filename.endswith('.mp3'):
    try:
      print "Uploading %s" % filename
      f = open(u'%s'% filename.decode('utf-8'))
      response = session.post("http://api.namba.kg/uploadFile.php", params={u'username': username, u'password': password}, files={u'file': f})
      if response.status_code != 200:
        print "Failed to upload File: %s" % filename
      else:
        print "Uploaded file: %s" % filename
      nambaIds.append(json.loads(response.text)['file_id'])
      mp3count +=1
      if mp3count == 50:
        requestString = ""
        for nambaid in nambaIds:
          requestString += '&mp3[]=%s' % nambaid
        response = session.post("http://namba.kg/api/?service=music&action=save_playlist&service=music&cover=71318491&type=playlist&title=KGSongs%s%s" % (playlistCount, requestString))
        print "Created playlist!!"
        print "Added music to playlist!"
        nambaIds = []
        mp3count = 0
        playlistCount += 1
    except:
      print "Failed to upload file %s" % file
