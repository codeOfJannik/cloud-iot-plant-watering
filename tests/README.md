# Tests - Software Class
This folder contains the tests that are automatically run by [GitLab CI Runner](https://docs.gitlab.com/runner/) when a 
new stand is uploaded.
For this project, the [device_software.py](../iot_core/software_class/device_software.py) is tested with the python 
default package unittest. It test the behaviour of the class and functions on success and failure events, the device and
the AWS SDK connections are patched with a simulated return value. For more information see in-code comments in the 
[test file](./test_device_software.py) itself.
