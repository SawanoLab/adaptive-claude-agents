# Token Optimization Quick Start Guide

**5 Minutes to 60% Token Reduction**

This guide shows you how to immediately start saving tokens when using Adaptive Claude Agents.

---

## ✅ Step 1: Verify Installation (30 seconds)

Check that token optimization features are installed:

```bash
# Check for token optimization section in templates
grep -l "Token Optimization Guidelines" templates/*/*.md | wc -l
# Should show: 14 (all templates have it)

# Check for monitoring script
ls scripts/monitor_tokens.sh
# Should exist
```

---

## ✅ Step 2: Understand the Core Principle (1 minute)

**Before optimization** (wasteful):
```
User: "Review my API code"

Subagent:
  - Reads all files (20,000 tokens)
  - Returns detailed 5,000 token report
  - Main agent context grows by 5,000 tokens

Total: 25,000 tokens
```

**After optimization** (efficient):
```
User: "Review my API code"

Subagent:
  - Reads only relevant files (5,000 tokens)
  - Saves detailed report to .claude/reports/api-review-20251031.md
  - Returns 200 token summary

Total: 5,200 tokens (79% reduction!)
```

---

## ✅ Step 3: Apply to Your Project (2 minutes)

### Option A: New Project

When generating subagents for a new project, they automatically include token optimization:

```bash
cd your-new-project
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --auto
```

All generated subagents will have Token Optimization Guidelines built-in.

### Option B: Existing Project

Update your existing subagents:

```bash
cd your-existing-project

# Update all existing subagent files
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --update-only --auto
```

This adds Token Optimization Guidelines to all your `.claude/agents/*.md` files.

---

## ✅ Step 4: Monitor Your Savings (1 minute)

Track token usage over time:

```bash
# Run monitoring tool
./scripts/monitor_tokens.sh
```

Expected output:
```
🔍 Token Usage Monitoring Tool
==============================

📊 Recent Token Usage
--------------------
  • api-review: 5,200 tokens
  • test-generation: 8,500 tokens
  • code-refactor: 12,000 tokens

📈 Statistics
-------------
  Average tokens: 8,566
  ✅ Good! Average is below 20k target

📁 Generated Reports
-------------------
  Found 3 report(s)
  Total tokens in reports: 18,500
  ✅ These tokens were saved from main agent context!
```

---

## 🎯 Expected Results

### Immediate Benefits (Day 1)

- ✅ **20-30% token reduction** from following guidelines
- ✅ Subagent reports saved to `.claude/reports/`
- ✅ Main agent context stays smaller

### After 1 Week

- ✅ **40-50% token reduction** from optimized workflows
- ✅ Cost savings visible in usage metrics
- ✅ Faster response times (smaller context)

### After 1 Month

- ✅ **60-70% token reduction** (full optimization)
- ✅ $70-90/month savings (typical developer)
- ✅ Established best practices

---

## 📋 Quick Checklist

Use this checklist when working with subagents:

### Before Delegating to Subagent

- [ ] Can I do this in main agent with <5k tokens? (If yes, don't use subagent)
- [ ] Am I passing file paths instead of file contents?
- [ ] Is my context <5k tokens?
- [ ] Do I need parallel execution? (Limit to 2-3 max)

### After Subagent Returns

- [ ] Did subagent return a summary (<500 tokens)?
- [ ] Was detailed report saved to `.claude/reports/`?
- [ ] Do I actually need to read the full report?

### Weekly Review

- [ ] Run `./scripts/monitor_tokens.sh`
- [ ] Check average tokens per task (<20k target)
- [ ] Review `.claude/reports/` size
- [ ] Identify optimization opportunities

---

## 🔍 Common Questions

### Q: How do I know if optimization is working?

**A:** Run the monitoring script:
```bash
./scripts/monitor_tokens.sh
```

If your average is <20k tokens per task, optimization is working!

### Q: What if a subagent returns too much data?

**A:** The subagent should save detailed data to `.claude/reports/` and return only a summary. If it's not doing this, check that your templates have the Token Optimization Guidelines section.

### Q: Can I read the full reports later?

**A:** Yes! Reports are saved in `.claude/reports/`. You can read them anytime:
```bash
cat .claude/reports/api-review-20251031-143022.md
```

### Q: Should I commit `.claude/reports/` to git?

**A:** No! These are temporary analysis files. They're already in `.gitignore`.

---

## 📚 Next Steps

### Learn More

1. **For detailed strategies**: Read [TOKEN_OPTIMIZATION_GUIDE.md](TOKEN_OPTIMIZATION_GUIDE.md)
2. **For framework-specific tips**: See [2025_BEST_PRACTICES.md](2025_BEST_PRACTICES.md)
3. **For examples**: Check [examples/reports/](../examples/reports/)

### Advanced Optimization

Once you're comfortable with basics:

1. Implement Context Compression patterns
2. Use Just-in-Time Context Loading
3. Add token budget validation
4. Create custom monitoring dashboards

---

## 🎉 Success Stories

### Example 1: API Review

**Before**: 205,000 tokens
**After**: 10,700 tokens
**Savings**: 95%

### Example 2: Test Generation

**Before**: 45,000 tokens
**After**: 15,000 tokens
**Savings**: 67%

### Example 3: Code Refactoring

**Before**: 80,000 tokens
**After**: 25,000 tokens
**Savings**: 69%

---

## 🆘 Troubleshooting

### Issue: Subagent still returning large responses

**Solution**: Verify Token Optimization Guidelines are in your template:
```bash
grep "Token Optimization Guidelines" .claude/agents/your-subagent.md
```

If not found, update your subagents:
```bash
python3 "$SKILLS_DIR/adaptive-claude-agents/skills/project-analyzer/analyze_project.py" . --update-only --auto
```

### Issue: Reports not being created

**Solution**: Check if `.claude/reports/` directory exists:
```bash
mkdir -p .claude/reports
```

### Issue: High token usage persists

**Solution**: Review your usage patterns:
1. Are you parallelizing too much? (Limit to 2-3)
2. Are you passing full file contents? (Pass paths instead)
3. Are you reading reports unnecessarily? (Only when needed)

---

## 📞 Get Help

- **Documentation**: [TOKEN_OPTIMIZATION_GUIDE.md](TOKEN_OPTIMIZATION_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/SawanoLab/adaptive-claude-agents/issues)
- **Examples**: [examples/reports/](../examples/reports/)

---

**Time to first savings**: 5 minutes
**Expected ROI**: 60-70% token reduction
**Effort**: Minimal (automatic once set up)

🚀 Start optimizing now!
