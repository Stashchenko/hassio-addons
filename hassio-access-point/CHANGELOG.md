# Changelog

## [0.0.5] - 2026-09-30

### Changed

- Inbound-NAT/forwarding rules are now added idempotently (with -C checks), so they no longer accumulate as duplicates
  on every add-on restart.

- Explicit AP -> LAN return rule for established connections, so reaching AP devices from the LAN (e.g. ESPHome OTA)
  works even with `client_internet_access`
  disabled. Combine with a static route `192.168.99.0/24 -> <this host>` on your LAN router (or client) so LAN devices
  can route to AP addresses.
- New optional `default_route_interface` option to override the auto-detected upstream interface.

- Fixed the legacy integer-to-boolean config migration loop, which only ever processed the first option and referenced
  an unset variable.
- Default-route auto-detection now takes only the first default route.

## [0.0.4] - 2026-09-28

### Added

- Added Ukrainian language translations (`translations/uk.json`).

## [0.0.3] - 2026-09-27

### Added

- Added color-coded signal strength badges and dBm indicators to the web UI.
- Added detailed Tx/Rx rate breakdowns (including MCS index and short GI details) alongside client uptime metrics.
- Added comprehensive unit test suite for status parsing and subprocess error handling (`test_app.py`).
- Added robust error handling and fallback behaviors for missing `iw` commands or subprocess exceptions.
- Added support for auto mode.

### Changed

- Renamed backend module from `status.py` to `app.py` for improved structure.

## [0.0.2] - 2026-09-26

### Added

- Added signal strength to the web UI.

## [0.0.1] - 2026-09-26

- First release.
