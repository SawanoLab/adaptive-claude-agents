# Internal Documentation

This directory contains internal development documentation for Adaptive Claude Agents.

These files are excluded via `.gitignore` to keep the public repo focused on user-facing content.

---

## 📁 Directory Structure

```
docs/
├── internal/                    # Internal development docs (this directory)
│   ├── archive/                # Archived old release notes and plans
│   ├── DISCUSSION.md          # Project origin and rationale
│   ├── IMPLEMENTATION.md      # Technical implementation details
│   ├── RELEASE_NOTES_v0.5.0-beta.md  # Current release notes
│   └── README.md              # This file
├── archive/                    # Archived completed task reports
├── *.md                       # User-facing documentation
└── *.ja.md                    # Japanese user documentation
```

---

## 📝 Active Documents

### Development Context
- **DISCUSSION.md** (~93 lines): Project origin, rationale, and key decisions
- **IMPLEMENTATION.md** (~225 lines): Technical architecture and implementation details

### Release Documentation
- **RELEASE_NOTES_v0.5.0-beta.md** (~476 lines): Current release notes
  - Includes GitHub release summary (copy-paste ready)
  - Detailed technical information
  - Migration guide and roadmap

---

## 📦 Archived Documents

### docs/internal/archive/
Old release notes and completed plans:
- RELEASE_NOTES_v0.4.2-beta.md
- RELEASE_NOTES_v0.4.3-beta.md
- GITHUB_RELEASE_v0.4.1-beta.md
- GITHUB_RELEASE_v0.4.3-beta.md
- REDDIT_POST_v0.4.1.md
- COOKBOOK_INTEGRATION.md
- GITHUB_PLAN.md
- PHASE3_DESIGN.md

### docs/archive/
Completed development tasks:
- WEEK2_PROGRESS.md - Week 2 testing progress
- WEEK3_PLAN.md - Week 3 alpha testing plan
- DAY2_3_COMPLETION.md - Internal testing completion
- DAY4_5_COMPLETION.md - Code quality polish completion
- DAY6_COMPLETION.md - Public beta prep part 1
- DAY7_COMPLETION.md - Public beta prep part 2
- ALPHA_TESTING_GUIDE.md - Alpha testing guide (unused)
- LAUNCH_STEPS.md - Launch execution steps
- FINAL_LAUNCH_CHECKLIST.md - Final launch checklist

---

## 🗂️ Document Organization Policy

### What Stays Active
1. **Development Context**: DISCUSSION.md, IMPLEMENTATION.md (historical reference)
2. **Current Release Notes**: Latest version only (v0.5.0-beta)

### What Gets Archived
1. **Old Release Notes**: Previous version release documentation
2. **Completed Tasks**: Day-by-day completion reports, progress tracking
3. **Obsolete Plans**: Unused guides, completed checklists

### Archive Timing
- After new release: Move previous release notes to archive/
- After milestone completion: Move task reports to archive/
- Keep only 1-2 most recent release notes active

---

## 📊 Documentation Statistics

### Active Docs
- User-facing: 10 files (~4,800 lines)
- Internal: 4 files (~790 lines)
- **Total Active: 14 files**

### Archived Docs
- docs/archive: 9 files (~2,400 lines)
- docs/internal/archive: 8 files (~2,900 lines)
- **Total Archived: 17 files**

---

## 🔄 Maintenance

### When to Update
1. **After Each Release**: Archive old release notes, create new ones
2. **After Milestones**: Archive completion reports
3. **Quarterly**: Review and remove obsolete archived files (if >1 year old)

### How to Archive
```bash
# Move completed task docs
mv docs/DAY*_COMPLETION.md docs/archive/

# Move old release notes
mv docs/internal/RELEASE_NOTES_v0.4.*.md docs/internal/archive/
```

---

## 📚 Public Documentation

For public-facing documentation, see:
- [README.md](../../README.md) - Project overview
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - How to contribute
- [docs/BEST_PRACTICES.md](../BEST_PRACTICES.md) - Best practices and resources
- [LICENSE](../../LICENSE) - MIT License

---

**Last Updated**: 2025-10-23 (v0.5.0-beta)
**Maintainer**: Sawano Hiroaki
