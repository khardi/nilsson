import unittest
from datetime import datetime


class Test(unittest.TestCase):
    def test(self):
        p = Person('Jim')

        self.assertEqual('Jim', p.name)

    def test_can_calculate_nimber_of_kids(self):
        p = Person('Jim')

        p.add_children(Person('Tom'))
        p.add_children(Person('Sonya'))

        self.assertEqual(2, len(p.children))
        self.assertIsInstance(p.children[0], Person)
        self.assertIsInstance(p.children[1], Person)

    def test_birthdate(self):
        p = Person('Jim', birthdate=november(2000, 21))

        self.assertIsNotNone(p.birthdate)
        self.assertEqual(november(2000, 21), p.birthdate)

    def test_incorrect_birthdate(self):
        p = Person('Jim', birthdate=datetime.now())
        with self.assertRaises(ValueError):
            p.how_old()


class Person:
    def __init__(self, name, birthdate=None):
        self.__name = name
        self.__children = []
        self.__birthdate = birthdate

    @property
    def name(self):
        return self.__name

    @property
    def children(self):
        return self.__children

    @property
    def birthdate(self):
        return self.__birthdate

    def add_children(self, children):
        if not isinstance(children, Person):
            raise ValueError('The children is needs subclasses of Person class')
        self.__children.append(children)

    def how_old(self):
        if self._incorrect_birthdate():
            raise ValueError
        return self._number_of_years()

    def _incorrect_birthdate(self):
        return bool(self.birthdate < datetime.now())

    def _number_of_years(self):
        years = datetime.now().year - self.birthdate.year
        if datetime.now().timetuple().tm_yday < self.birthdate.timetuple().tm_yday:
            years -= 1
        return years


def november(year, day):
    return datetime(year=year, month=11, day=day)
