### [Hass.io Access Point](https://github.com/Stashchenko/hassio-addons/tree/main/hassio-access-point)

A robust Wi-Fi access point add-on designed to connect wireless IoT devices and clients directly to your Home Assistant hardware.

* **Built-in Status Dashboard & Ingress:** Real-time monitoring of connected wireless clients, active IP leases, MAC addresses, and hostnames directly inside the Home Assistant UI via Ingress.
* **Advanced Networking & DHCP:** Integrated `hostapd` and `dnsmasq` stack with optional internet sharing (`MASQUERADE`), custom DNS routing, and mDNS reflection (`Avahi`) for seamless local discovery.
* **Granular Security Controls:** Built-in support for MAC address filtering (`allow_mac_addresses` / `deny_mac_addresses`) and flexible custom configuration overrides.

---

<img src="https://raw.githubusercontent.com/Stashchenko/hassio-addons/main/images/hass-ap/web.png" alt="WebUI" width="100%">

### For developers

To run the unit tests for the signal parsing and backend logic:

```bash
cd hassio-access-point/web

python -m unittest discover -v

# with coverage 
python -m coverage run -m unittest discover -v
python -m coverage report -m
python -m coverage html
```

