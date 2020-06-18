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

        actual = self.device_software.run_update_data()
        expected = None  # because abort while loop and no return value is expected (only false if exception)
        self.assertEqual(expected, actual)

    # mock subscribe function and return True
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.subscribe_to_topic', return_value=True)
    # mock set gpio function and return True
    @patch('devices.chronos_iot.software_class.device_software.set_gpio', return_value=True)
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient.publish_message_to_topic', return_value=True)
    @patch('devices.chronos_iot.software_class.device_software.get_gpio', return_value={'state': {'open': True}})
    def test_run_water_valve(self, mock_get, mock_publish, mock_set, mock_subscribe):
        print('\ntest_run_water_valve:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_valve()
        expected = None  # because abort while loop and no return value is expected (only false if exception)
        self.assertEqual(expected, actual)

    """----aws iot client fail tests----"""

    # mocking AWSIoTClient is None
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient', return_value=None)
    # # mock get gpio function and return a fake value
    @patch('devices.chronos_iot.software_class.device_software.get_gpio', return_value={'state': {'value': 50}})
    def test_run_soil_moisture_no_client(self, mock_get, mock_update):
        print('\ntest_run_soil_moisture_no_IoT_client:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_update_data()
        expected = False
        self.assertEqual(expected, actual)

    # mocking AWSIoTClient is None
    @patch('devices.chronos_iot.software_class.aws_iot_client.AWSIoTClient', return_value=None)
    @patch('devices.chronos_iot.software_class.device_software.get_gpio', return_value={'state': {'open': True}})
    def test_run_water_valve_no_client(self, mock_get, mock_client):
        print('\ntest_run_water_valve_no_IoT_client:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_valve()
        expected = False
        self.assertEqual(expected, actual)

    """----gpio request fail tests----"""

    def test_run_soil_moisture_no_gpio(self):
        print('\ntest_run_soil_moisture_no_gpio:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_update_data()
        expected = False
        self.assertEqual(expected, actual)

    def test_run_water_valve_no_gpio(self):
        print('\ntest_run_water_valve_no_gpio:')
        # run loop only once:
        sentinel = PropertyMock(side_effect=[1, 0])
        type(self.device_software).running = sentinel

        actual = self.device_software.run_water_valve()
        expected = False
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    main()
