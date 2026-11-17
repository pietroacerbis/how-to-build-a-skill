#!/bin/bash
set -e
mkdir -p "$(dirname 'downloads/slide-outline/SKILL.md')"
cat > 'downloads/slide-outline/SKILL.md' <<'FIXTURE_EOF'
---
name: slide-outline
description: Drafts a slide-by-slide outline for a presentation from a topic and an audience. Use when the user asks for a deck outline or a talk structure.
---

# Slide outline

1. Ask for the topic, the audience and the length in minutes if they are missing.
2. Allow one slide per two minutes.
3. Write one line per slide: the title, then the single point it makes.
4. End with a closing slide that states what the audience should do next.
FIXTURE_EOF
