#!/bin/bash

# Agent Creation Wizard for Unified CoT Framework
# Version: 1.0.0
# Creates custom agent templates following framework standards

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
AGENTS_DIR="$HOME/.claude/agents"
LOCAL_AGENTS_DIR="$(pwd)/agents"
TEMPLATE_VERSION="2.0.0"

print_header() {
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  Unified CoT Framework - Agent Creation Wizard${NC}"
    echo -e "${BLUE}  Version $TEMPLATE_VERSION${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

prompt_user() {
    local prompt="$1"
    local variable_name="$2"
    local default_value="$3"

    if [ -n "$default_value" ]; then
        echo -ne "${BLUE}${prompt}${NC} [${default_value}]: "
    else
        echo -ne "${BLUE}${prompt}${NC}: "
    fi

    read -r user_input

    if [ -z "$user_input" ] && [ -n "$default_value" ]; then
        eval "$variable_name=\"$default_value\""
    else
        eval "$variable_name=\"$user_input\""
    fi
}

# Validate agent name
validate_agent_name() {
    local name="$1"

    # Check if name is empty
    if [ -z "$name" ]; then
        print_error "Agent name cannot be empty"
        return 1
    fi

    # Check if name contains only allowed characters
    if ! [[ "$name" =~ ^[a-z-]+$ ]]; then
        print_error "Agent name can only contain lowercase letters and hyphens"
        return 1
    fi

    # Check if agent already exists
    if [ -f "$LOCAL_AGENTS_DIR/agent-$name.md" ]; then
        print_warning "Agent 'agent-$name.md' already exists in local directory"
        prompt_user "Overwrite existing agent?" overwrite "n"
        if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
            return 1
        fi
    fi

    return 0
}

# Generate agent template
generate_agent_template() {
    local agent_name="$1"
    local agent_title="$2"
    local agent_purpose="$3"
    local agent_capabilities="$4"
    local author="$5"
    local date="$(date +%Y-%m-%d)"

    cat > "$LOCAL_AGENTS_DIR/agent-$agent_name.md" << EOF
# ${agent_title}

## Role and Purpose

${agent_purpose}

## Core Capabilities

${agent_capabilities}

## Chain of Thought Framework Integration

### ANALYZE Phase (CoT: Standard → Enhanced)

\`\`\`
ANALYZE {
  [Agent Name] Analysis:
    Input:
      - [Describe what input this agent requires]
      - [List relevant context needed]
      - [Specify any constraints or requirements]

    Process:
      1. [First analysis step]:
         - [Substep 1]
         - [Substep 2]
         - [Substep 3]

      2. [Second analysis step]:
         - [Substep 1]
         - [Substep 2]

      3. [Third analysis step]:
         - [Evaluation criteria]
         - [Metrics to collect]

    Output:
      [agent-name]-analysis.json:
      {
        "key_findings": [...],
        "metrics": {...},
        "issues_identified": [...],
        "recommendations": [...]
      }

  Validation Gates:
    ✓ [First validation check]
    ✓ [Second validation check]
    ✓ [Third validation check]
}
\`\`\`

### PLAN Phase (CoT: Enhanced)

\`\`\`
PLAN {
  [Agent Name] Strategy:
    Input:
      - [agent-name]-analysis.json
      - [Other required inputs]

    Process:
      1. Define approach:
         - [Strategy element 1]
         - [Strategy element 2]
         - [Strategy element 3]

      2. Create execution plan:
         Phase 1 - [Phase name] (Timeline):
           ✓ [Task 1]
           ✓ [Task 2]
           ✓ [Task 3]
           Expected outcome: [Description]

         Phase 2 - [Phase name] (Timeline):
           ✓ [Task 1]
           ✓ [Task 2]
           Expected outcome: [Description]

      3. Define success criteria:
         - [Success metric 1]
         - [Success metric 2]
         - [Success metric 3]

    Output:
      [agent-name]-plan.json:
      {
        "phases": [...],
        "success_criteria": {...},
        "timeline": "[estimated timeline]",
        "resources_needed": [...]
      }

  Validation Gates:
    ✓ [Planning validation 1]
    ✓ [Planning validation 2]
    ✓ [Planning validation 3]
}
\`\`\`

### VALIDATE Phase (CoT: Enhanced → Maximum)

\`\`\`
VALIDATE {
  [Agent Name] Validation Protocol:

    1. [Validation Category 1]:
       Checks:
         ✓ [Check 1]
         ✓ [Check 2]
         ✓ [Check 3]

       Testing method:
         - [How to test this]
         - [Acceptance criteria]

    2. [Validation Category 2]:
       Checks:
         ✓ [Check 1]
         ✓ [Check 2]

       Testing method:
         - [How to test this]

    3. [Validation Category 3]:
       Automated tests:
         \`\`\`bash
         # Example test command
         [test-command] [arguments]
         \`\`\`

       Expected results:
         - [Expected outcome 1]
         - [Expected outcome 2]

  Validation Gates:
    ✓ [Final validation gate 1]
    ✓ [Final validation gate 2]
    ✓ [Final validation gate 3]
}
\`\`\`

### IMPLEMENT Phase (CoT: Standard → Enhanced)

\`\`\`
IMPLEMENT {
  [Agent Name] Implementation:

    1. [Implementation Area 1]:

       Example:
       \`\`\`[language]
       // Code example showing implementation
       // Be specific and practical
       [code-example]
       \`\`\`

    2. [Implementation Area 2]:

       Step-by-step:
         1. [Step 1 with explanation]
         2. [Step 2 with explanation]
         3. [Step 3 with explanation]

       Example:
       \`\`\`[language]
       [code-example]
       \`\`\`

    3. [Implementation Area 3]:

       Best practices:
         - [Best practice 1]
         - [Best practice 2]
         - [Best practice 3]

  Common Patterns:
    - [Pattern 1]: [Description and when to use]
    - [Pattern 2]: [Description and when to use]
    - [Pattern 3]: [Description and when to use]
}
\`\`\`

### CONFIRM Phase (CoT: Enhanced)

\`\`\`
CONFIRM {
  [Agent Name] Completion Audit:

    1. [Audit Category 1]:
       ✓ [Completion check 1]
       ✓ [Completion check 2]
       ✓ [Completion check 3]

    2. [Audit Category 2]:
       Quality Metrics:
         - [Metric 1]: [Target] → [Actual] ✓
         - [Metric 2]: [Target] → [Actual] ✓
         - [Metric 3]: [Target] → [Actual] ✓

    3. [Audit Category 3]:
       Deliverables:
         ✓ [Deliverable 1] complete
         ✓ [Deliverable 2] complete
         ✓ [Deliverable 3] complete

  Final Checklist:
    ✓ [Final check 1]
    ✓ [Final check 2]
    ✓ [Final check 3]
    ✓ [Final check 4]
    ✓ [Final check 5]

  Status: APPROVED ✅

  Recommendations:
    - [Recommendation 1]
    - [Recommendation 2]
    - [Recommendation 3]
}
\`\`\`

## Example Usage

### Example 1: [Scenario Name] (cot)

\`\`\`
User: "[Example user request]"

Claude with ${agent_title} (cot):

ANALYZE {
  [Brief analysis summary]
}

PLAN {
  [Brief plan summary]
}

IMPLEMENT {
  [Brief implementation summary]
}

CONFIRM {
  ✓ [Completion confirmation]
}
\`\`\`

### Example 2: [Advanced Scenario] (cot+)

\`\`\`
User: "[More complex user request]"

Claude with ${agent_title} (cot+):

[More detailed workflow example showing
 how the agent handles complex scenarios]
\`\`\`

### Example 3: [Critical Scenario] (cot++)

\`\`\`
User: "[Critical/comprehensive request]"

Claude with ${agent_title} (cot++):

[Full workflow example showing maximum
 thinking and comprehensive approach]
\`\`\`

## Best Practices

### 1. [Best Practice Category 1]

**Do:**
✅ [Recommendation 1]
✅ [Recommendation 2]
✅ [Recommendation 3]

**Don't:**
❌ [Anti-pattern 1]
❌ [Anti-pattern 2]
❌ [Anti-pattern 3]

### 2. [Best Practice Category 2]

- [Practice 1 with explanation]
- [Practice 2 with explanation]
- [Practice 3 with explanation]

### 3. [Best Practice Category 3]

\`\`\`[language]
// Example demonstrating best practice
[code-example]
\`\`\`

## Anti-Patterns to Avoid

❌ **[Anti-pattern 1]**: [Why it's bad and what to do instead]

❌ **[Anti-pattern 2]**: [Why it's bad and what to do instead]

❌ **[Anti-pattern 3]**: [Why it's bad and what to do instead]

## Integration Points

### With Other Agents

- **[Agent 1]**: [How this agent complements Agent 1]
- **[Agent 2]**: [How this agent works with Agent 2]
- **[Agent 3]**: [When to use this agent vs Agent 3]

### With CoT Intensity Levels

| Intensity | Use When | Expected Output |
|-----------|----------|-----------------|
| **cot**   | [Scenario for standard] | [What to expect] |
| **cot+**  | [Scenario for enhanced] | [What to expect] |
| **cot++** | [Scenario for maximum] | [What to expect] |

## Tools and Resources

### Recommended Tools
- **[Tool 1]**: [Purpose and usage]
- **[Tool 2]**: [Purpose and usage]
- **[Tool 3]**: [Purpose and usage]

### References
- [Reference 1 with link if applicable]
- [Reference 2 with link if applicable]
- [Reference 3 with link if applicable]

---

**Agent Version**: 1.0.0
**Created By**: ${author}
**Last Updated**: ${date}
**Compatible with**: Unified CoT Framework v${TEMPLATE_VERSION}+
**Recommended Intensity**: [cot/cot+/cot++] for [specific use case]
EOF

    print_success "Agent template generated: $LOCAL_AGENTS_DIR/agent-$agent_name.md"
}

# Copy to Claude directory
install_agent() {
    local agent_name="$1"
    local source="$LOCAL_AGENTS_DIR/agent-$agent_name.md"
    local dest="$AGENTS_DIR/agent-$agent_name.md"

    if [ ! -d "$AGENTS_DIR" ]; then
        print_warning "Claude agents directory not found: $AGENTS_DIR"
        prompt_user "Create it now?" create_dir "y"
        if [ "$create_dir" = "y" ] || [ "$create_dir" = "Y" ]; then
            mkdir -p "$AGENTS_DIR"
            print_success "Created directory: $AGENTS_DIR"
        else
            print_info "Agent saved locally only: $source"
            return 0
        fi
    fi

    cp "$source" "$dest"
    print_success "Agent installed to Claude: $dest"
    print_info "The agent is now available globally in all Claude Code sessions"
}

# Main wizard
main() {
    print_header

    print_info "This wizard will help you create a custom agent for the Unified CoT Framework"
    echo ""

    # Create local agents directory if it doesn't exist
    if [ ! -d "$LOCAL_AGENTS_DIR" ]; then
        mkdir -p "$LOCAL_AGENTS_DIR"
    fi

    # Gather agent information
    print_info "Step 1: Agent Basic Information"
    echo ""

    # Agent name
    while true; do
        prompt_user "Agent name (lowercase, hyphens only, e.g., 'my-agent')" agent_name
        if validate_agent_name "$agent_name"; then
            break
        fi
    done

    # Agent title
    prompt_user "Agent title (e.g., 'My Custom Agent')" agent_title "$(echo $agent_name | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g') Agent"

    echo ""
    print_info "Step 2: Agent Purpose"
    echo ""

    prompt_user "What is this agent's primary purpose? (1-2 sentences)" agent_purpose

    echo ""
    print_info "Step 3: Core Capabilities"
    echo ""
    echo -e "${BLUE}Enter agent capabilities (one per line, press Enter twice when done):${NC}"

    agent_capabilities=""
    while true; do
        read -r capability
        if [ -z "$capability" ]; then
            if [ -n "$agent_capabilities" ]; then
                break
            fi
        else
            agent_capabilities="${agent_capabilities}- ${capability}\n"
        fi
    done

    echo ""
    print_info "Step 4: Author Information"
    echo ""

    prompt_user "Author name" author_name "$(git config user.name 2>/dev/null || echo 'Your Name')"

    echo ""
    print_info "Step 5: Review"
    echo ""

    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}Agent Configuration:${NC}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "  Name:         agent-${agent_name}.md"
    echo -e "  Title:        ${agent_title}"
    echo -e "  Purpose:      ${agent_purpose}"
    echo -e "  Author:       ${author_name}"
    echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    prompt_user "Create this agent?" confirm "y"

    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        print_warning "Agent creation cancelled"
        exit 0
    fi

    echo ""
    print_info "Generating agent template..."

    generate_agent_template "$agent_name" "$agent_title" "$agent_purpose" "$(echo -e $agent_capabilities)" "$author_name"

    echo ""
    prompt_user "Install to Claude agents directory? (~/.claude/agents/)" install "y"

    if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
        install_agent "$agent_name"
    fi

    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  ✨ Agent Created Successfully!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Edit the agent file to customize the implementation"
    echo "  2. Fill in the examples with realistic scenarios"
    echo "  3. Add specific best practices for your use case"
    echo "  4. Test the agent with different CoT intensity levels"
    echo ""
    echo -e "${BLUE}File Location:${NC}"
    echo "  Local:  $LOCAL_AGENTS_DIR/agent-$agent_name.md"
    if [ "$install" = "y" ] || [ "$install" = "Y" ]; then
        echo "  Global: $AGENTS_DIR/agent-$agent_name.md"
    fi
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo "  cot /use agent-$agent_name \"[your task]\""
    echo "  cot+ /use agent-$agent_name \"[complex task]\""
    echo "  cot++ /use agent-$agent_name \"[critical task]\""
    echo ""
    print_success "Happy agent building! 🚀"
    echo ""
}

# Run wizard
main "$@"
