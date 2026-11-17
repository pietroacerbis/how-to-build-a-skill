#!/usr/bin/env python3
"""Scan a skill folder for what should stop an install. Reads every file, runs none.

    python3 scan_security.py PATH/TO/SKILL

FAIL: hidden characters, instructions aimed at the model, secrets read, data sent out,
code decoded or downloaded and then run, writes to the user's shell or startup files.
WARN: what a person should look at: network calls, HTML comments, long encoded strings,
binary files. INFO: every domain the skill names.
Exit 0: no FAIL. Exit 2: at least one FAIL. Standard library only.
"""
import hashlib
import pathlib
import re
import sys

# Zero-width marks, direction overrides, word joiners, the byte-order mark, Unicode tags.
INVISIBLE_RANGES = [(0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x2066, 0x2069), (0xFEFF, 0xFEFF), (0xE0000, 0xE007F)]
HIDDEN = re.compile("[" + "".join(f"{chr(a)}-{chr(b)}" for a, b in INVISIBLE_RANGES) + "]")
MODEL_ADDRESSED = re.compile(
    r"ignore (all |any )?(previous|prior|above|earlier) (instructions|rules)"
    r"|do not (tell|inform|mention|show)( this to)? the user"
    r"|without (telling|asking|informing) the user"
    r"|(note|message) (to|for) (the )?(assistant|ai|claude|model)\b"
    r"|you are now\b|new system prompt|<\s*/?\s*system\s*>",
    re.I,
)
SECRETS = re.compile(
    r"\.env\b|\.ssh/|id_rsa|id_ed25519|\.aws/credentials|\.netrc|\.npmrc|\.pypirc"
    r"|keychain|find-generic-password|Login Data|Cookies\b|Local Storage"
    r"|(os\.environ|process\.env|getenv)[^\n]{0,40}(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)",
    re.I,
)
NETWORK = re.compile(
    r"\bcurl\b|\bwget\b|requests\.(get|post|put)|urllib\.request|http\.client|\bfetch\(|axios"
    r"|\bsocket\.|Invoke-WebRequest|\bnc\s+-",
    re.I,
)
RUN_DECODED = re.compile(
    r"base64\s+(-d|--decode)[^\n]*\|\s*(ba|z)?sh\b|(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b"
    r"|\b(eval|exec)\s*\(\s*(base64|atob|bytes\.fromhex|codecs\.decode|compile)"
    r"|new Function\(|\batob\([^)]*\)\s*\)",
    re.I,
)
STARTUP_WRITES = re.compile(r"(~|\$HOME|expanduser\([^)]*)[^\s'\"]*/\.(bashrc|zshrc|zprofile|bash_profile|profile)\b|\bcrontab\b|LaunchAgents|\brm\s+-rf\s+[~/]", re.I)
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
BLOB = re.compile(r"[A-Za-z0-9+/]{200,}={0,2}")
URL = re.compile(r"https?://([A-Za-z0-9.-]+)")
CODE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".rb", ".pl", ".ps1", ".bash", ".zsh", ".mjs", ".cjs"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: scan_security.py PATH/TO/SKILL")
        return 2
    root = pathlib.Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"FAIL {root} is not a folder")
        return 2

    findings, domains, scanned = [], set(), 0
    # This file holds the patterns it hunts for. A byte-identical copy is skipped by hash,
    # so an edited copy, or anything else, is scanned in full.
    own_hash = hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()

    def add(level: str, path: pathlib.Path, line_no: int, what: str):
        findings.append((level, f"{path.relative_to(root).as_posix()}:{line_no}", what))

    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts):
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() == own_hash:
            add("INFO", path, 0, "this scanner, byte for byte: skipped")
            continue
        if b"\x00" in raw[:4096]:
            add("WARN", path, 0, "binary file, not read: open it by hand or remove it")
            continue
        text = raw.decode("utf-8", errors="replace")
        scanned += 1
        is_code = path.suffix in CODE_SUFFIXES or text.startswith("#!")
        secret_lines, network_lines = [], []
        for n, line in enumerate(text.splitlines(), 1):
            if HIDDEN.search(line):
                add("FAIL", path, n, "invisible or direction-changing characters: text the reader cannot see")
            hit = MODEL_ADDRESSED.search(line)
            if hit:
                add("FAIL", path, n, f"text addressed to the model: {hit.group(0)!r}")
            hit = SECRETS.search(line)
            if hit:
                secret_lines.append(n)
                add("FAIL" if is_code else "WARN", path, n, f"reads secrets or credentials: {hit.group(0)!r}")
            hit = NETWORK.search(line)
            if is_code and hit:
                network_lines.append(n)
                add("WARN", path, n, f"network call: {hit.group(0)!r}")
            if RUN_DECODED.search(line):
                add("FAIL", path, n, "decodes or downloads code and runs it")
            hit = STARTUP_WRITES.search(line)
            if is_code and hit:
                add("FAIL", path, n, f"touches shell startup files or deletes outside the skill: {hit.group(0)!r}")
            if BLOB.search(line):
                add("WARN", path, n, "long encoded string: decode it and read it before trusting the skill")
            domains.update(URL.findall(line))
        if secret_lines and network_lines:
            add("FAIL", path, network_lines[0], f"reads secrets (line {secret_lines[0]}) and calls the network in the same file: possible exfiltration")
        if path.suffix == ".md":
            for match in COMMENT.finditer(text):
                n = text[: match.start()].count("\n") + 1
                body = match.group(1).strip()
                if MODEL_ADDRESSED.search(body) or re.search(r"\b(assistant|claude|instruction|secretly|silently)\b", body, re.I):
                    add("FAIL", path, n, f"HTML comment with instructions, invisible once rendered: {body[:80]!r}")
                elif body:
                    add("WARN", path, n, f"HTML comment, invisible once rendered: {body[:60]!r}")

    for level, where, what in findings:
        print(f"{level} {where} {what}")
    for domain in sorted(domains):
        print(f"INFO domain named: {domain}")
    fails = sum(1 for f in findings if f[0] == "FAIL")
    warns = sum(1 for f in findings if f[0] == "WARN")
    print(f"scanned {scanned} files: {fails} fail, {warns} warn, {len(domains)} domains")
    return 2 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
