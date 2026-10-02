# Changelog

## [0.0.6] - 2026-10-02

### Added

- Automatically refresh the client list every 5 seconds.

## [0.0.5] - 2026-10-01

### Changed

- Remove disconnected devices from the UI

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
