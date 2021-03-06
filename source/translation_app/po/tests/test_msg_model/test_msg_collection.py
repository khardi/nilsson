import unittest

from start_examples.po.msg_model.msg_collection import MsgCollection
from start_examples.po.msg_model.msg import Msg
from start_examples.po.msg_model.msg_plural import MsgPlural


class TestMsgCollection(unittest.TestCase):

    def test_eq(self):
        msg_collection1 = MsgCollection()
        msg_collection1.add_msg(id='Box', str='Ящик')

        msg_collection2 = MsgCollection()
        msg_collection2.add_msg(id='Box', str='Ящик')

        self.assertEqual(msg_collection1, msg_collection2)

    def test_count(self):
        expected = 1
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')

        result = msg_collection.count

        self.assertEqual(expected, result)

    def test_iter(self):
        box = Msg(id='Box')
        box.str = 'Ящик'
        expected = [box]
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')

        result = [msg for msg in msg_collection.msgs]

        self.assertEqual(expected, result)

    def test_simple_iter(self):
        expected = [
            Msg(id='Fox', str='Лиса'),
            MsgPlural(id='Box', id_plural='Boxes', strs=['Ящик', 'Ящики'])
        ]
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Fox', str='Лиса')
        msg_collection.add_msg_plural(id='Box', id_plural='Boxes', strs=['Ящик', 'Ящики'])

        result = [msg for msg in msg_collection]

        self.assertEqual(expected, result)

    def test_len(self):
        expected = 2
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Fox', str='Лиса')
        msg_collection.add_msg_plural(id='Box', id_plural='Boxes', strs=['Ящик', 'Ящики'])

        result = len(msg_collection)

        self.assertEqual(expected, result)

    def test_put_and_get_single_msg(self):
        expected = 'Ящик'
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')

        result = msg_collection.get_msg('Box').str

        self.assertEqual(expected, result)

    def test_add_msg_with_paths(self):
        expected = [
            '../modules/user/x.js:112',
            '../modules/user/x.js:300'
        ]
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик', paths=[
            '../modules/user/x.js:112',
            '../modules/user/x.js:300'
        ])

        box = msg_collection.get_msg('Box')
        result = [p for p in box.paths]

        self.assertEqual(expected, result)

    def test_add_str_to(self):
        expected = Msg(id='Box', str='Коробка')

        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')
        msg_collection.add_str_to(id='Box', str='Коробка')

        result = msg_collection.get_msg(id='Box')

        self.assertEqual(expected, result)

    def test_put_and_get_plural_msg(self):
        expected = ['Ящик', 'Ящики']
        msg_collection = MsgCollection()
        msg_collection.add_msg_plural(id='Box', id_plural='Boxes', strs=['Ящик', 'Ящики'])

        result = msg_collection.get_msg('Box').strs

        self.assertEqual(expected, result)

    def test_has_msg(self):
        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box')

        result = msg_collection.has_msg('Box')

        self.assertTrue(result)

    def test_add_path_to(self):
        expected = Msg(id='Box', str='Ящик', paths=[
            '../modules/user/x.js:112',
            '../modules/user/x.js:300'
        ])

        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')
        msg_collection.add_path_to(id='Box', path='../modules/user/x.js:112')
        msg_collection.add_path_to(id='Box', path='../modules/user/x.js:300')

        result = msg_collection.get_msg(id='Box')

        self.assertEqual(expected, result)

    def test_remove_msg(self):
        expected = MsgCollection()

        msg_collection = MsgCollection()
        msg_collection.add_msg(id='Box', str='Ящик')
        msg_collection.remove_msg(id='Box')

        result = msg_collection

        self.assertEqual(expected, result)

    def test_create_current_msg(self):
        msg_collection = MsgCollection()
        msg_collection.create_current_msg()

        result = msg_collection.current_msg

        self.assertIsNotNone(result)

    def test_add_path_to_current_msg(self):
        expected = Msg(id='Current', paths=['../modules/user/x.js:112'])
        msg_collection = MsgCollection()
        msg_collection.create_current_msg()
        msg_collection.add_path_to_current_msg(path='../modules/user/x.js:112')

        result = msg_collection.current_msg

        self.assertEqual(expected, result)
