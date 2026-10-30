import os
import subprocess
import sys

LOCAL_SERVER = "unix:/run/snapcast-pulse/native.sock"
MASTER_SINK = "host_out"
EQ_SINK = "snapcast_eq"

STATE = "/data/eq.conf"
NUM_BANDS = 10

DEFAULT_BANDS = ["0"] * NUM_BANDS
DEFAULT_GAIN = "0"


class ApplyError(Exception):
    pass


def _pactl(args, check=False):
    env = dict(os.environ, PULSE_SERVER=LOCAL_SERVER)
    return subprocess.run(
        ["pactl", *args],
        text=True,
        capture_output=True,
        env=env,
        check=check,
    )


def _eq_module_ids():
    out = _pactl(["list", "modules", "short"]).stdout
    needle = f"sink_name={EQ_SINK}"
    return [line.split("\t", 1)[0] for line in out.splitlines() if needle in line]


def _unload_sink():
    for module_id in _eq_module_ids():
        _pactl(["unload-module", module_id])


def sink_loaded():
    return bool(_eq_module_ids())


def _snapclient_inputs(sink_index=None):
    out = _pactl(["list", "sink-inputs"]).stdout
    ids = []
    current_id = None
    current_sink = None
    for line in out.splitlines():
        stripped = line.strip()
        if stripped.startswith("Sink Input #"):
            current_id = stripped.split("#", 1)[1].strip()
            current_sink = None
        elif stripped.startswith("Sink:"):
            current_sink = stripped.split(":", 1)[1].strip()
        elif stripped.startswith('application.name = "snapclient"'):
            if current_id is not None and (sink_index is None or current_sink == sink_index):
                ids.append(current_id)
    return ids


def _db_to_raw_volume(gain_db):
    raw = int(65536 * (10 ** (gain_db / 20)))
    return max(raw, 0)


def _validate(bands, gain):
    if isinstance(bands, str):
        bands = [b.strip() for b in bands.split(",")]
    if len(bands) != NUM_BANDS:
        raise ApplyError(f"expected {NUM_BANDS} bands, got {len(bands)}")
    try:
        band_vals = [float(b) for b in bands]
        gain_val = float(gain)
    except (TypeError, ValueError):
        raise ApplyError("bands and gain must be numbers")
    return band_vals, gain_val


def load_state():
    state = {"enabled": False, "bands": list(DEFAULT_BANDS), "gain": DEFAULT_GAIN}
    try:
        with open(STATE, "r") as handle:
            for line in handle:
                key, _, value = line.strip().partition("=")
                if key == "ENABLED":
                    state["enabled"] = value == "1"
                elif key == "BANDS" and value:
                    state["bands"] = [b.strip() for b in value.split(",")]
                elif key == "GAIN" and value:
                    state["gain"] = value
    except OSError:
        pass
    return state


def save_state(enabled, bands, gain):
    if isinstance(bands, (list, tuple)):
        bands = ",".join(str(b) for b in bands)
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as handle:
        handle.write(f"ENABLED={'1' if enabled else '0'}\n")
        handle.write(f"BANDS={bands}\n")
        handle.write(f"GAIN={gain}\n")


def state_for_web():
    state = load_state()
    return {
        "enabled": state["enabled"],
        "bands": state["bands"],
        "gain": state["gain"],
        "active": sink_loaded(),
    }


def apply(enabled, bands, gain):
    band_vals, gain_val = _validate(bands, gain)
    control = ",".join(str(b) for b in bands) if isinstance(bands, (list, tuple)) \
        else ",".join(b.strip() for b in bands.split(","))

    save_state(enabled, control, gain)

    if not enabled:
        _unload_sink()
        return False

    _unload_sink()
    result = _pactl(
        [
            "load-module",
            "module-ladspa-sink",
            f"sink_name={EQ_SINK}",
            f"sink_master={MASTER_SINK}",
            "plugin=caps",
            "label=Eq10",
            f"control={control}",
        ]
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or "pactl returned non-zero"
        raise ApplyError(f"failed to load module-ladspa-sink: {detail}")

    for input_id in _snapclient_inputs():
        _pactl(["move-sink-input", input_id, EQ_SINK])

    _pactl(["set-sink-volume", EQ_SINK, str(_db_to_raw_volume(gain_val))])
    return True


def setup():
    _unload_sink()
    state = load_state()
    if state["enabled"]:
        try:
            if apply(True, state["bands"], state["gain"]):
                control = ",".join(str(b) for b in state["bands"])
                print(
                    f"Equalizer active on '{EQ_SINK}' "
                    f"(bands: {control}, preamp: {state['gain']} dB).",
                    file=sys.stderr,
                )
                print(EQ_SINK)
                return 0
        except ApplyError as err:
            print(
                f"Failed to set up equalizer ({err}); using '{MASTER_SINK}'.",
                file=sys.stderr,
            )
            print(MASTER_SINK)
    return 0


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "setup"
    if command == "setup":
        sys.exit(setup())
    print(f"unknown command '{command}'", file=sys.stderr)
    sys.exit(2)
