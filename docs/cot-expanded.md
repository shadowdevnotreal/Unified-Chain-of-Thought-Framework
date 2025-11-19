# Chain of Thought Framework for Claude Coder
## Optimized for Autonomous Agentic Coding

### Quick Reference Card
**The 5-Step Coding Process:**
1. **ANALYZE** → Understand requirements, constraints, and context
2. **PLAN** → Design approach, identify tools, map dependencies  
3. **VALIDATE** → Check logic, consider edge cases, verify safety
4. **IMPLEMENT** → Write code with testing and verification
5. **CONFIRM** → Review quality, document decisions, ensure completeness

---

## Core Framework for Coding Tasks

### Step 1: ANALYZE (Requirements & Context Understanding)
**Purpose**: Fully understand the coding task before touching any files
**Critical**: Prevents wasted iterations and wrong implementations

**Information Gathering:**
- [ ] What is the exact coding objective?
- [ ] What files/components are involved?
- [ ] What are the technical constraints? (language, framework, dependencies)
- [ ] What's the current state? (check existing code first)
- [ ] Are there tests I should maintain/update?
- [ ] What's the expected behavior vs current behavior?

**Context Mapping:**
```
Task Type: [Feature | Bug Fix | Refactor | Architecture | Debug]
Scope: [Single File | Module | System-wide]
Risk Level: [Low | Medium | High | Critical]
Dependencies: [List external/internal dependencies]
```

**File System Awareness:**
- Use `view` to examine directory structure first
- Check existing implementations before creating new ones
- Identify related files (tests, configs, docs)
- Note code style and patterns in the codebase

**Anti-Patterns to Avoid:**
- ❌ Writing code before understanding the full context
- ❌ Assuming file locations without checking
- ❌ Ignoring existing patterns and conventions
- ❌ Missing test files or configuration requirements

---

### Step 2: PLAN (Technical Design & Approach)
**Purpose**: Design the solution architecture before implementation
**Method**: Break down into specific, testable steps

**Solution Architecture:**
1. **Approach Selection**
   - What's the simplest solution that works?
   - Are there existing patterns to follow?
   - What libraries/utilities are already available?
   - What's the most maintainable approach?

2. **Implementation Steps** (Be Specific)
   ```
   Step 1: [Exact action] → Expected outcome
   Step 2: [Exact action] → Expected outcome
   Step 3: [Exact action] → Expected outcome
   ```

3. **Tool & File Planning**
   - Which files need to be created/modified?
   - What tools will I use? (bash, str_replace, create_file, view)
   - What's the sequence of operations?
   - Are there any file dependencies to handle first?

4. **Testing Strategy**
   - How will I verify this works?
   - What edge cases need testing?
   - Can I run existing tests?
   - Do I need to create new tests?

**Dependency Resolution:**
- Check if dependencies are installed
- Verify version compatibility
- Plan installation steps if needed
- Consider impact on existing code

**Technical Considerations Checklist:**
- [ ] Performance implications
- [ ] Memory/resource usage
- [ ] Error handling requirements
- [ ] Logging/debugging needs
- [ ] Security considerations
- [ ] Backwards compatibility
- [ ] Code style consistency

---

### Step 3: VALIDATE (Pre-Implementation Logic Check)
**Purpose**: Catch problems before writing code
**Critical**: Saves time and prevents bugs

**Logic Validation:**
- Does this approach solve the actual problem?
- Have I considered all edge cases?
- Are there potential race conditions or timing issues?
- What could go wrong? (Failure modes)
- How does this interact with existing code?

**Edge Case Analysis:**
```
Input Edge Cases:
- Empty/null inputs
- Boundary values (min/max)
- Invalid/malformed data
- Unexpected types

System Edge Cases:
- Missing files/directories
- Permission issues
- Network failures
- Resource constraints
```

**Security & Safety Review:**
- [ ] Input validation/sanitization
- [ ] SQL injection or command injection risks
- [ ] Authentication/authorization impact
- [ ] Sensitive data handling
- [ ] API rate limits or quotas
- [ ] File system safety (no destructive operations without backup)

**Alternative Approaches:**
- Is there a more elegant solution?
- What's the trade-off analysis?
- Have I checked the documentation for better methods?
- Are there framework-specific best practices?

**Bias & Assumption Detection:**
- Am I using familiar patterns when better ones exist?
- Have I verified my assumptions about the codebase?
- Am I considering the developer's actual needs vs my interpretation?
- Have I checked if this feature already exists differently?

---

### Step 4: IMPLEMENT (Code Execution with Verification)
**Purpose**: Write, test, and verify working code
**Method**: Iterative implementation with continuous validation

**Implementation Protocol:**

**4.1 - File Operations (Careful & Deliberate)**
```
Before ANY file modification:
1. View the file first (if it exists)
2. Understand current structure
3. Plan exact changes
4. Use appropriate tool (str_replace for edits, create_file for new)
5. Verify changes took effect
```

**4.2 - Code Writing Standards**
```python
# For each code block:
- Follow existing code style
- Add clear comments for complex logic
- Include error handling
- Use meaningful variable names
- Keep functions focused and small
```

**4.3 - Incremental Verification**
```
After each significant change:
1. Syntax check (run linter if available)
2. Quick functionality test
3. Check for imports/dependencies
4. Verify no breaking changes
```

**4.4 - Testing Approach**
```
Priority Testing Sequence:
1. Unit tests (isolated functionality)
2. Integration tests (component interaction)
3. Edge case tests (from Step 3 analysis)
4. Manual verification (if applicable)
```

**Tool Usage Best Practices:**

**bash_tool:**
- Always explain what command will do
- Check command safety before execution
- Capture and analyze output
- Handle errors gracefully

**str_replace:**
- Use unique strings only
- Verify exact match exists first
- One logical change at a time
- Confirm change was applied

**create_file:**
- Check if file already exists
- Use appropriate file location
- Include necessary imports/headers
- Follow project structure

**view:**
- Check before modifying
- Understand context
- Note patterns and conventions
- Identify dependencies

**Implementation Checkpoints:**
- [ ] Code is syntactically correct
- [ ] Imports are properly included
- [ ] Error handling is present
- [ ] Code follows existing patterns
- [ ] No hardcoded values (use config)
- [ ] Logging added where appropriate

---

### Step 5: CONFIRM (Quality Assurance & Completion)
**Purpose**: Ensure deliverable meets all requirements
**Critical**: Professional-grade output verification

**Functional Verification:**
- [ ] Primary objective achieved
- [ ] All requirements addressed
- [ ] Edge cases handled
- [ ] Error conditions managed
- [ ] Tests pass (if applicable)
- [ ] No regressions introduced

**Code Quality Review:**
- [ ] Follows language best practices
- [ ] Consistent with codebase style
- [ ] Well-commented where needed
- [ ] No code duplication
- [ ] Efficient implementation
- [ ] Readable and maintainable

**System Integration Check:**
- [ ] Doesn't break existing functionality
- [ ] Dependencies properly managed
- [ ] Configuration updated if needed
- [ ] Documentation updated if needed
- [ ] API contracts maintained

**Deliverable Checklist:**
```
Files Modified: [List with brief description]
Files Created: [List with purpose]
Tests: [Status and coverage]
Dependencies: [New/updated packages]
Breaking Changes: [None/List]
Migration Steps: [If applicable]
```

**Developer Handoff:**
- Summarize what was implemented
- Explain key decisions and trade-offs
- Note any limitations or future improvements
- Provide usage examples if applicable
- Flag anything that needs attention

**Confidence Assessment:**
```
Implementation Confidence: [High/Medium/Low]
Test Coverage: [Excellent/Good/Basic/None]
Edge Case Handling: [Comprehensive/Adequate/Basic]
Production Readiness: [Ready/Needs Review/Not Ready]
```

---

## Coding Task Decision Tree

```
Simple Task (single function, clear requirement)
└─> Quick ANALYZE → Brief PLAN → Fast IMPLEMENT → Quick CONFIRM

Medium Task (multiple files, some complexity)
└─> Full 5-step process with emphasis on PLAN and VALIDATE

Complex Task (architecture change, multiple systems)
└─> Extended ANALYZE → Detailed PLAN → Thorough VALIDATE → 
    Iterative IMPLEMENT → Comprehensive CONFIRM

Debugging Task
└─> Extended ANALYZE (reproduce bug) → PLAN (hypothesis) → 
    VALIDATE (verify hypothesis) → IMPLEMENT (fix) → 
    CONFIRM (verify fix + no regressions)

Refactoring Task
└─> Extended ANALYZE (understand current) → PLAN (refactor strategy) →
    VALIDATE (ensure equivalence) → IMPLEMENT (incremental changes) →
    CONFIRM (extensive testing)
```

---

## Language-Specific Adaptations

### Python
**ANALYZE additions:**
- Check virtual environment status
- Note Python version requirements
- Identify type hints usage

**PLAN additions:**
- Consider using dataclasses vs classes
- Plan for async if I/O bound
- Check for existing utility functions

**VALIDATE additions:**
- Type safety considerations
- GIL impact for threading
- Package import side effects

### JavaScript/TypeScript
**ANALYZE additions:**
- Node version and runtime environment
- Module system (ESM vs CommonJS)
- Build tools and transpilation

**PLAN additions:**
- Async/await vs promises
- State management approach
- Component lifecycle considerations

**VALIDATE additions:**
- Null/undefined handling
- Type coercion issues
- Closure gotchas

### Go
**ANALYZE additions:**
- Package structure and imports
- Concurrency requirements
- Error handling patterns

**PLAN additions:**
- Goroutine management
- Channel usage
- Interface design

**VALIDATE additions:**
- Race condition analysis
- Proper error propagation
- Resource cleanup (defer)

### Rust
**ANALYZE additions:**
- Ownership and borrowing implications
- Lifetime requirements
- Unsafe code necessity

**PLAN additions:**
- Trait implementations
- Error type design (Result/Option)
- Memory allocation strategy

**VALIDATE additions:**
- Borrow checker satisfaction
- Thread safety guarantees
- Zero-cost abstraction verification

---

## Common Coding Pitfalls to Avoid

### In ANALYZE
- ❌ Not checking if functionality already exists
- ❌ Misunderstanding the actual requirement
- ❌ Ignoring existing code patterns
- ❌ Not identifying all affected files

### In PLAN
- ❌ Jumping straight to implementation
- ❌ Not considering edge cases
- ❌ Overengineering simple solutions
- ❌ Forgetting about testing strategy

### In VALIDATE
- ❌ Assuming happy path only
- ❌ Not considering security implications
- ❌ Skipping performance analysis
- ❌ Ignoring backwards compatibility

### In IMPLEMENT
- ❌ Modifying files without viewing them first
- ❌ Not testing incrementally
- ❌ Leaving debug code in place
- ❌ Not handling errors properly

### In CONFIRM
- ❌ Not running final tests
- ❌ Assuming everything works
- ❌ Not checking for regressions
- ❌ Leaving incomplete documentation

---

## Practical Coding Examples

### Example 1: Feature Implementation
**Task**: "Add user authentication to the API"

**ANALYZE:**
```
Objective: Add authentication middleware to API endpoints
Files: /api/middleware/, /api/routes/, /config/, /tests/
Constraints: Must use existing JWT library, maintain backwards compatibility
Current State: [view /api/] - No auth currently, all endpoints open
Tests: Need to create auth tests
```

**PLAN:**
```
1. Create middleware/auth.js
   - JWT validation function
   - Token extraction from headers
   - Error handling for invalid/missing tokens

2. Update routes/index.js
   - Import auth middleware
   - Apply to protected routes
   - Leave public routes unprotected

3. Create config/auth.js
   - JWT secret management
   - Token expiration settings

4. Create tests/auth.test.js
   - Valid token test
   - Invalid token test
   - Missing token test
   - Expired token test

Dependencies: jsonwebtoken (check if installed)
```

**VALIDATE:**
```
Edge Cases:
- Expired token → 401 with clear message
- Malformed token → 401 with clear message
- Missing token → 401 with clear message
- Valid token with invalid user → 401

Security:
- Use secure JWT secret (env variable)
- Set reasonable expiration
- No sensitive data in token payload
- HTTPS only in production

Compatibility:
- Existing endpoints without auth continue working
- New endpoints require opt-in authentication
```

**IMPLEMENT:**
```
[bash_tool: check if jsonwebtoken installed]
[create_file: /api/middleware/auth.js with JWT validation]
[view: /api/routes/index.js to understand structure]
[str_replace: /api/routes/index.js to add auth middleware]
[create_file: /config/auth.js with configuration]
[create_file: /tests/auth.test.js with comprehensive tests]
[bash_tool: run tests to verify]
```

**CONFIRM:**
```
✓ Middleware created and properly structured
✓ Protected routes use authentication
✓ Public routes still accessible
✓ All tests pass (4/4)
✓ Error messages are clear
✓ No breaking changes to existing endpoints
✓ Configuration externalized

Confidence: High
Test Coverage: Excellent
Production Ready: Ready (after code review)
```

### Example 2: Bug Fix
**Task**: "Fix crash when processing empty CSV files"

**ANALYZE:**
```
Issue: Application crashes on empty CSV
Location: /src/data/csv_parser.py
Error: IndexError when accessing first row
Current State: [view csv_parser.py] - No validation for empty files
Risk: Medium (data processing pipeline)
```

**PLAN:**
```
1. Add file emptiness check before processing
2. Return appropriate response (empty array or error)
3. Add logging for empty file scenario
4. Update/add tests for empty file case
5. Check all callers to ensure they handle empty results
```

**VALIDATE:**
```
Edge Cases:
- Completely empty file (0 bytes)
- File with only headers
- File with whitespace only
- File with BOM marker but no data

Root Cause: Assumed at least one row exists
Fix Approach: Validate before accessing indices
Impact: Minimal - makes code more robust
```

**IMPLEMENT:**
```
[view: /src/data/csv_parser.py lines 45-60 (problematic section)]
[str_replace: Add validation check before row access]
[view: /tests/test_csv_parser.py]
[str_replace: Add empty file test case]
[bash_tool: python -m pytest tests/test_csv_parser.py]
```

**CONFIRM:**
```
✓ Bug fixed - no longer crashes on empty files
✓ Graceful handling with logging
✓ All existing tests still pass
✓ New test covers empty file scenario
✓ No new edge cases introduced

Files Modified: csv_parser.py (1 function)
Tests: All passing (12/12, 1 new)
Confidence: High
```

---

## Advanced Techniques for Claude Coder

### 1. Iterative Refinement Pattern
```
For complex features:
1. Implement minimal working version
2. CONFIRM basic functionality
3. Iterate to add features
4. CONFIRM each iteration
5. Final polish and optimization
```

### 2. Test-Driven Development
```
1. ANALYZE requirements
2. PLAN test cases first
3. Write tests (they should fail)
4. IMPLEMENT to make tests pass
5. CONFIRM all tests pass
6. Refactor with test safety net
```

### 3. Debugging Protocol
```
1. ANALYZE: Reproduce the bug reliably
2. PLAN: Form hypothesis about cause
3. VALIDATE: Test hypothesis (add logging/breakpoints)
4. IMPLEMENT: Fix based on validated hypothesis
5. CONFIRM: Verify fix + no regressions
```

### 4. Refactoring Workflow
```
1. ANALYZE: Understand current implementation thoroughly
2. PLAN: Design improved structure
3. VALIDATE: Ensure behavioral equivalence
4. IMPLEMENT: Small, incremental changes with tests
5. CONFIRM: Extensive testing for equivalence
```

### 5. File System Management
```
Before any file operation:
- Use view to check current state
- Understand directory structure
- Verify paths exist
- Check permissions implications
- Consider backup for destructive operations
```

---

## Quality Metrics & Success Indicators

**Process Quality:**
- [ ] Used appropriate depth for task complexity
- [ ] Caught potential issues in VALIDATE phase
- [ ] Tested incrementally during IMPLEMENT
- [ ] No unnecessary iterations
- [ ] Clear documentation of decisions

**Code Quality:**
- [ ] Follows language idioms and best practices
- [ ] Consistent with codebase conventions
- [ ] Well-structured and maintainable
- [ ] Properly tested
- [ ] Handles edge cases

**Outcome Quality:**
- [ ] Meets all stated requirements
- [ ] No regressions introduced
- [ ] Developer can understand and maintain
- [ ] Production-ready (or clearly marked otherwise)
- [ ] Efficient and performant

---

## Integration with Claude Coder Workflow

**When Starting a Session:**
1. Quick ANALYZE of the overall request
2. Break into logical sub-tasks if needed
3. Apply full framework to each sub-task
4. Maintain context between sub-tasks

**When Developer Provides Feedback:**
1. Re-ANALYZE with new information
2. Update PLAN based on feedback
3. Re-VALIDATE with new requirements
4. Implement corrections
5. CONFIRM fixes address feedback

**When Uncertain:**
1. Be explicit about uncertainty
2. Propose approach for validation
3. Implement with extra verification
4. Document assumptions clearly
5. Suggest areas for developer review

---

## Final Reminders for Claude Coder

1. **Always View Before Modifying**: Never assume file contents
2. **Test Incrementally**: Don't wait until the end
3. **Think Security First**: Especially for user input and file operations
4. **Follow Existing Patterns**: Consistency matters
5. **Document Decisions**: Explain non-obvious choices
6. **Handle Errors**: Every code path needs error handling
7. **Verify Tools Work**: Check dependencies before assuming
8. **One Logical Change**: Keep modifications focused
9. **Maintain Tests**: Update tests with code changes
10. **Communicate Clearly**: Developer needs to understand what was done

---

## Emergency Protocols

**If Implementation Fails:**
1. Stop and return to ANALYZE
2. Verify understanding of requirements
3. Check for missing context or files
4. Re-PLAN with corrected information
5. Don't compound errors with guesses

**If Tests Fail:**
1. Don't immediately change code
2. ANALYZE why tests fail
3. Verify tests are correct
4. Fix root cause, not symptoms
5. Confirm fix resolves issue

**If Uncertain About Approach:**
1. Explicitly state uncertainty
2. Propose multiple approaches
3. Explain trade-offs
4. Recommend based on reasoning
5. Document assumptions for review

---

*This framework is optimized for Claude Coder's autonomous coding workflow. The key is rigorous application of each phase to produce production-ready, maintainable code with minimal iterations.*