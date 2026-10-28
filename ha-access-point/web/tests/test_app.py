import unittest
from unittest.mock import patch

from app import app


class TestApp(unittest.TestCase):

    @patch("app.get_clients")
    @patch("app.get_station_signals")
    @patch("app.get_ap_info")
    def test_index_renders_clients(
            self,
            mock_get_ap_info,
            mock_get_station_signals,
            mock_get_clients,
    ):
        mock_get_ap_info.return_value = {
            "ssid": "MyWifi",
            "channel": "6 (2437 MHz)",
        }
        mock_get_station_signals.return_value = {}
        mock_get_clients.return_value = [
            {
                "ip": "192.168.99.10",
                "mac": "14:63:93:6e:96:70",
                "hostname": "device-connected",
                "signal": "100% (-38 dBm)",
                "percent": 100,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "72.2 MBit/s",
                "connected_time": "1 hour and 15 minutes",
            }
        ]

        with app.test_client() as client:
            response = client.get("/")

        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)

        self.assertIn("MyWifi", html)
        self.assertIn("6 (2437 MHz)", html)
        self.assertIn("192.168.99.10", html)
        self.assertIn("14:63:93:6e:96:70", html)
        self.assertIn("device-connected", html)
        self.assertIn("100% (-38 dBm)", html)
        self.assertIn("72.2 MBit/s", html)
        self.assertIn("1 hour and 15 minutes", html)

    @patch("app.get_clients")
    @patch("app.get_station_signals")
    @patch("app.get_ap_info")
    def test_index_renders_empty_state(self, mock_get_ap_info, mock_get_station_signals, mock_get_clients):
        mock_get_ap_info.return_value = {"ssid": "MyWifi", "channel": "6 (2437 MHz)"}
        mock_get_station_signals.return_value = {}
        mock_get_clients.return_value = []

        with app.test_client() as client:
            response = client.get("/")

        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn("No active clients connected.", html)
