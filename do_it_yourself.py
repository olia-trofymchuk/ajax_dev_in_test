FILE = "app_2.log"


def controllers_with_big_handlers(file) -> list[dict[str, str]]:
    """Function which reads file and insert in list all controllers
    with BIG handler
    """
    list_with_big_handler = []

    with open(file, "r") as f:
        for line in f:
            if "BIG" in line:
                line = line.split(";")
                list_with_big_handler.append(
                    {"ID": line[2], "STATE": line[-2]}
                )
    return list_with_big_handler


def controllers_with_invalid_state(
    list_with_big_handler: list[dict[str, str]]
) -> set[str]:
    """Function which takes list with all controllers as parameter
    and insert their id of invalid state in set
    """
    set_with_failed_test = set()

    for line in list_with_big_handler:
        if line["STATE"] == "DD":
            set_with_failed_test.add(line["ID"])

    return set_with_failed_test


def controllers_with_valid_state(
    list_with_big_handler: list[dict[str, str]], set_with_failed_test: set[str]
):
    """Function which takes list with all controllers & set with failed controllers
    as parameters and adds into list all valid controllers & into set id
    of controllers which should be removed
    """
    list_with_success_test = []
    set_with_success_test = set()

    for line in list_with_big_handler:
        if line["ID"] not in set_with_failed_test:
            list_with_success_test.append(line["ID"])
            set_with_success_test.add(line["ID"])

    return list_with_success_test, set_with_success_test


if __name__ == "__main__":
    big_handlers = controllers_with_big_handlers(FILE)
    failed_devices_id = controllers_with_invalid_state(big_handlers)
    all_valid_devices, valid_devices_id = controllers_with_valid_state(
        big_handlers, failed_devices_id
    )

    print(
        f"________________Failed test {len(failed_devices_id)} devices________________"
    )

    for device_id in failed_devices_id:
        print(f"Device {device_id} was removed")

    print(
        f"________________Success test {len(valid_devices_id)} devices________________"
    )

    for device_id in valid_devices_id:
        print(
            f"Device {device_id} sent {all_valid_devices.count(device_id)} statuses"
        )
