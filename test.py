import unittest
from productManager.elements import Element
from productManager.settings import get_database_connection

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("Constructor of the test")
        conn = get_database_connection()
        if conn != None:
            cur = conn.cursor()
            f = open('databases/test.sql', 'r')
            query = f.read()
            for row in query.split(";"):
                if row.strip().replace("\n", "") != "":
                    query = str(row).strip().replace("\n", "") + ";" 
                    cur.execute(query)
                    conn.commit()

    @classmethod
    def tearDownClass(cls):
        print("Destructor of the test")

    def test_add_positive_numbers(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -2), -3)

    def test_add_mixed_numbers(self):
        self.assertEqual(add(1, -2), -1)
        self.assertEqual(add(-1, 2), 1)
    part = Element()
    print(str(part.conn))
if __name__ == '__main__':
    unittest.main()