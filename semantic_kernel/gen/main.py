'''
This module contains the basic logic of working
with the database and the assembly of semantics.
'''
from sql_ import Pattern
from xml_monsrt import Scan
from minus_word import sort
from bukvarix import (Bukvarix_auto, Bukvarix, BukForm)
import json


# A copy of the database operation.
SQL = Pattern()


MINUS_W = [1]


def auto_sem(id):
    '''
    Automatic collection of domain semantics.
    :param id: Project id.
    :param url: Project domain.
    :return: None.
    '''

    url = SQL.select_id(id)

    sem = Bukvarix_auto.get(url)

    minus_word = SQL.select_minus_word(MINUS_W)

    sem = sort(sem, minus_word)

    for i in sem:
        position = {
            "0": {
                "g": "-",
                "y": i['Position']
            }
        }

        SQL.add_from_base(id, i['quiry'],
                          i['Frequency'],
                          json.dumps(position, ensure_ascii=False))


def query_sem(id, query, ko):
    '''
    :param id: Project id.
    :param url: Project domain.
    :param ko: Max count semantics.
    :return: None.
    '''

    position = {
        "0": {
            "g": "-",
            "y": '-'
        }
    }

    # Max range result.
    k = 0

    SQL.delite(id)

    # DB entry.
    for i in Bukvarix.get(query):

        try:
            type(int(i['quiry']))
            continue
        except Exception:
            SQL.add_from_base(id, i['quiry'],
                              i['frequency_all_world'],
                              json.dumps(position,
                                         ensure_ascii=False))
        # This number 300 at max range result.
        if k > ko:
            break

        k += 1


def cr_sem(id, query):
    '''
    Check for the method, this method is
    responsible for collecting semantics by competitors.
    :param id: Project id.
    :param url: Project domain.
    :param query: query string.
    :return: None.
    '''

    # API key for xml_monstr.
    # User for xml_monstr.
    key = ''
    user = ''

    lr = SQL.select_region(id)
    url = SQL.select_id(id)

    # Collects competitors.
    data = Scan(url, query, lr,
                key=key, user=user).data['full']

    sem = Bukvarix_auto.get(url, data[0], data[1],
                            data[2], data[3], serch='cr')

    # Minus words assembly.
    minus_word = SQL.select_minus_word(MINUS_W)

    sem = sort(sem, minus_word)

    # DB entry.
    for i in sem:
        position = {
            "0": {
                "g": "-",
                "y": i['Position']
            }
        }

        SQL.add_from_base(id, i['quiry'], i['Frequency'],
                                json.dumps(position, ensure_ascii=False))


def form_sem(id, array_id):
    '''
    :param id: Project id.
    :param array_id: Array ids minus word.
    :return: None.
    '''

    # Minus word array.
    q5 = SQL.select_minus_word(array_id)

    # Word query.
    q4 = SQL.select_requests(id)

    data = BukForm(q4, q5).data

    # Remove query in BD.
    SQL.delite(id)

    # Enumeration write to the database.
    for i in data:
        position = {
            "0": {
                "g": "-",
                "y": "-"
            }
        }

        SQL.add_from_base(id, i[0], i[3],
                                json.dumps(position, ensure_ascii=False))
