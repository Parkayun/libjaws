# -*- coding:utf-8 -*-
import soundcloud


class Jaws(object):
    client = None

    def __init__(self, client_id=''):
        self.client = soundcloud.Client(client_id=client_id)

    def search(self, q):
        return self.client.get('/tracks', q=q)

    def search_streams(self, q):
        result = []
        for idx, track in enumerate(self.search(q)):
            result.append({
                'order': str(idx+1),
                'uri': track.obj['uri']+'/stream/?client_id='+self.client.client_id
            })
        return result