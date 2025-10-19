---
name: Template Request
about: Request a new framework or language template
title: '[TEMPLATE] Add support for [Framework/Language]'
labels: template, enhancement
assignees: ''
---

## Framework/Language Information

**Name**: [e.g., React Native, Ruby on Rails, Rust]
**Category**: [Frontend / Backend / Mobile / ML / Other]
**Official Website**: [URL]

## Popularity & Justification

Why should this template be added?

- **GitHub Stars**: [if applicable]
- **npm/PyPI Downloads**: [if applicable]
- **Community Size**: [describe]
- **Your Use Case**: [why you need this]

## Detection Criteria

How should we detect this framework/language?

### File Indicators

What files indicate this is a [Framework] project?

- [ ] `package.json` with dependency: `___________`
- [ ] `requirements.txt` with dependency: `___________`
- [ ] `Cargo.toml` with dependency: `___________`
- [ ] Specific directory structure: `___________`
- [ ] Configuration file: `___________`
- [ ] Other: `___________`

### Example Detection Logic

```python
# Example (you can suggest pseudocode)
if package_json.has("react-native"):
    framework = "react-native"
    confidence = 0.95
```

## Recommended Subagents

What specialized subagents would be useful for this framework?

1. **[framework]-developer**: Main development specialist
2. **[framework]-tester**: Testing specialist (unit, integration, E2E)
3. **[framework]-performance**: Performance optimization (optional)
4. **Other**: ___________

## Code Patterns & Best Practices

What are the key patterns developers should follow?

### Example 1: [Pattern Name]

```[language]
// Provide a code example showing best practices
```

### Example 2: [Pattern Name]

```[language]
// Another example
```

## Testing Tools

What testing tools are commonly used?

- [ ] Unit testing: `___________` (e.g., Jest, pytest)
- [ ] Integration testing: `___________`
- [ ] E2E testing: `___________`
- [ ] Mocking: `___________`

## Common Dependencies

What tools/libraries are typically used with this framework?

| Category | Library | Purpose |
|----------|---------|---------|
| State Management | ___________ | ___________ |
| HTTP Client | ___________ | ___________ |
| Database | ___________ | ___________ |
| Styling | ___________ | ___________ |

## Related Documentation

- Official Docs: [URL]
- Best Practices Guide: [URL]
- Testing Guide: [URL]
- Style Guide: [URL]

## Sample Project (optional)

If you have a sample project that demonstrates this framework, share the repository:

**Repository**: [URL]
**Description**: [Brief description]

## Your Contribution

Are you willing to help create this template?

- [ ] I can provide code examples
- [ ] I can help write documentation
- [ ] I can test the template on real projects
- [ ] I can create a PR with the template
- [ ] I need someone else to implement it

## Additional Context

Add any other context about the template request here.

---

**Checklist**:

- [ ] I've checked that this framework isn't already supported
- [ ] I've provided detection criteria
- [ ] I've suggested realistic code patterns
- [ ] I've listed common testing tools
