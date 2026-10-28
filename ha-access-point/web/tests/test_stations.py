import subprocess
import unittest
from unittest.mock import patch

from app import get_station_signals


class TestGetStationSignals(unittest.TestCase):

    @patch("app.subprocess.check_output")
    def test_success(self, mock_check_output):
        mock_check_output.return_value = """
Station 14:63:93:6e:96:70 (on wlan0)
    signal:         -38 dBm
    tx bitrate:     72.2 MBit/s
    rx bitrate:     72.2 MBit/s
    connected time: 4500 seconds

Station e8:f6:0a:89:69:fc (on wlan0)
    signal:         -65 dBm
    tx bitrate:     54.0 MBit/s
    rx bitrate:     24.0 MBit/s
    connected time: 300 seconds
        """

        mock_check_output.return_value = mock_check_output.return_value

        result = get_station_signals("wlan0")

        self.assertEqual(
            result["14:63:93:6e:96:70"]["dbm"],
            -38,
        )
        self.assertEqual(
            result["14:63:93:6e:96:70"]["percent"],
            100,
        )
        self.assertEqual(
            result["14:63:93:6e:96:70"]["connected_time"],
            "1 hour and 15 minutes",
        )

        self.assertEqual(
            result["e8:f6:0a:89:69:fc"]["dbm"],
            -65,
        )
        self.assertEqual(
            result["e8:f6:0a:89:69:fc"]["percent"],
            70,
        )

    @patch("app.subprocess.check_output")
    def test_command_not_found(self, mock_check_output):
        mock_check_output.side_effect = FileNotFoundError()

        self.assertEqual(
            get_station_signals("wlan0"),
            {},
        )

    @patch("app.subprocess.check_output")
    def test_subprocess_error(self, mock_check_output):
        mock_check_output.side_effect = subprocess.SubprocessError(
            "test error"
        )

        self.assertEqual(
            get_station_signals("wlan0"),
            {},
        )
