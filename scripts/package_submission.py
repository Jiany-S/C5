"""Build an allowlisted standalone source ZIP; exclude secrets, runtime data and caches."""
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]

TOP_LEVEL = ["README.md", "business.py", "mcp_server.py", "agent_client.py", "config.py", "terminal_ui.py", "pytest.ini",
             "requirements.txt", "requirements-dev.txt", "requirements-lock.txt", ".env.example", ".gitignore", ".gitattributes"]
FOLDERS = ["business_data", "docs", "tests", "scripts", "evidence"]
EXTENSIONS = {".py", ".md", ".json", ".xml", ".srt", ".png"}


def submission_files() -> list[Path]:
    files = [ROOT / name for name in TOP_LEVEL]
    for folder in FOLDERS:
        files.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and p.suffix in EXTENSIONS and "__pycache__" not in p.parts)
    return sorted(set(files))


def main():
    files = submission_files()
    assert all(p.is_file() and p.is_relative_to(ROOT) for p in files)
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / "C5-submission.zip"
    with ZipFile(archive, "w", ZIP_DEFLATED) as bundle:
        for path in files:
            bundle.write(path, "C5/" + path.relative_to(ROOT).as_posix())
    with ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        assert len(bundle.namelist()) == len(files)
        assert not any(n.endswith(".env") or "/runtime/" in n or "/.venv/" in n for n in bundle.namelist())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / "manifest.json").write_text(json.dumps({"sha256":digest,
         "files":[p.relative_to(ROOT).as_posix() for p in files]},indent=2),encoding="utf-8")
    print(f"Created {archive.name}: {len(files)} files, {archive.stat().st_size} bytes, SHA-256 {digest}")


if __name__ == "__main__":
    main()
