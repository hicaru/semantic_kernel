# -*- coding: utf-8 -*-
'''This module is designed to work with minus words.'''


def sort(sem, minus):
    '''
    :param sem: Generator containing semantics.
    :param minus: Negative array of words.
    :return: Blow-off generator.
    '''

    for i in sem:
        if not i['quiry'] in minus and len(i['quiry']) > 2:
            yield i
