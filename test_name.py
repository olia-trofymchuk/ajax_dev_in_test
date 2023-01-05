from unittest import mock
import pytest

from scanner_handler import CheckQr


@pytest.fixture()
def mocked_connection():
    with mock.patch("scanner_handler.CheckQr.check_in_db") as mocker:
        yield mocker


@pytest.fixture()
def mocked_adding_device():
    with mock.patch("scanner_handler.CheckQr.can_add_device") as mocker:
        yield mocker


@pytest.fixture()
def mocked_sending_error():
    with mock.patch("scanner_handler.CheckQr.send_error") as mocker:
        yield mocker


@pytest.mark.parametrize(
    "qr_len, expected_result",
    [
        ("123", "Red"),
        ("12345", "Green"),
        ("1234567", "Fuzzy Wuzzy"),
    ],
)
def test_assign_correct_color_for_qr_in_db(
    mocked_connection, qr_len, expected_result
):
    QR = CheckQr()

    mocked_connection.return_value = True
    QR.check_scanned_device(qr_len)
    assert QR.color == expected_result


@pytest.mark.parametrize(
    "qr_len, expected_result",
    [
        ("1234", None),
        ("123456", None),
        ("12345677898", None),
    ],
)
def test_assign_none_color_for_qr_not_in_db(
    mocked_connection, qr_len, expected_result
):
    QR = CheckQr()

    mocked_connection.return_value = True
    QR.check_scanned_device(qr_len)
    assert QR.color == expected_result


@pytest.mark.parametrize(
    "qr_len",
    [
        "123",
        "12345",
        "1234567",
    ],
)
def test_can_add_device_called_with_correct_message(
    qr_len, mocked_connection, mocked_adding_device
):
    Qr = CheckQr()
    mocked_connection.return_value = True
    Qr.check_scanned_device(qr_len)
    mocked_adding_device.assert_called_once_with(f"hallelujah {qr_len}")


@pytest.mark.parametrize(
    "qr_len",
    [
        "1234",
        "123456",
        "12345678",
    ],
)
def test_sending_errors_for_wrong_length(
    qr_len, mocked_connection, mocked_sending_error
):
    Qr = CheckQr()
    mocked_connection.return_value = True
    Qr.check_scanned_device(qr_len)
    mocked_sending_error.assert_called_once_with(
        f"Error: Wrong qr length {len(qr_len)}"
    )


@pytest.mark.parametrize(
    "qr_len",
    [
        "1234567",
        "123",
        "12345",
    ],
)
def test_sending_errors_for_qr_not_in_db(
    qr_len, mocked_connection, mocked_sending_error
):
    Qr = CheckQr()
    mocked_connection.return_value = None
    Qr.check_scanned_device(qr_len)
    mocked_sending_error.assert_called_once_with("Not in DB")
