import datetime

from django.test import TestCase

from data_consig.data_treatment.data_treatment import DataTreatment


# import json


class TestDataTreatment(TestCase):
    # region Testes de função convert date
    def test_convert_to_date_if_none(self):
        self.assertEqual(DataTreatment.convert_to_date(None, True), None)
        self.assertEqual(DataTreatment.convert_to_date(None, False), None)

    def test_convert_to_date_if_date(self):
        self.assertEqual(DataTreatment.convert_to_date('1990/03/22', False), datetime.date(1990, 3, 22))
        self.assertEqual(DataTreatment.convert_to_date('1990-03-22', False), datetime.date(1990, 3, 22))
        self.assertEqual(DataTreatment.convert_to_date('1990.03.22', False), datetime.date(1990, 3, 22))
        self.assertEqual(DataTreatment.convert_to_date('1990 03 22', False), datetime.date(1990, 3, 22))
        self.assertEqual(DataTreatment.convert_to_date('1990 03 22', False), datetime.date(1990, 3, 22))
        self.assertEqual(DataTreatment.convert_to_date('1990/08/03', False), datetime.date(1990, 8, 3))
        self.assertEqual(DataTreatment.convert_to_date('90/08/03', False), datetime.date(1990, 8, 3))
        self.assertEqual(DataTreatment.convert_to_date('03/08/1990', True), datetime.date(1990, 8, 3))
        self.assertEqual(DataTreatment.convert_to_date('03/08/90', True), datetime.date(1990, 8, 3))

    def test_convert_to_date_if_lista(self):
        self.assertEqual(DataTreatment.convert_to_date([], False), None)
        self.assertEqual(DataTreatment.convert_to_date([], True), None)
        self.assertEqual(DataTreatment.convert_to_date({}, False), None)
        self.assertEqual(DataTreatment.convert_to_date({}, True), None)

    # endregion
    # region Teste de função Date treatment
    def test_date_treatment_if_date(self):
        self.assertEqual(DataTreatment.date_treatment('1990 do 08 de 03'), ('1990/08/03', False))
        self.assertEqual(DataTreatment.date_treatment('90 do 08 de 03'), ('90/08/03', False))
        self.assertEqual(DataTreatment.date_treatment('03 de 08 de 1990'), ('03/08/1990', True))
        self.assertEqual(DataTreatment.date_treatment('03 ! 08 # 90'), ('03/08/90', True))

    def test_date_treatment_if_none(self):
        self.assertEqual(DataTreatment.date_treatment(''), (None, False))

    def test_date_treatment_if_datetime(self):
        self.assertEqual(DataTreatment.date_treatment(datetime.date(1990, 8, 3)), (datetime.date(1990, 8, 3), False))
        self.assertEqual(DataTreatment.date_treatment(datetime.datetime(1990, 8, 3, 10, 10, 10)),
                         (datetime.date(1990, 8, 3), False))

    def test_date_treatment_if_list(self):
        self.assertEqual(DataTreatment.date_treatment([]), (None, False))

    # endregion
    # region Teste de função int Treatment
    def test_int_treatment_if_none(self):
        self.assertEqual(DataTreatment.int_treatment(''), None)
        self.assertEqual(DataTreatment.int_treatment(None), None)

    def test_int_treatment_if_numeric(self):
        self.assertEqual(DataTreatment.int_treatment(1.99), 2)
        self.assertEqual(DataTreatment.int_treatment(1), 1)
        self.assertEqual(DataTreatment.int_treatment('string loca'), None)
        self.assertEqual(DataTreatment.int_treatment('123String23Loca'), 12323)
        self.assertEqual(DataTreatment.int_treatment(''), None)
        self.assertEqual(DataTreatment.int_treatment(0), 0)
        self.assertEqual(DataTreatment.int_treatment('0'), 0)
        self.assertEqual(DataTreatment.int_treatment(-10), -10)
        self.assertEqual(DataTreatment.int_treatment('-10'), -10)
        self.assertEqual(DataTreatment.int_treatment(True), None)
        self.assertEqual(DataTreatment.int_treatment(False), None)

    def test_int_treatment_if_lista(self):
        self.assertEqual(DataTreatment.int_treatment([]), None)

    # endregion
    # region Teste de função float treatment
    def test_float_treatment_if_none(self):
        self.assertEqual(DataTreatment.float_treatment(''), None)
        self.assertEqual(DataTreatment.float_treatment(None), None)

    def test_float_treatment_if_numeric(self):
        self.assertEqual(DataTreatment.float_treatment(1.99), 1.99)
        self.assertEqual(DataTreatment.float_treatment(2), 2.0)
        self.assertEqual(DataTreatment.float_treatment('2'), 2.0)
        self.assertEqual(DataTreatment.float_treatment('string123loca'), 123.0)
        self.assertEqual(DataTreatment.float_treatment('.23dsadsd'), .23)
        self.assertEqual(DataTreatment.float_treatment('.0'), .0)
        self.assertEqual(DataTreatment.float_treatment(0), .0)
        self.assertEqual(DataTreatment.float_treatment('0'), .0)
        self.assertEqual(DataTreatment.float_treatment(True), None)
        self.assertEqual(DataTreatment.float_treatment(False), None)

    def test_float_treatment_if_list(self):
        self.assertEqual(DataTreatment.float_treatment([]), None)

    # endregion
    # region Teste de função boolean Treatment
    def test_boolean_treatment_if_none(self):
        self.assertEqual(DataTreatment.bool_treatment(''), None)
        self.assertEqual(DataTreatment.bool_treatment(None), None)

    def test_boolean_treatment_if_numeric(self):
        self.assertEqual(DataTreatment.bool_treatment(123), None)
        self.assertEqual(DataTreatment.bool_treatment(' 1 2 3 '), None)
        self.assertEqual(DataTreatment.bool_treatment(True), True)
        self.assertEqual(DataTreatment.bool_treatment(False), False)
        self.assertEqual(DataTreatment.bool_treatment('False'), False)
        self.assertEqual(DataTreatment.bool_treatment('false'), False)
        self.assertEqual(DataTreatment.bool_treatment('f a l s e'), False)
        self.assertEqual(DataTreatment.bool_treatment('f a 2l 3s 4e'), False)
        self.assertEqual(DataTreatment.bool_treatment('True'), True)
        self.assertEqual(DataTreatment.bool_treatment('true'), True)
        self.assertEqual(DataTreatment.bool_treatment('-true!'), True)
        self.assertEqual(DataTreatment.bool_treatment('-$#!'), None)

    def test_boolean_treatment_if_list(self):
        self.assertEqual(DataTreatment.bool_treatment([]), None)
    # endregion
