"""Audio rendering helpers for jazz rhythm studies."""

from __future__ import annotations

import math
from pathlib import Path
import random
import tempfile
import wave
from array import array

from audio_rendering import normalize_wav
import mido


def _make_clap_sample(sample_rate: int) -> array:
    """Create a short synthetic hand-clap sample."""
    duration = 0.18
    total_samples = int(sample_rate * duration)
    rng = random.Random(24601)
    sample = array("f", [0.0]) * total_samples
    delays = (0.0, 0.012, 0.024)
    gains = (1.0, 0.7, 0.45)
    noise_buffer = [rng.uniform(-1.0, 1.0) for _ in range(total_samples)]

    for delay, gain in zip(delays, gains):
        offset = int(delay * sample_rate)
        for index in range(offset, total_samples):
            t = (index - offset) / sample_rate
            envelope = math.exp(-38.0 * t)
            if t < 0.006:
                envelope *= t / 0.006
            filtered = noise_buffer[index] * 0.75 + math.sin(2 * math.pi * 1850 * t) * 0.25
            sample[index] += gain * envelope * filtered
    return sample


def render_clap_wav(midi_path: str, wav_path: str, sample_rate: int = 44100) -> None:
    """Render note-on events from a MIDI file as synthetic claps."""
    midi = mido.MidiFile(midi_path)
    clap = _make_clap_sample(sample_rate)
    total_duration = max(midi.length + 0.5, 1.0)
    total_samples = int(total_duration * sample_rate)
    mix = array("f", [0.0]) * total_samples

    current_time = 0.0
    for message in midi:
        current_time += message.time
        if message.type == "note_on" and message.velocity > 0:
            start = int(current_time * sample_rate)
            velocity_scale = max(0.2, min(message.velocity / 100.0, 1.2))
            for offset, value in enumerate(clap):
                target = start + offset
                if target >= total_samples:
                    break
                mix[target] += value * velocity_scale

    peak = max((abs(value) for value in mix), default=1.0)
    normalizer = 0.9 / peak if peak > 0 else 1.0

    pcm = array("h")
    for value in mix:
        clamped = max(-1.0, min(1.0, value * normalizer))
        pcm.append(int(clamped * 32767))

    with tempfile.TemporaryDirectory() as temp_dir:
        raw_wav_path = Path(temp_dir) / "jazz-rhythm-raw.wav"
        with wave.open(str(raw_wav_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm.tobytes())
        normalize_wav(str(raw_wav_path), wav_path, sample_rate)
