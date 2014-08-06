# -*- coding:utf-8 -*-
import requests
import soundcloud
from bs4 import BeautifulSoup


class Jaws(object):
    client = None

    def __init__(self, client_id=''):
        self.client = soundcloud.Client(client_id=client_id)

    def _get_track_row(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        track_table = soup.find('form', {'id': 'frm_defaultList'})
        return track_table.findAll('tr')[1:]

    def get_one_track_data(self, q):
        url = 'http://www.melon.com/search/song/index.htm?q=%s&section=&searchGnbYn=Y&ipath=srch_form&ipath=srch_form' % q

        track_rows = self._get_track_row(url)
        try:
            data = track_rows[0].findAll('a', {'class': 'fc_mgray'})
            result = {
                'title': track_rows[0].find('a', {'class': 'fc_gray'}).text,
                'artist': data[0].text,
                'album': data[2].text
            }
            result['uri'] = self.get_soundcloud_uri(result['title'] + ' ' + result['artist']).obj['uri'] + \
                            '/stream/?client_id='+self.client.client_id
        except (AttributeError, IndexError):
            pass
        return result

    def get_track_meta_data(self, q):
        results = []

        url = 'http://www.melon.com/search/song/index.htm?q=%s&section=&searchGnbYn=Y&ipath=srch_form&ipath=srch_form' % q

        track_rows = self._get_track_row(url)

        for row in track_rows:
            try:
                data = row.findAll('a', {'class': 'fc_mgray'})
                result = {
                    'title': row.find('a', {'class': 'fc_gray'}).text,
                    'artist': data[0].text,
                    'album': data[2].text
                }
                result['uri'] = self.get_soundcloud_uri(result['title'] + ' ' + result['artist']).obj['uri'] + \
                            '/stream/?client_id='+self.client.client_id
                results.append(result)
            except (AttributeError, IndexError):
                pass
        return results

    def get_soundcloud_uri(self, q):
        try:
            return self.client.get('/tracks', q=q)[0]
        except IndexError:
            return None

    def search_stream(self, q):
        return self.get_one_track_data(q)

    def search_streams(self, q):
        result = []
        tracks = self.get_track_meta_data(q)
        for track in tracks:
            data = self.get_soundcloud_uri(track['title'] + ' ' + track['artist'])
            if data is not None:
                result.append({
                    'title': track['title'],
                    'artist': track['artist'],
                    'album': track['album'],
                })
        return result