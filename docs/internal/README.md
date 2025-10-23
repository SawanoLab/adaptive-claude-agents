# Internal Documentation

This directory contains internal development documentation for Adaptive Claude Agents.

These files are excluded via `.gitignore` to keep the public repo focused on user-facing content.

---

## 📁 Directory Structure

```
docs/
├── internal/                    # Internal development docs (this directory)
│   ├── archive/                # Archived old release notes and legacy plans
│   ├── releases/               # Release notes by version
│   ├── planning/               # Development plans and kickoff docs
│   ├── completion/             # Week/day completion reports
│   ├── design/                 # Architecture and design documents
│   ├── DISCUSSION.md          # Project origin and rationale
│   ├── IMPLEMENTATION.md      # Technical implementation details
│   └── README.md              # This file
├── archive/                    # Archived completed task reports (legacy)
├── *.md                       # User-facing documentation
└── *.ja.md                    # Japanese user documentation
```

---

## 📝 Active Documents

### Development Context
- **DISCUSSION.md** (~93 lines): Project origin, rationale, and key decisions
- **IMPLEMENTATION.md** (~225 lines): Technical architecture and implementation details

### Organized by Category

#### releases/ - Release Documentation
- **RELEASE_NOTES_v0.5.0-beta.md** (~476 lines): v0.5.0 comprehensive release notes
- **RELEASE_NOTES_v0.6.0-beta.md** (~730 lines): v0.6.0 comprehensive release notes
- **RELEASE_NOTES_v0.7.0-beta.md** (~650 lines): v0.7.0 comprehensive release notes
- **GITHUB_RELEASE_v0.7.0-beta.md** (~250 lines): v0.7.0 GitHub release summary (copy-paste ready)

#### planning/ - Development Plans
- **v0.6.0_PLAN.md** (~580 lines): v0.6.0 2-week development plan
- **v0.7.0_PLAN.md** (~600 lines): v0.7.0 4-week development plan
- **v0.7.0_WEEK1_KICKOFF.md** (~550 lines): v0.7.0 Week 1 task breakdown

#### completion/ - Progress Reports
- **WEEK2_v0.6.0_COMPLETION.md** (~450 lines): v0.6.0 Week 2 completion report
- **WEEK3_v0.6.0_COMPLETION.md** (~650 lines): v0.6.0 Week 3 completion report
- **v0.7.0_DAY3_4_COMPLETION.md** (~450 lines): v0.7.0 Day 3-4 completion report
- **v0.7.0_DAY5_6_COMPLETION.md** (~700 lines): v0.7.0 Day 5-6 completion report
- **v0.7.0_WEEK1_COMPLETION.md** (~650 lines): v0.7.0 Week 1 final report

#### design/ - Technical Design Documents
- **v0.7.0_CACHING_DESIGN.md** (~800 lines): Caching system architecture
- **v0.7.0_PERFORMANCE_TRACKING.md** (~550 lines): Performance baseline and tracking
- **v0.7.0_DAY3_4_OPTIMIZATION.md** (~600 lines): DirectoryScanner optimization plan
- **v0.7.0_REVERT_DECISION.md** (~300 lines): Why DirectoryScanner was reverted

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

### Directory Purpose

**Root (docs/internal/)**:
- Core development context documents (DISCUSSION.md, IMPLEMENTATION.md)
- These rarely change and provide historical context

**releases/**:
- Comprehensive release notes by version
- GitHub release summaries (copy-paste ready)
- Keep all versions for historical reference

**planning/**:
- Development plans (4-week, 2-week cycles)
- Week kickoff documents with task breakdowns
- Move here at start of development cycle

**completion/**:
- Week/day completion reports
- Progress tracking documents
- Move here after completion of work period

**design/**:
- Technical design documents
- Architecture decisions
- Performance analysis and optimization plans
- Move here during design phase

**archive/**:
- Old release notes from v0.4.x and earlier
- Legacy documents no longer relevant
- Completed plans that are >6 months old

### Organization Timing
- **At release start**: Create plan in planning/
- **During development**: Create design docs in design/
- **After milestone**: Move completion reports to completion/
- **At release**: Create release notes in releases/
- **Annually**: Move old documents (>1 year) to archive/

---

## 📊 Documentation Statistics

### docs/internal/
- **Core context**: 2 files (~318 lines)
- **releases/**: 4 files (~2,106 lines)
- **planning/**: 3 files (~1,730 lines)
- **completion/**: 5 files (~2,900 lines)
- **design/**: 4 files (~2,250 lines)
- **archive/**: 8 files (~2,900 lines)
- **Total: 26 files (~12,204 lines)**

### User-facing docs/
- Documentation: 10 files (~4,800 lines)
- Archive: 9 files (~2,400 lines)
- **Total: 19 files (~7,200 lines)**

---

## 🔄 Maintenance

### When to Update
1. **At Release Start**: Create plan in planning/
2. **During Development**: Create design docs in design/
3. **After Completion**: Move reports to completion/
4. **At Release**: Create release notes in releases/
5. **Annually**: Move old documents (>1 year) to archive/

### How to Organize
```bash
# Planning phase
git mv docs/internal/vX.Y.Z_PLAN.md docs/internal/planning/
git mv docs/internal/vX.Y.Z_WEEK*_KICKOFF.md docs/internal/planning/

# Design phase
git mv docs/internal/vX.Y.Z_*_DESIGN.md docs/internal/design/
git mv docs/internal/vX.Y.Z_PERFORMANCE_TRACKING.md docs/internal/design/

# Completion phase
git mv docs/internal/vX.Y.Z_DAY*_COMPLETION.md docs/internal/completion/
git mv docs/internal/vX.Y.Z_WEEK*_COMPLETION.md docs/internal/completion/

# Release phase
git mv docs/internal/RELEASE_NOTES_vX.Y.Z-beta.md docs/internal/releases/
git mv docs/internal/GITHUB_RELEASE_vX.Y.Z-beta.md docs/internal/releases/

# Annual cleanup (move >1 year old docs)
git mv docs/internal/releases/RELEASE_NOTES_v0.*.md docs/internal/archive/
```

---

## 📚 Public Documentation

For public-facing documentation, see:
- [README.md](../../README.md) - Project overview
- [CONTRIBUTING.md](../../CONTRIBUTING.md) - How to contribute
- [docs/BEST_PRACTICES.md](../BEST_PRACTICES.md) - Best practices and resources
- [LICENSE](../../LICENSE) - MIT License

---

## 📋 Quick Reference

### Find a Document

**Looking for release notes?** → `releases/RELEASE_NOTES_vX.Y.Z-beta.md`
**Looking for development plan?** → `planning/vX.Y.Z_PLAN.md`
**Looking for completion report?** → `completion/vX.Y.Z_WEEK*_COMPLETION.md`
**Looking for technical design?** → `design/vX.Y.Z_*_DESIGN.md`
**Looking for project origin?** → `DISCUSSION.md` (root)
**Looking for architecture?** → `IMPLEMENTATION.md` (root)

---

**Last Updated**: 2025-10-23 (v0.7.0-beta, organized structure)
**Maintainer**: Sawano Hiroaki
