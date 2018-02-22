# -*- coding: utf-8 -*-
"""This module determines the theme of the site."""
import re
import requests


class SubjectsSite(object):

    shop = r'(корзин|Корзин|cart|Cart)'

    def __init__(self, domain):
        """
        :param domain: Domain web site.
        """

        self.domain = domain

        # Shaping url.
        self.url = 'http://%s/' % domain

        # property.
        self._data = {}

    @property
    def data(self):
        """
        :return: property.
        """

        # Create a query.
        r = requests.get(self.url)

        # Search for entries.
        r = re.findall(self.shop, r.text)

        # Test.
        if 'корзин' in r or 'Корзин' in r or 'cart' in r:
            self._data = {self.domain: 'shop'}
        else:
            self._data = {self.domain: 'service'}

        return self._data
