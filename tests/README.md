# Tests - Software Class
This folder contains the tests that are automatically run by [GitLab CI Runner](https://docs.gitlab.com/runner/) when
new code is pushed to the repository.
The [testcase_creation.py](testcase_creeation.py) contains a function (make_test_case) that returns a test case class based on parameters (sensor_type, gpio_return_value, device_name) passed to the functions.
Each test_*.py file creates a test case for each device type using the make_test_case function.
The [device_software.py](../iot_core/software_class/device_software.py) is tested with the python default package unittest. It tests the behaviour of the class and run methods on success and failure events. The device and the AWS SDK connections are patched with a simulated return value. For more information see in-code comments in the 
[test file](test_soil_moisture_sensors.py) itself.
