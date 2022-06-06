from email import message
import unittest
from app_a_client import FileMon
from app_b_server import AccessPoint
import copy

FILE_CONTENT = {
  "access_points": [
    {
      "ssid": "MyAP",
      "snr": 63,
      "channel": 111
    },
    {
      "ssid": "YourAP",
      "snr": 42,
      "channel": 11
    },
    {
      "ssid": "HisAP",
      "snr": 54,
      "channel": 66
    }
  ]
}

class TestClient(unittest.TestCase):
    def setUp(self):
        self.f = FileMon()

    def test_check_file_content(self):
        """Check if object is able to load the file content"""
        self.f.file_checker()
        self.assertEqual(self.f.content, FILE_CONTENT)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.access_point = AccessPoint(ssid=FILE_CONTENT['access_points'][0]['ssid'], 
                                snr=FILE_CONTENT['access_points'][0]['snr'], 
                                channel=FILE_CONTENT['access_points'][0]['channel']
                            )

    def test_get_attribute_diff(self):
        """Check if updates in object attribute can be captured"""
        access_point_copy = copy.copy(self.access_point)
        access_point_copy.channel = 123
        message = self.access_point.get_attribute_diff(access_point_copy)
        print(f"Object diff message: {message}")
        self.assertNotEqual(message.find("channel has changed"), -1)
