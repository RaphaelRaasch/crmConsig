import datetime
import re

from dateutil.parser import parse, ParserError


class DataTreatment:

    @staticmethod
    def is_date_type(date) -> datetime.date:
        if type(date) == datetime.date:
            return date
        elif type(date) == datetime.datetime:
            return date.date()

    @classmethod
    def convert_to_date(cls, date, is_dayfirst=False) -> (None, datetime.date):
        is_date_type = DataTreatment.is_date_type(date)
        if not date:
            return None
        elif is_date_type:
            return is_date_type
        try:
            return parse(date, dayfirst=is_dayfirst).date()
        except ParserError:
            return None

    @classmethod
    def date_treatment(cls, date) -> tuple:
        """
        Realiza a manipulação de campo date para retornar um formato de data válido e a ordem do dia/mês.
        :param date: Input de formato data ou string para tratamento
        :return: Retorna tupla com dados formatados e um booleano True caso o dia seja o primeiro número
        """
        is_date_type = DataTreatment.is_date_type(date)
        if not date:
            return None, False
        elif is_date_type:
            return is_date_type, False
        date = re.sub(r"[a-z\W_]", ' ', date)
        date_list = re.findall(r"[\w']+[0-9]+", str(date))
        formatted_date = '/'.join(date_list)
        is_year = int(date_list[-1]) > 31
        is_day_first = True if len(date_list[-1]) == 4 or is_year else False
        return formatted_date, is_day_first

    @classmethod
    def int_treatment(cls, value) -> (int, None):
        if type(value) in frozenset({int, float}):
            return round(value)
        elif not value and value != 0:
            return None
        elif type(value) == bool:
            return None
        list_of_digits = [s for s in value if s.isdigit() or s == '-']
        return int(''.join(list_of_digits)) if list_of_digits else None

    @classmethod
    def bool_treatment(cls, value) -> (bool, None):
        if type(value) == bool:
            return value
        elif not value:
            return None
        treated_value = ''.join([i for i in str(value).replace(' ', '') if i.isalpha()]).capitalize()
        if treated_value in frozenset({'True', 'False'}):
            return True if treated_value == 'True' else False

    @classmethod
    def float_treatment(cls, value) -> (None, float):
        if type(value) in frozenset({int, float}):
            return float(value)
        elif type(value) == bool:
            return None
        elif not value:
            return None
        list_of_digits = [s for s in value if s.isdigit() or s == '.' or s == '-']
        return float(''.join(list_of_digits)) if list_of_digits else None

    @classmethod
    def check_key_in(cls, key, a_dict):
        if type(a_dict) == dict and key in a_dict:
            return a_dict.get(key)
