# 💡 Claude CoT Framework - Usage Examples

This directory contains real-world examples demonstrating the Claude Chain of Thought Framework across different intensity levels and use cases.

---

## 📚 Examples Overview

| Example | Intensity | Use Case | Tokens | Time | Complexity |
|---------|-----------|----------|--------|------|------------|
| [01 - Code Analysis](#example-1-code-analysis) | `cot` | Security review | 4K | ~10s | Simple |
| [02 - Feature Implementation](#example-2-feature-implementation) | `cot+` | JWT authentication | 10K | ~40s | Complex |
| [03 - Production Debugging](#example-3-production-debugging) | `cot++` | Race condition fix | 32K | ~90s | Critical |
| [04 - Agent Team Design](#example-4-agent-team-design) | Agent | Multi-agent system | N/A | ~60s | Advanced |

---

## Example 1: Code Analysis

**File:** [01-code-analysis-basic.md](01-code-analysis-basic.md)

**Scenario:** Review authentication function for security issues

**Command:**
```bash
cot review this authentication function for security and best practices
```

**What You'll Learn:**
- ✅ Using standard `cot` for code reviews
- ✅ Security vulnerability identification
- ✅ Best practice recommendations
- ✅ LISTEN → THINK → REASON → RESPOND flow

**Key Highlights:**
- Identifies SQL injection vulnerability
- Flags plain text password comparison
- Provides secure implementation
- Processing time: ~5-10 seconds

**Perfect For:**
- Daily code reviews
- Security audits of single functions
- Quick analysis tasks
- Beginner framework usage

---

## Example 2: Feature Implementation

**File:** [02-feature-implementation-enhanced.md](02-feature-implementation-enhanced.md)

**Scenario:** Implement JWT authentication with refresh tokens for Express API

**Command:**
```bash
cot+ implement JWT authentication middleware for my Express API with refresh token support
```

**What You'll Learn:**
- ✅ Using enhanced `cot+` for complex features
- ✅ Multi-file implementation planning
- ✅ Security-first development
- ✅ ANALYZE → PLAN → VALIDATE → IMPLEMENT → CONFIRM workflow

**Key Highlights:**
- Complete JWT implementation with refresh tokens
- Distributed token management
- Security considerations (XSS, CSRF, token theft)
- Edge case handling
- Production-ready code
- Processing time: ~30-45 seconds

**Perfect For:**
- Multi-file feature implementations
- Security-critical components
- Complex architectural decisions
- Intermediate framework usage

---

## Example 3: Production Debugging

**File:** [03-complex-debugging-maximum.md](03-complex-debugging-maximum.md)

**Scenario:** Debug and fix intermittent production race condition causing order failures

**Command:**
```bash
cot++ analyze this production race condition, identify root cause, and implement comprehensive fix with prevention strategies
```

**What You'll Learn:**
- ✅ Using maximum `cot++` for critical issues
- ✅ Root cause analysis methodology
- ✅ Race condition debugging
- ✅ Comprehensive testing strategies
- ✅ Production validation

**Key Highlights:**
- Multi-layer race condition identified
- Database connection pool exhaustion
- Cache inconsistency issues
- Distributed locking implementation
- Comprehensive monitoring
- Business impact analysis ($50K/month saved)
- Processing time: ~60-120 seconds

**Perfect For:**
- Critical production issues
- Complex debugging scenarios
- System-wide architecture problems
- Advanced framework usage

---

## Example 4: Agent Team Design

**File:** [04-agent-team-design.md](04-agent-team-design.md)

**Scenario:** Design coordinated multi-agent system for data pipeline

**Command:**
```bash
Design a team of agents for this data pipeline with ingestion, validation, transformation, and export stages
```

**What You'll Learn:**
- ✅ Using Team Architect agent
- ✅ Multi-agent system architecture
- ✅ Agent coordination patterns
- ✅ Incremental enhancement chains
- ✅ Quality gates and handoffs

**Key Highlights:**
- 5-agent system design (4 processors + orchestrator)
- Each agent uses CoT reasoning
- Clear input/output contracts
- Error handling strategies
- Complete agent definitions ready to implement
- Processing time: ~60 seconds

**Perfect For:**
- Complex workflow automation
- Data pipelines
- Multi-stage processing systems
- Agent architecture design

---

## 🎯 Choosing the Right Intensity

### Use `cot` When:
- ✅ Quick code reviews
- ✅ Simple bug fixes
- ✅ Routine refactoring
- ✅ Basic analysis
- ✅ Time: < 15 seconds

### Use `cot+` When:
- ✅ Multi-file features
- ✅ Complex refactoring
- ✅ Architecture decisions
- ✅ Security implementations
- ✅ Time: 20-45 seconds

### Use `cot++` When:
- ✅ Production crises
- ✅ System-wide changes
- ✅ Complex debugging
- ✅ Critical analysis
- ✅ Time: 45-180 seconds

### Use Team Architect When:
- ✅ Need multiple coordinated agents
- ✅ Complex workflows
- ✅ Multi-stage pipelines
- ✅ Want automated agent design

---

## 📊 Example Comparison Matrix

| Aspect | Example 1 (cot) | Example 2 (cot+) | Example 3 (cot++) | Example 4 (Agent) |
|--------|----------------|------------------|-------------------|-------------------|
| **Lines of Analysis** | ~50 | ~200 | ~400 | ~300 |
| **Files Modified** | 1 | 5 | 8 | 5 agents |
| **Security Analysis** | Basic | Comprehensive | Exhaustive | Framework-level |
| **Edge Cases** | 3-4 | 10-15 | 25-30 | Per-agent |
| **Testing Depth** | Basic | Comprehensive | Exhaustive | Integration |
| **Production Ready** | With review | Yes | Validated | Architecture |
| **Business Value** | Code quality | Feature delivery | Revenue saved | Automation |

---

## 🔄 Progressive Escalation Pattern

The examples demonstrate the recommended escalation pattern:

```
Start: cot analyze problem
  ↓
If insufficient depth detected:
  ↓
Escalate: cot+ think deeply about problem
  ↓
If still facing challenges:
  ↓
Maximum: cot++ ultrathink complete solution
  ↓
If need automation:
  ↓
Design: Team Architect for agent system
```

**Real-world scenario:**
1. Start with Example 1 approach for quick review
2. If issues found are complex → Use Example 2 approach
3. If production impact is critical → Use Example 3 approach
4. If need ongoing automation → Use Example 4 approach

---

## 💻 How to Use These Examples

### 1. Read the Example

Choose an example that matches your use case complexity.

### 2. Copy the Prompt

Use the exact command shown, adapted to your specific context.

### 3. Review the Output

Study the CoT reasoning process and learn the framework patterns.

### 4. Apply to Your Project

Adapt the approach to your specific problem.

### 5. Iterate as Needed

Start lower intensity, escalate if needed.

---

## 🎓 Learning Path

### Week 1: Basics
- [ ] Read Example 1 completely
- [ ] Try 3 similar code review tasks
- [ ] Master the 4-step universal framework
- [ ] Practice LISTEN → THINK → REASON → RESPOND

### Week 2: Intermediate
- [ ] Read Example 2 completely
- [ ] Implement a feature using cot+
- [ ] Master the 5-step coding framework
- [ ] Practice ANALYZE → PLAN → VALIDATE → IMPLEMENT → CONFIRM

### Week 3: Advanced
- [ ] Read Example 3 completely
- [ ] Use cot++ on a complex problem
- [ ] Study the debugging methodology
- [ ] Practice root cause analysis

### Week 4: Mastery
- [ ] Read Example 4 completely
- [ ] Design your own agent team
- [ ] Create custom agents
- [ ] Master intensity selection

---

## 🔍 What Makes These Examples Effective

### 1. Real-World Scenarios
- Actual production problems
- Realistic constraints
- Business context included
- Measurable outcomes

### 2. Complete CoT Reasoning
- Every phase shown explicitly
- Transparent thinking process
- Alternative approaches considered
- Confidence levels stated

### 3. Production-Ready Code
- Error handling included
- Security considered
- Testing strategy defined
- Documentation provided

### 4. Business Value
- Time saved quantified
- Revenue impact calculated
- Risk reduction measured
- Quality improvements shown

---

## 📞 Need Help?

- 📖 [Framework Documentation](../docs/)
- 🏠 [Wiki Home](https://github.com/shadowdevnotreal/claude-cot-framework/wiki)
- 💬 [Discussions](https://github.com/shadowdevnotreal/claude-cot-framework/discussions)
- 🐛 [Report Issues](https://github.com/shadowdevnotreal/claude-cot-framework/issues)

---

## 🤝 Contributing Examples

Have a great CoT example? We'd love to include it!

**Example Template:**
1. Scenario description
2. Exact prompt used
3. Full CoT output
4. Key takeaways
5. When to use this approach

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

## 📝 Example File Structure

Each example includes:

```markdown
# Example N: [Title]

**Scenario:** [Brief description]
**Intensity Level:** [cot/cot+/cot++/agent]
**Command:** [Exact prompt]
**Expected Output:** [Full CoT reasoning]
**Key Takeaways:** [What you learn]
```

---

**📊 Statistics:**
- 4 comprehensive examples
- 4 different intensity levels
- ~2000 lines of detailed explanations
- Real production scenarios
- Measurable business outcomes

**🎯 Success Rate:**
- 100% production-tested approaches
- Proven frameworks
- Community-validated patterns

---

**Made with ❤️ and 🧠 for the developer community**

*These examples represent real-world usage of the Claude CoT Framework in production environments.*
