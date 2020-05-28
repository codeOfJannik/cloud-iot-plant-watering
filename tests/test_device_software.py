from unittest import TestCase, main
from unittest.mock import patch, PropertyMock
from devices.chronos_iot.software_class.device_software import DeviceSoftware


def test_function():
    test_value = 5
    return test_value


class TestDeviceSoftware(TestCase):

    @classmethod
    # set sample env variables
    @patch.dict('os.environ', {'HARDWARE_URL': "http://soilmoisture1_emulator:9292",
                               'DEVICE_NAME': "soilMoisture1_sensor"})
    @patch('devices.chronos_iot.software_class.device_software.super')
    def setUpClass(cls, mock_super):
        print('Create DeviceSoftware class')
        # call class and skip super init
        cls.device_software = DeviceSoftware()

    """----success tests----"""

    # mock publish message function and return True
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.publish_message_to_topic', return_value=True)
    # mock get gpio function and return a fake value
    @patch('devices.chronos_iot.software_class.device_software.get_gpio', return_value={'state': {'value': 50}})
    def test_run_soil_moisture(self, mock_get, mock_publish):
        print('\ntest_run_soil_moisture:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_soil_moisture()
        expected = None  # because abort while loop and no return value is expected (only false if exception)
        self.assertEqual(expected, actual)

    # mock subscribe function and return True
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.subscribe_to_topic', return_value=True)
    # mock set gpio function and return True
    @patch('devices.chronos_iot.software_class.device_software.set_gpio', return_value=True)
    def test_run_water_switch(self, mock_set, mock_subscribe):
        print('\ntest_run_water_switch:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_switch()
        expected = None  # because abort while loop and no return value is expected (only false if exception)
        self.assertEqual(expected, actual)

    """----aws iot client fail tests----"""

    # mock publish message function and simulate failure
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.publish_message_to_topic',
           return_value=False)
    # mock get gpio function and return a fake value
    @patch('devices.chronos_iot.software_class.device_software.get_gpio', return_value={'state': {'value': 50}})
    def test_run_soil_moisture_no_client(self, mock_get, mock_publish):
        print('\ntest_run_soil_moisture_no_IoT_client:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_soil_moisture()
        expected = False
        self.assertEqual(expected, actual)

    # mock subscribe function and simulate failure
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.subscribe_to_topic', return_value=False)
    # mock set gpio function and return True
    @patch('devices.chronos_iot.software_class.device_software.set_gpio', return_value=True)
    def test_run_water_switch_no_client(self, mock_set, mock_subscribe):
        print('\ntest_run_water_switch_no_IoT_client:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_switch()
        expected = False
        self.assertEqual(expected, actual)

    """----gpio request fail tests----"""

    # mock publish message function and return True, but no succeeded gpio request,
    # throw <urlopen error [Errno -2] Name or service not known>
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.publish_message_to_topic', return_value=True)
    def test_run_soil_moisture_no_gpio(self, mock_publish):
        print('\ntest_run_soil_moisture_no_gpio:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_soil_moisture()
        expected = False
        self.assertEqual(expected, actual)

    # mock subscribe function and return False (because callback is False -> no succeeded gpio request)
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.subscribe_to_topic', return_value=False)
    def test_run_water_switch_no_gpio(self, mock_subscribe):
        print('\ntest_run_water_switch_no_gpio:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_switch()
        expected = False
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    main()
