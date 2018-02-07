'''
key = '441993aed7c28ccb2511c2d74d31d62a'
user = 'fantomcheg25@gmail.com'
'''
from re import findall
from requests import get


class Scan:

    def __init__(self, domain, query, lr, **kwargs):
        '''
        :param domain: domain search.
        :param query: query in search.
        :param lr: Region in yandex.
        :param kwargs: api_key and user_api.
        '''
        # Domain address, without (www).
        self.domain = domain
        # Query string.
        self.query = query
        # Region id yandex.
        self.lr = lr

        # Simple check for the
        # presence of a parameter.
        if "key" in kwargs and 'user' in kwargs:
            self.key = kwargs['key']
            self.user = kwargs['user']
        else:
            # If there is no data.
            raise KeyError('no information on api')

        # url for access to api.
        self.url = "http://xmlmonster.com/search/xml?" \
                   "query={0}" \
                   "&lr={1}" \
                   "&sortby=rlv" \
                   "&filter=strict" \
                   "&groupby=attr%3Dd.mode%3Ddeep." \
                   "groups-on-page%3D100.docs-in-group%3D1" \
                   "&maxpassages=5" \
                   "&page=0&user={2}" \
                   "&key={3}"
        # property.
        self._data = {}

    def pos(self, data):
        '''
        :param data: array data.
        :return: Position.
        '''

        for i, j in enumerate(data):
            if self.domain.lower() in j.lower():
                # +1 to position
                return i + 1

    @property
    def data(self):
        url = self.url.format(self.query, self.lr,
                              self.user, self.key)
        r = get(url).text
        r = findall(r'<domain>(.+?)</domain>', r)
        temp = [i.replace('www.', '') for i in r]

        self._data = {
            'full': temp,
            'position': self.pos(temp),
        }

        return self._data
