# -*- coding:utf-8 -*-
import soundcloud


class Jaws(object):
    client = None

    def __init__(self, client_id=''):
        self.client = soundcloud.Client(client_id=client_id)

    def search(self, q):
        return self.client.get('/tracks', q=q)