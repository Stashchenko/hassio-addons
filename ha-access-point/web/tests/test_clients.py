import unittest
from unittest.mock import mock_open, patch

from app import get_clients


class TestGetClients(unittest.TestCase):

    @patch("app.os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_builds_clients(
            self,
            mock_file,
            mock_exists,
    ):
        mock_exists.return_value = True

        mock_file.return_value.__enter__.return_value = [
            "1234567890 14:63:93:6e:96:70 192.168.99.10 laptop *\n",
        ]

        station_data = {
            "14:63:93:6e:96:70": {
                "dbm": -38,
                "percent": 100,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "72.2 MBit/s",
                "connected_time": "1 hour and 15 minutes",
            }
        }

        result = get_clients(station_data)

        self.assertEqual(len(result), 1)

        self.assertEqual(
            result[0],
            {
                "ip": "192.168.99.10",
                "mac": "14:63:93:6e:96:70",
                "hostname": "laptop",
                "signal": "100% (-38 dBm)",
                "percent": 100,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "72.2 MBit/s",
                "connected_time": "1 hour and 15 minutes",
            },
        )

    @patch("app.os.path.exists")
    def test_no_lease_file(self, mock_exists):
        mock_exists.return_value = False

        result = get_clients({})

        self.assertEqual(result, [])

    @patch("app.os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_excludes_disconnected_clients(
            self,
            mock_file,
            mock_exists,
    ):
        mock_exists.return_value = True

        mock_file.return_value.__enter__.return_value = [
            "1234567890 aa:aa:aa:aa:aa:01 192.168.1.10 connected *\n",
            "1234567891 aa:aa:aa:aa:aa:02 192.168.1.11 disconnected *\n",
        ]

        station_data = {
            "aa:aa:aa:aa:aa:01": {
                "dbm": -40,
                "percent": 100,
                "rx_bitrate": "72.2 MBit/s",
                "tx_bitrate": "72.2 MBit/s",
                "connected_time": "5 minutes",
            }
        }

        result = get_clients(station_data)

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0]["mac"],
            "aa:aa:aa:aa:aa:01",
        )

    @patch("app.os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_sorts_by_ip(
            self,
            mock_file,
            mock_exists,
    ):
        mock_exists.return_value = True

        mock_file.return_value.__enter__.return_value = [
            "1 aa:aa:aa:aa:aa:02 192.168.1.20 laptop *\n",
            "2 aa:aa:aa:aa:aa:01 192.168.1.10 phone *\n",
        ]

        station_data = {
            "aa:aa:aa:aa:aa:02": {},
            "aa:aa:aa:aa:aa:01": {},
        }

        result = get_clients(station_data)

        self.assertEqual(
            [client["ip"] for client in result],
            [
                "192.168.1.10",
                "192.168.1.20",
            ],
        )
