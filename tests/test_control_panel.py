from tests.testcase_creation import make_test_case


class ControlPanelTestCase(
    make_test_case(
        sensor_type="control_panel",
        gpio_return_value={"rain_barrel_threshold": {"state": {"value": 10}},
                           "bed_1_soilMoisture_threshold": {"state": {"value": 50}},
                           "bed_2_soilMoisture_threshold": {"state": {"value": 60}}},
        device_name="control_panel"
    )
):
    pass
