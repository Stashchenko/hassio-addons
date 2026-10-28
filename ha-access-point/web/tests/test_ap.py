import subprocess
import unittest
from unittest.mock import patch

from app import get_ap_info


class TestGetApInfo(unittest.TestCase):

    @patch("app.subprocess.check_output")
    def test_success(self, mock_check_output):
        mock_check_output.return_value = """
        Interface wlan0
            type AP
            channel 6 (2437 MHz)
            ssid MyWifi
        """

        result = get_ap_info("wlan0")

        self.assertEqual(result, {"ssid": "MyWifi", "channel": "6 (2437 MHz)"})
        mock_check_output.assert_called_once_with(["iw", "dev", "wlan0", "info"], text=True, stderr=subprocess.DEVNULL)

    @patch("app.subprocess.check_output")
    def test_command_not_found(self, mock_check_output):
        mock_check_output.side_effect = FileNotFoundError()

        result = get_ap_info("wlan0")
        self.assertEqual(result, {"ssid": "N/A", "channel": "N/A"})

    @patch("app.subprocess.check_output")
    def test_subprocess_error(self, mock_check_output):
        mock_check_output.side_effect = subprocess.SubprocessError("test error")

        result = get_ap_info("wlan0")
        self.assertEqual(result, {"ssid": "N/A", "channel": "N/A"})
