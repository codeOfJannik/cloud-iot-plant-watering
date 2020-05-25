from software_class.device_software import DeviceSoftware


device_software = DeviceSoftware()
device_software.start_loop(software_function=device_software.run_soil_moisture)


if __name__ == "__main__":
    pass
