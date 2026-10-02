import unittest
from unittest.mock import patch

from app import app


class TestClientApi(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("app.get_clients")
    @patch("app.get_station_signals")
    def test_clients(self, mock_station, mock_clients):
        mock_station.return_value = {
            "aa:bb:cc:dd:ee:ff": {}
        }

        mock_clients.return_value = [
            {
                "ip": "192.168.1.10",
                "mac": "aa:bb:cc:dd:ee:ff",
                "hostname": "laptop",
                "signal": "96% (-52 dBm)",
                "percent": 96,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "144.4 MBit/s",
                "connected_time": "10 minutes",
            }
        ]

        response = self.client.get("/api/v1/clients")

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.get_json(),
            mock_clients.return_value,
        )

        mock_station.assert_called_once()
        mock_clients.assert_called_once_with(
            mock_station.return_value
        )

    @patch("app.get_clients")
    @patch("app.get_station_signals")
    def test_clients_empty(self, mock_station, mock_clients):
        mock_station.return_value = {}
        mock_clients.return_value = []

        response = self.client.get("/api/v1/clients")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])
