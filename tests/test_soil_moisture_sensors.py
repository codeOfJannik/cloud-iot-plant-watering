from tests.testcase_creation import make_test_case


class SoilMoistureSensorTestCase(
    make_test_case(
        sensor_type="soil_moisture",
        gpio_return_value={'state': {'value': 50}},
        device_name="soilMoisture1_sensor"
    )
):
    pass

