import unittest
from finalproj_main import *

class TestData(unittest.TestCase):

    def test_data_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Date FROM Data'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('10/17/15',), result_list)
        self.assertEqual(len(result_list), 20644)

        sql = '''SELECT Time FROM Data WHERE Time LIKE "%AM"'''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 8884)
        self.assertEqual(result_list[1][0], "09:07 AM")
        self.assertEqual(result_list[-1][0], "00:30 AM")
        conn.close()

    def test_crimetype_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''SELECT Type FROM CrimeType'''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Vandalism',), result_list)
        self.assertEqual(len(result_list), 9)

        sql = '''
            SELECT Data.Name, CrimeType.Type
            FROM Data JOIN CrimeType ON Data.CrimeId = CrimeType.Id'''
        results = cur.execute(sql)
        count = results.fetchall()
        self.assertEqual(count[0][0], count[0][1])

        conn.close()

    def test_data_processing(self):
        crime_frequency()
        self.assertIn('Theft', crime_frequency())
        self.assertEqual(len(crime_frequency()), 9)
        self.assertEqual(crime_frequency()['Arson'], 36)
        crime_locations()
        self.assertIn('WASHTENAW', crime_locations())
        self.assertEqual(crime_locations()['STADIUM'], 345)
        self.assertEqual(len(crime_locations()), 1230)
        self.assertNotIn('ANN ARBOR', crime_locations())

    def test_data_processing2(self):
        crime_time()
        self.assertEqual(crime_time()['2PM'], 987)
        self.assertEqual(len(crime_time()),24)
        crime_over_time()
        self.assertEqual(crime_over_time()['2017'], 3548)
        self.assertEqual(len(crime_over_time()), 9)
        self.assertNotIn('2019', crime_over_time())

unittest.main()
