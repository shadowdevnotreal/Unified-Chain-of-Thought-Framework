# Contributing to Unified CoT Framework

Thank you for your interest in contributing to the Unified Chain of Thought Framework! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Specify your environment (OS, shell, Claude Code version)
- Attach relevant logs or screenshots

### 2. Suggest Enhancements
- Open a GitHub Issue with the "enhancement" label
- Clearly describe the proposed feature
- Explain the use case and benefits
- Consider implementation complexity

### 3. Improve Documentation
- Fix typos and clarify explanations
- Add examples and use cases
- Improve installation instructions
- Translate documentation (future)

### 4. Create New Agents
- Follow the agent template structure
- Include comprehensive examples
- Document all capabilities and usage patterns
- Test thoroughly before submission

### 5. Submit Code
- Fix bugs or implement features
- Follow coding standards
- Add tests where applicable
- Update documentation

---

## 🚀 Getting Started

### Prerequisites
- Git installed
- Bash or Zsh shell
- Claude Code access
- Basic familiarity with the framework

### Fork and Clone
```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/unified-cot-framework.git
cd unified-cot-framework
```

### Test Installation Locally
```bash
# Run the installer
./install.sh

# Verify installation
cot-version
cot-agents
```

---

## 📋 Contribution Guidelines

### Code Style
- Use clear, descriptive variable names
- Add comments for complex logic
- Follow existing code patterns
- Keep functions focused and small

### Shell Scripts
- Use `#!/bin/bash` shebang
- Include error handling (`set -e`)
- Add descriptive comments
- Use color-coded output for clarity
- Support multiple platforms where possible

### Markdown Documentation
- Use clear headings and structure
- Include code examples with syntax highlighting
- Add tables for comparisons
- Use emoji sparingly and consistently
- Keep line length reasonable (80-120 chars)

### Agent Development

When creating new agents, follow this template structure:

```markdown
# Agent Name

## Role and Purpose
[Clear description of the agent's role]

## Core Capabilities
- Capability 1
- Capability 2
- Capability 3

## Chain of Thought Framework Integration

### ANALYZE Phase
[Framework integration details]

### PLAN Phase
[Framework integration details]

### VALIDATE Phase
[Framework integration details]

### IMPLEMENT Phase
[Framework integration details]

### CONFIRM Phase
[Framework integration details]

## Example Usage
[Practical examples with different intensity levels]

## Best Practices
[Guidelines for effective use]

---
**Agent Version**: 1.0.0
**Last Updated**: YYYY-MM-DD
**Compatible with**: Unified CoT Framework v2.0+
```

---

## 🔍 Pull Request Process

### Before Submitting

1. **Test Your Changes**
   ```bash
   # Install and test
   ./install.sh

   # Verify agents work
   cot /use your-new-agent "test command"

   # Test uninstall
   ./uninstall.sh
   ```

2. **Update Documentation**
   - Update README.md if adding features
   - Add examples for new capabilities
   - Update agent documentation
   - Include inline code comments

3. **Check for Issues**
   - Ensure no broken links
   - Verify all scripts are executable
   - Test on multiple platforms if possible
   - Check for shell compatibility

### Submitting PR

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number
   ```

2. **Commit Changes**
   ```bash
   git add .
   git commit -m "Clear, descriptive commit message"
   ```

   **Commit Message Format:**
   ```
   [TYPE] Brief description (50 chars or less)

   More detailed explanation if needed (wrap at 72 chars).
   Include the motivation for the change and contrast with
   previous behavior.

   Fixes #issue_number (if applicable)
   ```

   **Types:**
   - `[FEAT]` - New feature
   - `[FIX]` - Bug fix
   - `[DOCS]` - Documentation changes
   - `[STYLE]` - Code style changes (formatting)
   - `[REFACTOR]` - Code refactoring
   - `[TEST]` - Adding tests
   - `[CHORE]` - Maintenance tasks

3. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open Pull Request**
   - Use the PR template
   - Link related issues
   - Describe changes thoroughly
   - Add screenshots if relevant
   - Request review from maintainers

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Breaking change
- [ ] Other (please describe)

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
Describe how you tested your changes:
- [ ] Tested installation on [OS]
- [ ] Verified agent functionality
- [ ] Checked documentation accuracy
- [ ] Tested uninstall process

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Tested on multiple platforms (if applicable)
- [ ] Added examples for new features

## Related Issues
Fixes #issue_number
Related to #issue_number

## Screenshots (if applicable)
[Add screenshots here]
```

---

## 🧪 Testing Guidelines

### Manual Testing

1. **Installation Testing**
   ```bash
   # Fresh install
   ./install.sh

   # Check created directories
   ls -la ~/cot-framework
   ls -la ~/.claude/agents

   # Verify aliases
   cot-version
   cot-docs
   cot-agents
   ```

2. **Agent Testing**
   ```bash
   # Test each agent
   cot /use agent-code-reviewer "test task"
   cot /use agent-test-engineer "test task"
   cot /use agent-security-auditor "test task"
   cot /use agent-team-architect "test task"
   ```

3. **Uninstall Testing**
   ```bash
   ./uninstall.sh
   # Verify cleanup
   ls ~/cot-framework  # should not exist
   cat ~/.bashrc | grep cot  # should be empty
   ```

### Platform Testing

Test on different platforms when possible:
- Ubuntu/Debian Linux
- macOS (Intel and Apple Silicon if possible)
- Windows WSL
- Different shells (bash, zsh)

---

## 🐛 Bug Report Template

```markdown
## Bug Description
Clear, concise description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., Ubuntu 22.04, macOS 13.0, Windows 11 WSL]
- Shell: [e.g., bash 5.1, zsh 5.8]
- Framework Version: [run `cot-version`]
- Claude Code Version: [if applicable]

## Logs/Screenshots
[Paste error messages or attach screenshots]

## Additional Context
Any other relevant information
```

---

## 💡 Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches did you consider?

## Use Cases
Specific scenarios where this would be useful:
1. Use case 1
2. Use case 2

## Implementation Complexity
Your assessment: [Low / Medium / High]

## Additional Context
Any mockups, examples, or references
```

---

## 🏗️ Agent Development Guide

### Creating a New Agent

1. **Define Purpose**
   - What specific problem does the agent solve?
   - What makes it different from existing agents?
   - Who is the target user?

2. **Design Capabilities**
   - List core capabilities
   - Define input/output formats
   - Specify CoT integration points

3. **Implement Structure**
   ```markdown
   # Agent Name
   ## Role and Purpose
   ## Core Capabilities
   ## Chain of Thought Framework Integration
   ### ANALYZE Phase
   ### PLAN Phase
   ### VALIDATE Phase
   ### IMPLEMENT Phase
   ### CONFIRM Phase
   ## Example Usage
   ## Best Practices
   ```

4. **Add Examples**
   - Include 3-5 practical examples
   - Show different intensity levels
   - Demonstrate edge cases

5. **Test Thoroughly**
   - Test with cot, cot+, cot++
   - Verify output quality
   - Check error handling

6. **Document**
   - Update README.md
   - Add to agent list
   - Include usage examples

### Agent Quality Checklist

- [ ] Clear role and purpose defined
- [ ] Core capabilities listed
- [ ] CoT framework integration for all 5 phases
- [ ] Practical examples included (min. 3)
- [ ] Best practices documented
- [ ] Error handling considered
- [ ] Version and compatibility noted
- [ ] Tested with all intensity levels

---

## 📞 Getting Help

### Questions?
- Open a GitHub Discussion
- Check existing documentation
- Review examples in `/examples/`

### Not Sure Where to Start?
Look for issues labeled:
- `good first issue`
- `help wanted`
- `documentation`

### Join the Community
- Star the repository to show support
- Watch for updates
- Share your use cases and feedback

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive Behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable Behavior:**
- Harassment, trolling, or insulting comments
- Personal or political attacks
- Public or private harassment
- Publishing others' private information
- Other conduct reasonably considered inappropriate

### Enforcement

Instances of unacceptable behavior may be reported to project maintainers. All complaints will be reviewed and investigated and will result in a response deemed necessary and appropriate to the circumstances.

---

## 🎉 Recognition

Contributors will be recognized in:
- GitHub contributors list
- Future CHANGELOG entries
- Project documentation (with permission)

Thank you for contributing to making the Unified CoT Framework better! 🚀
