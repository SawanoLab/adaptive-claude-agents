# Reddit Post Template - v0.4.1-beta

**Subreddit**: r/ClaudeAI
**Flair**: Project / Show and Tell

---

## Title Option 1 (Enthusiastic)
```
🚀 100% Framework Coverage! Adaptive Claude Agents now supports Go & Flutter
```

## Title Option 2 (Informative)
```
[Update] Adaptive Claude Agents v0.4.1 - Added Go backend & Flutter mobile support
```

## Title Option 3 (Technical)
```
Adaptive Claude Agents achieves 100% framework coverage with Go & Flutter support
```

---

## Post Content

```markdown
Hey r/ClaudeAI! 👋

Quick update on **Adaptive Claude Agents** - we just released **v0.4.1-beta** with Go backend and Flutter mobile framework support!

## 🎉 What's New

**Go Backend Framework** (85% detection confidence):
- Auto-detects Gin, Echo, Fiber, Chi, Gorilla Mux
- GORM, Ent ORM support
- 3 specialized templates: go-developer, go-reviewer, concurrency-checker

**Flutter Mobile Framework** (80% detection confidence):
- Detects Provider, Riverpod, Bloc, GetX, MobX
- HTTP clients (Dio), databases (sqflite, Hive)
- Specialized flutter-developer template

## 📊 Now Supporting 11/11 Frameworks (100% Coverage!)

**Frontend**: Next.js (100%), React (80%), Vue (90%)
**Backend**: FastAPI (80%), Django (80%), Flask (70%), Go (85%) 🆕
**Mobile**: iOS Swift (80%), Flutter (80%) 🆕
**ML/AI**: Python ML/CV (100%)
**Web**: Vanilla PHP (70%)

## 💡 What is Adaptive Claude Agents?

A framework that automatically:
1. **Detects your project's tech stack** (framework, tools, testing libs)
2. **Generates specialized subagents** tailored to your stack
3. **Adapts code review rigor** based on your development phase (prototype → MVP → production)

Think of it as "Claude Code that automatically configures itself for your project."

## 🚀 Quick Start

```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

Then in Claude Code:
```
/project-analyzer
```

It'll detect your stack and generate the right subagents automatically.

## 📚 Resources

- GitHub: https://github.com/SawanoLab/adaptive-claude-agents
- Quick Start: [docs/QUICKSTART.md](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/QUICKSTART.md)
- Examples: [docs/EXAMPLES.md](https://github.com/SawanoLab/adaptive-claude-agents/blob/main/docs/EXAMPLES.md)

## 🙏 Feedback Welcome!

This is still beta, so please report any issues or suggestions! The goal is to support every major framework developers actually use.

What frameworks would you like to see next? (Considering: Ruby on Rails, Spring Boot, Laravel...)

---

**Edit**: For those asking - yes, this works with the new Claude Code features! The subagents integrate seamlessly with the native agent system.
```

---

## Alternative Shorter Version (if char limit)

```markdown
**Adaptive Claude Agents v0.4.1** is out! 🚀

Added **Go backend** (Gin, Echo, Fiber) and **Flutter mobile** support. Now at **100% framework coverage** (11/11).

**What it does**: Auto-detects your project's tech stack and generates specialized Claude Code subagents tailored to your framework + development phase.

**Install**:
```bash
curl -fsSL https://raw.githubusercontent.com/SawanoLab/adaptive-claude-agents/main/install.sh | bash
```

GitHub: https://github.com/SawanoLab/adaptive-claude-agents

Feedback welcome! What frameworks should we add next?
```

---

## Expected Questions & Answers

**Q: How is this different from claude-init?**
A: claude-init is for one-time setup. This runs as a global Skill, continuously adapts to your project, and adjusts code review rigor based on development phase (prototype vs. production).

**Q: Does this work with the new Claude Code?**
A: Yes! It's designed specifically for Claude Code and uses the native subagent system.

**Q: What does "phase-aware review" mean?**
A: It adjusts code review strictness based on whether you're prototyping (light review, focus on speed) or in production (strict review, 80%+ test coverage, OWASP checks).

**Q: Can I customize the templates?**
A: Yes! They're just markdown files in `templates/`. You can edit or add your own.

**Q: Why Go and Flutter specifically?**
A: Community requests! If you want to see other frameworks (Rails, Spring Boot, Laravel), please open an issue or discussion.

**Q: Is this open source?**
A: Yes! MIT licensed. Contributions welcome.

---

## Posting Strategy

**Best Time to Post**:
- Weekday mornings (9-11am EST)
- Avoid weekends (lower engagement)

**Engagement Tips**:
- Respond to questions within first 2 hours
- Be humble and open to feedback
- Thank people for suggestions
- If someone reports a bug, acknowledge and create GitHub issue

**Follow-up Comments** (after 1-2 hours):
```markdown
Thanks for the positive feedback everyone! 🙏

A few folks asked about [common question] - [answer].

If you try it out, I'd love to hear what works and what doesn't. Filing issues on GitHub is super helpful!
```

---

## Success Metrics

**Good Response**:
- 20+ upvotes in 24 hours
- 5+ constructive comments
- 1-2 GitHub stars/issues

**Great Response**:
- 50+ upvotes
- 10+ comments
- 5+ GitHub stars
- Feature requests or contributions

---

Repository: https://github.com/SawanoLab/adaptive-claude-agents
