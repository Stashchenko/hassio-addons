## 0.0.7
 
- Fized the DAC-runaway watchdog rest sink in case of pulse audio stuck.

## 0.0.6

- New `extra_clients` option to run additional snapcast clients on the same host. (ex. Bluetooth A2DP sink).
  Scan via `pactl list sinks short`
  ```
  alsa_output.usb-CSCTEK_USB_Audio_and_HID_A34004801402-00.analog-stereo  module-alsa-card.c       s16le 2ch 48000Hz       IDLE
  bluez_sink.D1_37_3B_5A_C6_41.a2dp_sink  module-bluez5-device.c  s16le 2ch 44100Hz       IDLE
  ```
  Thees's what we may add to extra_clients `bluez_sink.D1_37_3B_5A_C6_41.a2dp_sink`

## 0.0.5

- Default buffer 1500 ms

## 0.0.4

- Local snapcast client now waits for the PulseAudio socket before starting, instead of a fixed delay.
- Added a watchdog that detects the outputBufferDacTime runaway (seen on some VM/USB-audio setups where the DAC clock
  wedges,
  spiking CPU with no audio). On detection it resets the PulseAudio sink (suspend/resume, which reopens the ALSA/USB
  device) and restarts the client, so a reboot is no longer needed.
- Added the pulseaudio-utils package to the image to provide pactl for the sink reset above.

## 0.0.2

- Fix avahi advertisement for Snapcast server, no longer publishes bundled to ssh.service/sftp.service
- New `advertise_interfaces` option to restrict the network interfaces to advertise on. If empty, all interfaces will be
  advertised.

## 0.0.1

- Initial version based on the Home Assistant App example. Supports Snapcast v0.35.0 server.
  
