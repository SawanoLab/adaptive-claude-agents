# Security Policy

## Supported Versions

This project is currently in **pre-alpha** development (Phase 1). Security updates will be provided for:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x: (pre-release)  |

Once v1.0 is released, we will provide security updates for the latest stable version.

## Reporting a Vulnerability

We take the security of Adaptive Claude Agents seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please **do not** report security vulnerabilities through public GitHub issues, discussions, or pull requests.

### 2. Report Privately

Send a detailed report to: **[INSERT SECURITY EMAIL]**

Include:

- **Description**: Clear explanation of the vulnerability
- **Impact**: Potential consequences if exploited
- **Reproduction**: Step-by-step instructions to reproduce
- **Environment**: OS, Claude Code version, Python version, etc.
- **Suggested fix**: If you have one (optional)

### 3. What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Regular updates**: Every 7 days on progress
- **Resolution timeline**: Varies by severity
  - **Critical**: 7 days
  - **High**: 30 days
  - **Medium**: 60 days
  - **Low**: 90 days

### 4. Disclosure Policy

- We will work with you to understand and resolve the issue
- We will credit you in the security advisory (unless you prefer to remain anonymous)
- We will coordinate public disclosure after a fix is available
- Typical disclosure timeline: 90 days from initial report

## Security Considerations

### Template Security

**Risk**: Malicious templates could execute harmful code

**Mitigation**:

- All community-submitted templates undergo manual review
- Templates are sandboxed during testing
- Dangerous commands are flagged in review process
- Users are warned before executing any template

### Detection Script Security

**Risk**: Project analysis scripts could be exploited

**Mitigation**:

- Scripts run with user permissions (no privilege escalation)
- File system access is limited to project directory
- No network requests without explicit user consent
- All dependencies are pinned and verified

### MCP Configuration Security

**Risk**: MCP configuration could expose sensitive data

**Mitigation**:

- MCP config files are gitignored
- No credentials stored in configuration
- User-specific settings are local only
- Clear documentation on secure setup

### Dependency Security

We regularly check for vulnerabilities in dependencies:

```bash
# Python dependencies
pip-audit

# Node.js dependencies (if used)
npm audit
```

### Code Injection Prevention

**Risk**: User input could lead to code injection

**Mitigation**:

- Input validation on all user-provided data
- No `eval()` or similar dynamic code execution
- Parameterized commands when calling external tools
- Sanitization of file paths

## Best Practices for Users

### When Using This Tool

1. **Review Generated Templates**
   - Always review subagent templates before using
   - Understand what tools each subagent has access to
   - Be cautious with templates from unknown sources

2. **Limit Permissions**
   - Run with minimal necessary permissions
   - Use virtual environments
   - Don't run as root/administrator

3. **Verify Sources**
   - Only use templates from trusted sources
   - Check template author credentials
   - Review template code before activation

4. **Keep Updated**
   - Regularly update to latest version
   - Subscribe to security advisories
   - Monitor project announcements

### When Contributing

1. **Code Review**
   - All code changes require maintainer review
   - Security-sensitive changes need extra scrutiny
   - Follow secure coding guidelines

2. **Dependencies**
   - Minimize new dependencies
   - Use well-maintained, trusted packages
   - Pin versions in requirements.txt

3. **Secrets**
   - Never commit API keys, tokens, or credentials
   - Use environment variables for sensitive data
   - Review `.gitignore` before committing

## Security Features

### Current (Phase 1)

- [ ] Input validation on project paths
- [ ] Safe file path handling
- [ ] No network requests without consent
- [ ] Dependency vulnerability scanning

### Planned (Future Phases)

- [ ] Template signature verification
- [ ] Sandboxed template execution
- [ ] Automated security testing (SAST)
- [ ] Dependency update automation (Dependabot)

## Known Security Limitations

As a **pre-alpha** project, be aware of these limitations:

1. **Limited Testing**: Security testing is not yet comprehensive
2. **Rapid Changes**: Security features are still being developed
3. **Community Templates**: Not all templates are vetted equally
4. **MCP Integration**: Relies on security of MCP servers

**Recommendation**: Use in **non-production** environments during pre-alpha.

## Security Resources

### For Users

- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Claude Code Security](https://docs.claude.com/en/docs/claude-code) (Official docs)

### For Contributors

- [Secure Coding Guidelines](https://wiki.sei.cmu.edu/confluence/display/seccode)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- Project `CONTRIBUTING.md` - includes security review checklist

## Security Acknowledgments

We would like to thank the following individuals for responsibly disclosing security vulnerabilities:

<!-- Will be populated as vulnerabilities are reported and fixed -->

*No vulnerabilities reported yet (project in pre-alpha)*

## Questions?

- **General security questions**: Open a [GitHub Discussion](https://github.com/SawanoLab/adaptive-claude-agents/discussions)
- **Security vulnerability**: Email [INSERT SECURITY EMAIL]
- **Security feature requests**: Create a [GitHub Issue](https://github.com/SawanoLab/adaptive-claude-agents/issues) with `security` label

---

**Last Updated**: 2025-01-19

**Note**: This security policy will be updated as the project matures. Current focus is on establishing secure development practices during Phase 1.
