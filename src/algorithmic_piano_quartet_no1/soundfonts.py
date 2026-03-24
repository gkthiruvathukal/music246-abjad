"""SoundFont helpers for algorithmic quartet audio rendering."""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile


AEGEAN_SF2_NAME = "AegeanSymphonicOrchestra.sf2"
AEGEAN_DOWNLOAD_URL = (
    "https://drive.google.com/uc?export=download&id=1E9YQVLrtEbTOWeWHUNOrX7ZKq8ANp4-C"
)
SALAMANDER_SF2_NAME = "SalamanderGrandPiano-V3+20200602.sf2"
SALAMANDER_DOWNLOAD_URL = (
    "https://freepats.zenvoid.org/Piano/SalamanderGrandPiano/"
    "SalamanderGrandPiano-SF2-V3+20200602.tar.xz"
)


def ensure_soundfont(soundfont_path: str) -> Path:
    """Return a usable SoundFont path, downloading supported defaults if needed."""
    soundfont = Path(soundfont_path).expanduser()
    if soundfont.exists():
        return soundfont

    if soundfont.name == AEGEAN_SF2_NAME:
        return _download_aegean_soundfont(soundfont)
    if soundfont.name == SALAMANDER_SF2_NAME:
        return _download_salamander_soundfont(soundfont)

    raise FileNotFoundError(f"Soundfont not found: {soundfont}")


def _download_aegean_soundfont(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Aegean Symphonic Orchestra soundfont to {destination}")

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "aegean-symphonic-orchestra.zip"
        _download_google_drive_archive(AEGEAN_DOWNLOAD_URL, archive_path)
        with zipfile.ZipFile(archive_path) as archive:
            member_name = _find_archive_member(archive.namelist(), ".sf2")
            with archive.open(member_name) as source:
                with destination.open("wb") as target:
                    shutil.copyfileobj(source, target)

    print(f"Soundfont cached: {destination}")
    return destination


def _download_salamander_soundfont(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Salamander Grand Piano soundfont to {destination}")

    with tempfile.TemporaryDirectory() as temp_dir:
        archive_path = Path(temp_dir) / "salamander-grand-piano.tar.xz"
        _download_binary_file(SALAMANDER_DOWNLOAD_URL, archive_path)
        with tarfile.open(archive_path, mode="r:xz") as archive:
            member_name = _find_archive_member(archive.getnames(), ".sf2")
            member = archive.getmember(member_name)
            with archive.extractfile(member) as source:
                if source is None:
                    raise FileNotFoundError("Salamander archive did not contain extractable .sf2 data.")
                with destination.open("wb") as target:
                    shutil.copyfileobj(source, target)

    print(f"Soundfont cached: {destination}")
    return destination


def _find_archive_member(member_names: list[str], suffix: str) -> str:
    for member_name in member_names:
        if member_name.lower().endswith(suffix):
            return member_name
    raise FileNotFoundError(f"Downloaded archive did not contain a {suffix} file.")


def _download_google_drive_archive(url: str, destination: Path) -> None:
    opener = urllib.request.build_opener()
    with opener.open(url) as response:
        if _looks_like_html(response):
            html = response.read().decode("utf-8", "ignore")
            confirm_url = _extract_confirm_url(html)
            if confirm_url is None:
                raise RuntimeError("Could not locate Google Drive confirmation link for soundfont download.")
            with opener.open(confirm_url) as confirmed_response:
                with destination.open("wb") as file_pointer:
                    shutil.copyfileobj(confirmed_response, file_pointer)
            return

        with destination.open("wb") as file_pointer:
            shutil.copyfileobj(response, file_pointer)


def _download_binary_file(url: str, destination: Path) -> None:
    with urllib.request.urlopen(url) as response:
        with destination.open("wb") as file_pointer:
            shutil.copyfileobj(response, file_pointer)


def _looks_like_html(response) -> bool:
    return response.headers.get_content_type() == "text/html"


def _extract_confirm_url(html: str) -> str | None:
    action_match = re.search(r'<form id="download-form" action="([^"]+)"', html)
    if action_match is None:
        return None

    inputs = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', html))
    if not inputs:
        return None

    query = urllib.parse.urlencode(inputs)
    return f"{action_match.group(1)}?{query}"
