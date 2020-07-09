import statr.main as s
import requests
import unittest


class TestWrapper(unittest.TestCase):
    def test_normal_case(self):
        """
        Test with a statuspage.io statuspage.
        """
        result = s.wrapper("https://status.instructure.com")
        self.assertEqual(result, "Canvas is up.")
        
    def test_bad_case(self):
        """
        test it not working....
        """
        self.assertRaises(requests.exceptions.MissingSchema, s.wrapper, "TheKidsCanCallYouHoJu")

if __name__ == '__main__':
    unittest.main()