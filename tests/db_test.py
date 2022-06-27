import unittest

from db_service.db_client import DatabaseClient


class TestDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDB, self).__init__(*args, **kwargs)
        self.client = DatabaseClient()

    def test_get(self):
        get_item = self.client.get_box(33)

    def test_boxes(self):
        get_items = self.client.get_boxes()

    def test_create(self):
        create_item = self.client.create_box(
            {
                'id' : 47,
                'name' : 'special',
                'price' : 10,
                'description' : 'tasty and vitamin abundant',
                'category' : 'food',
                'quantity' : 20,
            }
        )

    def test_update(self):
        update_item = self.client.update_box(
            {
                'id' : 30,
                'name' : 'cherry',
                'price' : 10,
                'description' : 'changed',
                'category' : 'food',
                'quantity' : 20,
            }
        )

    def test_delete(self):
        delete_item = self.client.delete_box(44)

    def test_category(self):
        category_items = self.client.getboxes_incategory("food")

    def test_timerange(self):
        timerange_items = self.client.getboxes_intimerange({"seconds": 888888888, "nanos": 345789654}, {"seconds": 999999999, "nanos": 643858364})



if __name__ == '__main__':
    unittest.main()
