---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Run command '...'
3. See error

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Environment

- **OS**: [e.g., macOS 13.5, Ubuntu 22.04, Windows 11 WSL2]
- **Python Version**: [e.g., 3.9.7, 3.11.2]
- **Claude Code Version**: [e.g., 0.4.0]
- **Adaptive Claude Agents Version**: [run `git -C "$HOME/Library/Application Support/Claude/skills/adaptive-claude-agents" rev-parse --short HEAD` or check installation]

## Project Type

What kind of project were you analyzing?

- [ ] Next.js
- [ ] React
- [ ] Vue
- [ ] FastAPI
- [ ] Django
- [ ] Flask
- [ ] Vanilla PHP/Web
- [ ] Python ML/CV
- [ ] iOS Swift
- [ ] Go
- [ ] Flutter
- [ ] Other: ___________

## Logs/Error Messages

```
Paste any error messages or relevant logs here
```

## Detection Output (if applicable)

If the bug is related to tech stack or phase detection, please paste the output:

```bash
python3 skills/project-analyzer/detect_stack.py /path/to/your/project
```

```
Paste detection output here
```

## Screenshots (optional)

If applicable, add screenshots to help explain your problem.

## Additional Context

Add any other context about the problem here.

---

**Checklist**:

- [ ] I've searched existing issues to ensure this isn't a duplicate
- [ ] I've provided all the requested information
- [ ] I've tested with the latest version
