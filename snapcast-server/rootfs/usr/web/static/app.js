const FREQS = ["31", "63", "125", "250", "500", "1k", "2k", "4k", "8k", "16k"];
const bandsEl = document.getElementById("bands");
const sliders = [];

FREQS.forEach((f) => {
    const wrap = document.createElement("div");
    wrap.className = "band";
    const freq = document.createElement("div");
    freq.className = "freq";
    freq.textContent = f;
    const input = document.createElement("input");
    input.type = "range";
    input.min = "-24";
    input.max = "24";
    input.step = "1";
    input.value = "0";
    const val = document.createElement("div");
    val.className = "val";
    val.textContent = "0";
    input.addEventListener("input", () => {
        val.textContent = input.value;
    });
    input.addEventListener("change", apply);
    wrap.append(freq, input, val);
    bandsEl.append(wrap);
    sliders.push({input, val});
});

const enabled = document.getElementById("enabled");
const controls = document.getElementById("controls");
const preamp = document.getElementById("preamp");
const preampVal = document.getElementById("preampVal");
const status = document.getElementById("status");
const warn = document.getElementById("warn");

preamp.addEventListener("input", () => {
    preampVal.textContent = preamp.value;
});
preamp.addEventListener("change", apply);
enabled.addEventListener("change", () => {
    syncDisabled();
    apply();
});

function syncDisabled() {
    controls.disabled = !enabled.checked;
}

function setStatus(text, cls) {
    status.textContent = text;
    status.className = cls || "";
}

async function apply() {
    const bands = sliders.map(s => s.input.value).join(",");
    const gain = preamp.value;
    const en = enabled.checked ? "1" : "0";
    setStatus("Applying…");
    try {
        const r = await fetch(`api/apply?enabled=${en}&bands=${encodeURIComponent(bands)}&gain=${encodeURIComponent(gain)}`);
        const j = await r.json();
        if (j.ok) {
            setStatus("Applied", "ok");
            warn.style.display = "none";
        } else setStatus("Error: " + (j.error || "unknown"), "err");
    } catch (e) {
        setStatus("Request failed", "err");
    }
}

document.getElementById("reset").addEventListener("click", () => {
    sliders.forEach(s => {
        s.input.value = "0";
        s.val.textContent = "0";
    });
    preamp.value = "0";
    preampVal.textContent = "0";
    apply();
});

async function load() {
    try {
        const r = await fetch("api/state");
        const j = await r.json();
        (j.bands || []).forEach((g, i) => {
            if (sliders[i]) {
                sliders[i].input.value = g;
                sliders[i].val.textContent = g;
            }
        });
        if (typeof j.gain !== "undefined") {
            preamp.value = j.gain;
            preampVal.textContent = j.gain;
        }
        enabled.checked = !!j.enabled;
        syncDisabled();
        warn.style.display = (j.enabled && !j.active) ? "block" : "none";
    } catch (e) {
        setStatus("Could not load current settings", "err");
    }
}

void load();
