import unittest
import db


class TestTasks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db.init()

    def test_select(self):
        self.assertEqual(db.get_last_update_index(), 0)

    def test_update(self):
        db.update_last_update_index(10)
        self.assertEqual(db.get_last_update_index(), 10)

    @classmethod
    def tearDownClass(cls):
        db.update_last_update_index(0)

if __name__ == '__main__':
    unittest.main()