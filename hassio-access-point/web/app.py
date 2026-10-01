import os
import subprocess

import humanize
from flask import Flask, render_template

app = Flask(__name__)

PORT = int(os.environ.get("WEB_PORT", 8080))
LEASES_FILE = "/var/lib/misc/dnsmasq.leases"
INTERFACE = os.environ.get("INTERFACE", "wlan0")


def get_ap_info(interface):
    """Get current AP channel and SSID."""
    info = {"ssid": "N/A", "channel": "N/A"}
    try:
        output = subprocess.check_output(
            ["iw", "dev", interface, "info"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("ssid "):
                info["ssid"] = line.split(" ", 1)[1]
            elif line.startswith("channel "):
                info["channel"] = line.replace("channel ", "")
    except FileNotFoundError:
        app.logger.warning("'iw' command not found")
    except subprocess.SubprocessError as e:
        app.logger.warning(f"Failed to ssid/channel: {e}")
    return info


def get_station_signals(interface):
    """Get detailed wireless metrics for connected clients."""
    stations = {}
    try:
        output = subprocess.check_output(
            ["iw", "dev", interface, "station", "dump"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        current_mac = None
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("Station "):
                current_mac = line.split()[1].lower()
                stations[current_mac] = {
                    "dbm": "N/A", "percent": "N/A",
                    "rx_bitrate": "N/A", "tx_bitrate": "N/A",
                    "connected_time": "N/A"
                }
            elif current_mac:
                if line.startswith("signal:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            dbm = int(parts[1])
                            stations[current_mac]["dbm"] = dbm
                            stations[current_mac]["percent"] = max(0, min(100, int(2 * (dbm + 100))))
                        except ValueError:
                            pass
                elif line.startswith("rx bitrate:"):
                    stations[current_mac]["rx_bitrate"] = line.split(":", 1)[1].strip()
                elif line.startswith("tx bitrate:"):
                    stations[current_mac]["tx_bitrate"] = line.split(":", 1)[1].strip()
                elif line.startswith("connected time:"):
                    try:
                        value = line.split(":", 1)[1].strip()
                        seconds = int(value.split()[0])

                        stations[current_mac]["connected_time"] = humanize.precisedelta(
                            seconds,
                            minimum_unit="minutes",
                            format="%0.0f",
                        )

                    except (ValueError, TypeError):
                        stations[current_mac]["connected_time"] = "N/A"

    except FileNotFoundError:
        app.logger.warning("'iw' command not found")
    except subprocess.SubprocessError as e:
        app.logger.warning(f"Failed to get station signals: {e}")

    return stations


@app.route("/")
def index():
    ap_info = get_ap_info(INTERFACE)
    station_data = get_station_signals(INTERFACE)
    clients = []

    if os.path.exists(LEASES_FILE):
        try:
            with open(LEASES_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 4:
                        continue
                    ip = parts[2]
                    mac = parts[1].lower()
                    hostname = parts[3]

                    if mac not in station_data:
                        continue

                    stats = station_data[mac]
                    signal_display = f"{stats.get('percent', 'N/A')}% ({stats.get('dbm', 'N/A')} dBm)" if stats.get(
                        "dbm") != "N/A" else "N/A"

                    clients.append({
                        "ip": ip,
                        "mac": mac,
                        "hostname": hostname,
                        "signal": signal_display,
                        "percent": stats.get("percent", "N/A"),
                        "rx_bitrate": stats.get("rx_bitrate", "N/A"),
                        "tx_bitrate": stats.get("tx_bitrate", "N/A"),
                        "connected_time": stats.get("connected_time", "N/A")
                    })
        except OSError as e:
            app.logger.warning(f"Failed to read DHCP leases: {e}")

    clients.sort(key=lambda client: tuple(map(int, client["ip"].split("."))))

    return render_template("index.html", clients=clients, ap_info=ap_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
