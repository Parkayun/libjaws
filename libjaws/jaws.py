# -*- coding:utf-8 -*-
import requests
import soundcloud
from bs4 import BeautifulSoup


class Jaws(object):
    client = None

    def __init__(self, client_id=''):
        self.client = soundcloud.Client(client_id=client_id)

    def get_track_meta_data(self, q):
        results = []

        url = 'http://www.melon.com/search/song/index.htm?q=%s&section=&searchGnbYn=Y&ipath=srch_form&ipath=srch_form' % q
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        track_table = soup.find('form', {'id': 'frm_defaultList'})
        track_rows = track_table.findAll('tr')[1:]

        for row in track_rows:
            try:
                data = row.findAll('a', {'class': 'fc_mgray'})
                results.append({
                    'title': row.find('a', {'class': 'fc_gray'}).text,
                    'artist': data[0].text,
                    'album': data[2].text
                })
            except (AttributeError, IndexError):
                pass
        return results

    def search(self, q):
        try:
            return self.client.get('/tracks', q=q)[0]
        except IndexError:
            return None

    def search_stream(self):
        pass

    def search_streams(self, q):
        result = []
        tracks = self.get_track_meta_data(q)
        for track in tracks:
            data = self.search(track['title'] + ' ' + track['artist'])
            if data is not None:
                result.append({
                    'title': track['title'],
                    'artist': track['artist'],
                    'album': track['album'],
                    'uri': data.obj['uri']+'/stream/?client_id='+self.client.client_id
                })
        return result