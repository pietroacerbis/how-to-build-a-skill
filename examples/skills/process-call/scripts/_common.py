"""Helpers shared by the process-call scripts. Standard library only."""
import pathlib
import re
import unicodedata

SKILL_DIR = pathlib.Path(__file__).resolve().parent.parent
SPINE_BEFORE = ["Framing", "Open loops", "What happened", "Decisions", "Actions", "Quotes"]
SPINE_AFTER = ["Next steps", "Provenance"]


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def frontmatter(text: str) -> dict:
    """Read a flat YAML frontmatter: key: value, and key: [a, b]."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        data[key.strip()] = value
    return data


def body(text: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)


def variants() -> dict:
    """The variant set is the files in variants/: the folder is the set."""
    found = {}
    for path in sorted((SKILL_DIR / "variants").glob("*.md")):
        sections = frontmatter(path.read_text(encoding="utf-8")).get("sections")
        if isinstance(sections, list):
            found[path.stem] = sections
    return found


def expected_sections(call_type: str) -> list:
    return SPINE_BEFORE + variants().get(call_type, []) + SPINE_AFTER
