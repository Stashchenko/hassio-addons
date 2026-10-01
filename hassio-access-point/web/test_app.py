import subprocess
import unittest
from unittest.mock import patch

# Updated import to match app.py
from app import app, get_station_signals


class TestGetStationSignals(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.logger.disabled = True

    @classmethod
    def tearDownClass(cls):
        app.logger.disabled = False

    @patch('app.subprocess.check_output')
    def test_get_station_signals_success(self, mock_check_output):
        mock_output = """
Station 14:63:93:6e:96:70 (on wlan0)
    inactive time:  10 ms
    rx bytes:       15200
    tx bytes:       45021
    signal:         -38 dBm
    tx bitrate:     72.2 MBit/s
    rx bitrate:     72.2 MBit/s
    connected time: 4500 seconds
Station e8:f6:0a:89:69:fc (on wlan0)
    inactive time:  20 ms
    signal:         -65 dBm
    tx bitrate:     54.0 MBit/s
    rx bitrate:     24.0 MBit/s
    connected time: 300 seconds
        """
        mock_check_output.return_value = mock_output

        result = get_station_signals("wlan0")

        self.assertIn("14:63:93:6e:96:70", result)
        stats1 = result["14:63:93:6e:96:70"]
        self.assertEqual(stats1["dbm"], -38)
        self.assertEqual(stats1["percent"], 100)
        self.assertEqual(stats1["tx_bitrate"], "72.2 MBit/s")
        self.assertEqual(stats1["rx_bitrate"], "72.2 MBit/s")
        self.assertEqual(stats1["connected_time"], "1 hour and 15 minutes")

        self.assertIn("e8:f6:0a:89:69:fc", result)
        stats2 = result["e8:f6:0a:89:69:fc"]
        self.assertEqual(stats2["dbm"], -65)
        self.assertEqual(stats2["percent"], 70)
        self.assertEqual(stats2["tx_bitrate"], "54.0 MBit/s")
        self.assertEqual(stats2["rx_bitrate"], "24.0 MBit/s")
        self.assertEqual(stats2["connected_time"], "5 minutes")

    @patch('app.subprocess.check_output')
    def test_get_station_signals_command_not_found(self, mock_check_output):
        mock_check_output.side_effect = FileNotFoundError()
        result = get_station_signals("wlan0")
        self.assertEqual(result, {})

    @patch('app.subprocess.check_output')
    def test_get_station_signals_subprocess_error(self, mock_check_output):
        mock_check_output.side_effect = subprocess.SubprocessError("Test Error")
        result = get_station_signals("wlan0")
        self.assertEqual(result, {})

    @patch("app.render_template")
    @patch("app.get_station_signals")
    @patch("app.os.path.exists")
    @patch("builtins.open")
    def test_index_excludes_disconnected_device(self, mock_open, mock_exists, mock_get_station_signals,
                                                mock_render_template):
        mock_exists.return_value = True

        mock_open.return_value.__enter__.return_value = [
            "1234567890 14:63:93:6e:96:70 192.168.99.10 device-connected *\n",
            "1234567891 e8:f6:0a:89:69:fc 192.168.99.11 device-disconnected *\n",
        ]

        mock_get_station_signals.return_value = {
            "14:63:93:6e:96:70": {
                "dbm": -38,
                "percent": 100,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "72.2 MBit/s",
                "connected_time": "1 hour and 15 minutes",
            }
        }

        mock_render_template.return_value = "OK"

        with app.test_client() as client:
            response = client.get("/")

        self.assertEqual(response.status_code, 200)

        mock_render_template.assert_called_once()

        _, kwargs = mock_render_template.call_args

        clients = kwargs["clients"]

        self.assertEqual(len(clients), 1)
        self.assertEqual(clients[0]["mac"], "14:63:93:6e:96:70")
        self.assertEqual(clients[0]["ip"], "192.168.99.10")
        self.assertEqual(clients[0]["hostname"], "device-connected")
        self.assertNotIn("e8:f6:0a:89:69:fc", [client["mac"] for client in clients])


if __name__ == '__main__':
    unittest.main()
