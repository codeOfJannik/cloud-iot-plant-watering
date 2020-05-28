from unittest import TestCase
from unittest.mock import patch, PropertyMock, MagicMock
from io import StringIO
from devices.chronos_iot.software_class.device_software import DeviceSoftware


def test_function():
    test_value = 5
    return test_value


class TestDeviceSoftware(TestCase):

    # set sample env variables
    @patch.dict('os.environ', {'HARDWARE_URL': "http://soilmoisture1_emulator:9292",
                               'DEVICE_NAME': "soilMoisture1_sensor"})
    @patch('devices.chronos_iot.software_class.device_software.super')
    def setUp(self, mock_super) -> None:
        # call class and skip super init
        self.device_software = DeviceSoftware()

    @patch('devices.chronos_iot.software_class.device_software.urllib.request.urlopen')
    def test_run_soil_moisture_fail(self, mock_urlopen):
        # cm = MagicMock()
        # cm.getcode.return_value = 200
        # cm.read.return_value = 'contents'
        mock_urlopen.status.return_value = 200
        mock_urlopen.read.return_value = 'content'
        mock_urlopen.__enter__.return_value = mock_urlopen.status
        actual = self.device_software.run_soil_moisture()
        expected = False
        self.assertEqual(expected, actual)

    # def test_run_water_switch(self):
    #     self.device_software.run_water_switch()
