from software_class.device_software import DeviceSoftware
from software_class.policy_topic_reader import *

topic = shorten_topic(get_topic(read_policy("./policy.json")))
device_software = DeviceSoftware()
device_software.run_update_data(topic)


if __name__ == "__main__":
    pass
