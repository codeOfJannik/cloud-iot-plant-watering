from tests.testcase_creation import make_test_case


class RainBarrelSensorTestCase(
    make_test_case(
        sensor_type="rain_barrel",
        gpio_return_value={'state': {'value': 50}},
        device_name="rain_barrel_sensor"
    )
):
    pass
