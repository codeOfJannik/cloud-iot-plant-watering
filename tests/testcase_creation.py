from unittest import TestCase, main
from unittest.mock import patch, PropertyMock, Mock
from iot_core.software_class.device_software import DeviceSoftware


def make_test_case(sensor_type, gpio_return_value, device_name):
    class TestDeviceSoftware(TestCase):
        @classmethod
        # set sample env variables (in real process set by docker-compose)
        @patch.dict('os.environ', {'HARDWARE_URL': f"http://emulator_{device_name}:9292",
                                   'DEVICE_NAME': device_name})
        # skip super init
        @patch('iot_core.software_class.device_software.super')
        # set, that files exist
        @patch('iot_core.software_class.device_software.DeviceSoftware.cert_files_exist', return_value=True)
        @patch('iot_core.software_class.device_software.DeviceSoftware.read_settings_yaml',
               return_value=(2, 1, sensor_type))
        def setUpClass(cls, settings, files_exist, mock_super):
            print('Create DeviceSoftware class')
            # call class and skip super init
            cls.device_software = DeviceSoftware()

        """----success test----"""
        """tests if functions are run correctly, if all connections have been successfully established"""

        # mock subscribe function and return True
        @patch('iot_core.software_class.aws_iot_client.AWSIoTClient.subscribe_to_topic', return_value=True)
        # mock set gpio function and return True
        @patch('iot_core.software_class.device_software.set_gpio', return_value=True)
        # mock publish message function and return True
        @patch('iot_core.software_class.aws_iot_client.AWSIoTClient.publish_message_to_topic', return_value=True)
        # mock get gpio function and return a fake value
        @patch('iot_core.software_class.device_software.get_gpio',
               return_value=gpio_return_value
               )
        # mock the is_running method to run the loop only once
        @patch('iot_core.software_class.device_software.DeviceSoftware.is_running', side_effect=[True, False])
        def test_run_success(self, mock_running, mock_get, mock_publish, mock_set, mock_subscribe):
            print(f'\ntest run method for {sensor_type} on success when all connections are established')
            # loop for updating sensor values will be run just once cause of mocked is_running method:
            actual = self.device_software.run_device_software()

            # because we abort after loop run once and no return value is expected (returns false only at exceptions)
            expected = None
            self.assertEqual(expected, actual)

        """----aws iot client fail tests----"""
        """tests if the run method returns false, if no AWS IoT client connection is available"""

        # mocking AWSIoTClient is None
        @patch('iot_core.software_class.aws_iot_client.AWSIoTClient', return_value=None)
        # # mock get gpio function and return a fake value
        @patch('iot_core.software_class.device_software.get_gpio',
               return_value=gpio_return_value
               )
        def test_run_no_client(self, mock_get, mock_client):
            print(f'\ntest run method for {sensor_type} with no AWS IoT client:')
            actual = self.device_software.run_device_software()

            expected = False
            self.assertEqual(expected, actual)

        """----gpio request fail tests----"""
        """tests if the run method returns false, if there's no GPIO connection"""

        def test_run_no_gpio(self):
            print(f'\ntest run method for {sensor_type} with no gpio connection:')
            actual = self.device_software.run_device_software()

            expected = False
            self.assertEqual(expected, actual)

    return TestDeviceSoftware


if __name__ == "__main__":
    main()
