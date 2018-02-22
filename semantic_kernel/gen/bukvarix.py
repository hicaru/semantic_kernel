'''
The module contains 3 classes.
Class Bukvarix_auto can collect domain semantics.
Class Bukvarix collects semantics in one phrase.
Class BukForm to collect semantics, you can specify words and minus words.
'''
import requests
from re import findall
from yaml import load
from urllib.parse import urlencode


class BukvarixAuto(object):
    """
    This class collects semantics
    automatically, for a given domain.
    """

    # Yandex.
    y_url = "http://www.bukvarix.com/" \
            "site/?q=%s&region=msk&v=table"

    # Google.
    g_url = "http://www.bukvarix.com/site" \
            "/?q=%s&region=gmsk&v=table"

    # This URL is designed to
    # collect semantics by competitors.
    cr = "http://www.bukvarix.com/mcmp/?" \
         "q3=%s+%s+%s+%s&region=msk&v=table"

    @classmethod
    def get(cls, domain, *args, serch='y') -> object:
        """
        :param domain: Domain web site.
        :param args: Parameters for the method cr.
        :param serch: Use yandex and google.
        :return: Generator.
        """

        # Parameter check.
        if serch == 'y':
            url = cls.y_url % domain
        elif serch == 'g':
            url = cls.g_url % domain
        elif serch == 'cr':
            url = cls.cr % args
        else:
            raise TypeError

        # Create a query.
        r = requests.get(url).text

        # This regular degeneration searches for the
        # occurrence of the dictionary, which generates
        # the letters, the parser generates the
        # dictionary in the <script> tag.
        r = findall(
            r'\r\n\t\t(.+?)\r\n\t\t\r\n\r\n\t\t\t\r\n',
            r)[0]

        return cls._parse(r)

    @staticmethod
    def _parse(data: object) -> object:
        """
        :param content: html_content
        :return: dict
        """

        data = "{%s}" % data

        data = load(data)

        for i in data['data']:
            yield dict(quiry=i[0],
                     search_results=i[1],
                     # Responsible for the number of words.
                     Frequency=i[4],
                     Position=i[6])


class Bukvarix(object):

    url = "http://www.bukvarix.com/keywords/?q=%s"

    @classmethod
    def get(cls, query):
        """
        :param query:
        :param dump:
        :return: dict_with_keys(
        frequency_accurate,
        frequency_all_world,
        words_count, quiry,
        symbols_count)
        """
        r = requests.get(cls.url % query)
        href = findall(
            r'<a class="report-download-button"(.+?)</a>',
            r.text
        )[0]

        get_csv = "http://www.bukvarix.com" \
                  "{}".format(
            href.split('"')[1]
        )

        csv_dump = requests.get(
            get_csv
        ).content.decode('utf8')

        csv_dump = csv_dump.replace("\r\n", ";")
        csv_dump = csv_dump.replace('\ufeff"', "")
        csv_dump = csv_dump.replace('"', "")
        csv_dump = csv_dump.split(';')
        [csv_dump.pop(0) for _ in range(5)]  # number_5_the_remove_trash
        return [i for i in cls.__get_dict(csv_dump)]

    @staticmethod
    def __get_dict(dump):
        """
        :type dump: object-(dictionaries)
        :param dump: dump_csv_file
        :yield: dictionaries
        """
        k = 0  # the_variable_is_the_counter
        step = 3  # constant_is_the_iteration_step

        while True:
            try:
                temp = {}
                temp['quiry'] = dump[k]
                k += 1  # stepping
                temp['words_count'] = dump[k]
                k += 1  # stepping
                temp['symbols_count'] = dump[k]
                k += 1  # stepping
                temp['frequency_all_world'] = dump[k]
                k += 1  # stepping
                temp['frequency_accurate'] = dump[k]
                k += step  # stepping_up
                yield temp
            except IndexError:
                break


class BukForm(object):
    """
    The initializer takes 2 arrays (q4, q5).
    The date produces an array with data.
    """

    # Url for POST request.
    url = 'http://www.bukvarix.com/mkeywords/'

    # Pattern for search data.
    p = r'\r\n\t\t"data": (.+?)\r\n\r\n\r\n\t\t\r\n\r\n\t\t\t\r\n   }'

    def __init__(self, q4, q5):
        """
        :param q4: Array query word.
        :param q5: Array minus word.
        """

        # String for valide data.
        query_word = ''
        minus_word = ''

        # The loop a add with string query_word, minus_word.
        # Sign (-) does not support quote.
        for i in q4:
            query_word += i + '-'

        for i in q5:
            minus_word += i + '-'

        # Dict with the meanings of words and minus words.
        self.__slots__ = urlencode({
            'q4': query_word,
            'q5': minus_word,
            'r': 'report',
        }).replace('-', '%0D%0A')

        # property.
        self._data = {}

    @property
    def data(self):
        """
        :return: Array.
        """

        # Open session bukvarix.
        with requests.session() as r:
            content = r.post(self.url, data=self.__slots__)

        # Data string array.
        data = findall(self.p, content.text)

        try:
            return load(data[0])
        except IndexError:
            return None
