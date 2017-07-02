import unittest
from datetime import datetime


class Test(unittest.TestCase):
    def test(self):
        p = Person('Jim')

        self.assertEqual('Jim', p.name)

    def test_add_one_children(self):
        p = Person('Jim')

        p.add_children(Person('Tom'))

        self.assertEqual(1, len(p.children))
        self.assertIsInstance(p.children[0], Person)


class Person:
    def __init__(self, name):
        self.__name = name
        self.__children = []
        self.__children = []
        self.birthdate = datetime.now()

    @property
    def name(self):
        return self.__name

    @property
    def children(self):
        return self.__children

    def add_children(self, children):
        if not isinstance(children, Person):
            raise ValueError('The children is needs subclasses of Person class')
        self.__children.append(children)

    def how_old(self):
        if self.birthdate < datetime.now():
            years = datetime.now().year - self.birthdate.year
            if datetime.now().timetuple().tm_yday < self.birthdate.timetuple().tm_yday:
                years -= 1
            return years
        else:
            return 0