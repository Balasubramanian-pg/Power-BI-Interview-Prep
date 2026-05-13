from pathlib import Path
import re

ROOT = Path(".")

FENCE_RE = re.compile(r"^(```|~~~)")
TABLE_RE = re.compile(r"^\s*\|")
FRONTMATTER_RE = re.compile(r"^---\s*$")


def should_remove(line: str) -> bool:
    stripped = line.strip()

    return stripped in {"---", "***"}


def process_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()

    output = []

    in_code_block = False
    in_frontmatter = False
    frontmatter_done = False

    for idx, line in enumerate(lines):

        if FENCE_RE.match(line):
            in_code_block = not in_code_block
            output.append(line)
            continue

        if idx == 0 and FRONTMATTER_RE.match(line):
            in_frontmatter = True
            output.append(line)
            continue

        elif in_frontmatter and FRONTMATTER_RE.match(line):
            in_frontmatter = False
            frontmatter_done = True
            output.append(line)
            continue

        if in_code_block or in_frontmatter:
            output.append(line)
            continue

        if TABLE_RE.match(line):
            output.append(line)
            continue

        if should_remove(line):
            continue

        output.append(line)

    new_content = "\n".join(output) + "\n"

    path.write_text(new_content, encoding="utf-8")


for md_file in ROOT.rglob("*.md"):
    process_file(md_file)

print("Markdown cleanup complete.")
