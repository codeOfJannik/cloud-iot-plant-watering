from tests.testcase_creation import make_test_case


class WaterValveTestCase(
    make_test_case(
        sensor_type="water_valve",
        gpio_return_value={"id": "valve", "type": "switch", "direction": "input", "state": {"open": True}}
    )
):
    pass

