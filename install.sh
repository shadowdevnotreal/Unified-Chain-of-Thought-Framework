#!/bin/bash

# Unified CoT Framework Installation Script
# Version: 2.0.0
# Enhanced with better error handling, validation, and cross-platform support

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRAMEWORK_NAME="Unified CoT Framework"
VERSION="2.0.0"
INSTALL_DIR="$HOME/cot-framework"
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$CLAUDE_DIR/agents"
GLOBAL_FILE="$CLAUDE_DIR/GLOBAL_COT_FRAMEWORK.md"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}  $FRAMEWORK_NAME - Installation${NC}"
    echo -e "${BLUE}  Version: $VERSION${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

print_footer() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}  Installation Complete!${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if running in supported shell
    if [ -z "$SHELL" ]; then
        log_error "Unable to detect shell. Please set SHELL environment variable."
        exit 1
    fi

    # Detect shell type
    case "$SHELL" in
        */bash)
            SHELL_TYPE="bash"
            SHELL_RC="$HOME/.bashrc"
            ;;
        */zsh)
            SHELL_TYPE="zsh"
            SHELL_RC="$HOME/.zshrc"
            ;;
        */fish)
            SHELL_TYPE="fish"
            SHELL_RC="$HOME/.config/fish/config.fish"
            log_warning "Fish shell detected. Aliases will need manual configuration."
            ;;
        *)
            SHELL_TYPE="unknown"
            SHELL_RC="$HOME/.profile"
            log_warning "Unknown shell: $SHELL. Defaulting to .profile"
            ;;
    esac

    log_success "Shell detected: $SHELL_TYPE"

    # Check for required commands
    for cmd in cp mkdir chmod; do
        if ! command -v $cmd &> /dev/null; then
            log_error "Required command '$cmd' not found"
            exit 1
        fi
    done

    log_success "Prerequisites satisfied"
}

# Detect OS
detect_os() {
    log_info "Detecting operating system..."

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
        if grep -qi microsoft /proc/version 2>/dev/null; then
            OS="WSL"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        OS="Windows"
    else
        OS="Unknown"
        log_warning "Unknown OS: $OSTYPE"
    fi

    log_success "Operating System: $OS"
}

# Backup existing installation
backup_existing() {
    if [ -d "$INSTALL_DIR" ]; then
        BACKUP_DIR="${INSTALL_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
        log_warning "Existing installation found at $INSTALL_DIR"
        log_info "Creating backup at $BACKUP_DIR"

        cp -r "$INSTALL_DIR" "$BACKUP_DIR" || {
            log_error "Failed to create backup"
            exit 1
        }

        log_success "Backup created successfully"
    fi

    if [ -d "$AGENTS_DIR" ]; then
        AGENTS_BACKUP="${AGENTS_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
        log_info "Backing up existing agents to $AGENTS_BACKUP"
        cp -r "$AGENTS_DIR" "$AGENTS_BACKUP" || {
            log_error "Failed to backup agents"
            exit 1
        }
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."

    mkdir -p "$INSTALL_DIR" || {
        log_error "Failed to create $INSTALL_DIR"
        exit 1
    }

    mkdir -p "$CLAUDE_DIR" || {
        log_error "Failed to create $CLAUDE_DIR"
        exit 1
    }

    mkdir -p "$AGENTS_DIR" || {
        log_error "Failed to create $AGENTS_DIR"
        exit 1
    }

    log_success "Directories created successfully"
}

# Copy framework files
copy_files() {
    log_info "Copying framework files..."

    # Copy documentation
    if [ -d "$SCRIPT_DIR/docs" ]; then
        cp -r "$SCRIPT_DIR/docs" "$INSTALL_DIR/" || {
            log_error "Failed to copy docs"
            exit 1
        }
        log_success "Documentation copied"
    else
        log_warning "docs directory not found, skipping..."
    fi

    # Copy examples
    if [ -d "$SCRIPT_DIR/examples" ]; then
        cp -r "$SCRIPT_DIR/examples" "$INSTALL_DIR/" || {
            log_error "Failed to copy examples"
            exit 1
        }
        log_success "Examples copied"
    else
        log_warning "examples directory not found, skipping..."
    fi

    # Copy agents
    if [ -d "$SCRIPT_DIR/agents" ]; then
        cp "$SCRIPT_DIR/agents/"*.md "$AGENTS_DIR/" 2>/dev/null || {
            log_warning "No agent files found to copy"
        }
        log_success "Agent templates copied"
    else
        log_warning "agents directory not found, skipping..."
    fi

    # Copy root files
    for file in README.md LICENSE CONTRIBUTING.md; do
        if [ -f "$SCRIPT_DIR/$file" ]; then
            cp "$SCRIPT_DIR/$file" "$INSTALL_DIR/" || {
                log_warning "Failed to copy $file"
            }
        fi
    done

    log_success "Files copied successfully"
}

# Generate global framework file
generate_global_framework() {
    log_info "Generating global framework file..."

    cat > "$GLOBAL_FILE" << 'EOFGLOBAL'
# Unified CoT Framework - Global Access

This file enables the Chain of Thought framework globally in all Claude Code sessions.

## Quick Reference

### Intensity Levels
- `cot` - Standard thinking (4,000 tokens, 5-15s)
- `cot+` - Enhanced thinking (10,000 tokens, 20-45s)
- `cot++` - Maximum thinking (31,999 tokens, 45-180s)

### Universal Framework (4 Steps)
1. **LISTEN** - Actively gather and comprehend information
2. **THINK** - Apply Chain of Thought systematic breakdown
3. **REASON** - Validate with Chain of Reasoning
4. **RESPOND** - Synthesize and deliver clearly

### Coding Framework (5 Steps)
1. **ANALYZE** - Requirements and context understanding
2. **PLAN** - Technical design and approach
3. **VALIDATE** - Pre-implementation logic verification
4. **IMPLEMENT** - Code execution with verification
5. **CONFIRM** - Quality assurance and completion

## Usage Examples

### Basic Usage
```
cot <your task>
```

### Enhanced Thinking
```
cot+ Analyze this complex algorithm and suggest optimizations
```

### Maximum Reasoning
```
cot++ Design a microservices architecture for enterprise-scale application
```

## Available Agents

### Team Architect
Design and orchestrate multi-agent systems for complex projects.

### Code Reviewer
Comprehensive code review with quality, security, and performance analysis.

### Test Engineer
Generate test cases, implement test suites, and analyze coverage.

### Security Auditor
Security vulnerability assessment and OWASP compliance checking.

## Documentation Location
Full documentation: ~/cot-framework/

## Quick Commands
- `cot-docs` - View quick reference
- `cot-read` - Read this global file
- `cot-full` - Navigate to framework directory

---
Unified CoT Framework v2.0.0
EOFGLOBAL

    if [ $? -eq 0 ]; then
        log_success "Global framework file created at $GLOBAL_FILE"
    else
        log_error "Failed to create global framework file"
        exit 1
    fi
}

# Setup shell aliases
setup_aliases() {
    log_info "Setting up shell aliases..."

    # Check if shell RC file exists
    if [ ! -f "$SHELL_RC" ]; then
        log_warning "Shell RC file not found: $SHELL_RC"
        log_info "Creating new RC file..."
        touch "$SHELL_RC"
    fi

    # Remove old aliases if they exist
    if grep -q "# CoT Framework Aliases" "$SHELL_RC" 2>/dev/null; then
        log_info "Removing old aliases..."
        # Create temp file without old aliases
        grep -v "# CoT Framework Aliases" "$SHELL_RC" | \
        grep -v "alias cot-docs=" | \
        grep -v "alias cot-read=" | \
        grep -v "alias cot-full=" > "${SHELL_RC}.tmp"
        mv "${SHELL_RC}.tmp" "$SHELL_RC"
    fi

    # Add new aliases
    cat >> "$SHELL_RC" << EOF

# CoT Framework Aliases (Added by Unified CoT Framework installer)
alias cot-docs='cat ~/cot-framework/docs/cot-quick-reference.md 2>/dev/null || echo "Quick reference not found"'
alias cot-read='cat ~/.claude/GLOBAL_COT_FRAMEWORK.md 2>/dev/null || echo "Global framework file not found"'
alias cot-full='cd ~/cot-framework && ls -lah'
alias cot-agents='ls -lah ~/.claude/agents/'
alias cot-version='echo "Unified CoT Framework v2.0.0"'
EOF

    log_success "Shell aliases added to $SHELL_RC"
    log_info "Run 'source $SHELL_RC' to activate aliases in current session"
}

# Verify installation
verify_installation() {
    log_info "Verifying installation..."

    local errors=0

    # Check directories
    for dir in "$INSTALL_DIR" "$CLAUDE_DIR" "$AGENTS_DIR"; do
        if [ ! -d "$dir" ]; then
            log_error "Directory not found: $dir"
            ((errors++))
        fi
    done

    # Check global file
    if [ ! -f "$GLOBAL_FILE" ]; then
        log_error "Global framework file not found: $GLOBAL_FILE"
        ((errors++))
    fi

    # Check for at least some documentation
    if [ ! -d "$INSTALL_DIR/docs" ] && [ ! -f "$INSTALL_DIR/README.md" ]; then
        log_error "No documentation found in $INSTALL_DIR"
        ((errors++))
    fi

    # Check for agents
    agent_count=$(find "$AGENTS_DIR" -name "*.md" 2>/dev/null | wc -l)
    if [ "$agent_count" -eq 0 ]; then
        log_warning "No agent files found in $AGENTS_DIR"
    else
        log_success "Found $agent_count agent templates"
    fi

    if [ $errors -eq 0 ]; then
        log_success "Installation verified successfully"
        return 0
    else
        log_error "Installation verification failed with $errors errors"
        return 1
    fi
}

# Print post-installation instructions
print_instructions() {
    echo ""
    echo -e "${GREEN}┌─────────────────────────────────────────────────────────┐${NC}"
    echo -e "${GREEN}│         Installation Successful!                        │${NC}"
    echo -e "${GREEN}└─────────────────────────────────────────────────────────┘${NC}"
    echo ""
    echo -e "${BLUE}Installation Details:${NC}"
    echo "  Framework Location: $INSTALL_DIR"
    echo "  Claude Directory:   $CLAUDE_DIR"
    echo "  Agents Directory:   $AGENTS_DIR"
    echo "  Global File:        $GLOBAL_FILE"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Reload your shell configuration:"
    echo -e "     ${YELLOW}source $SHELL_RC${NC}"
    echo ""
    echo "  2. Try the quick reference:"
    echo -e "     ${YELLOW}cot-docs${NC}"
    echo ""
    echo "  3. View available agents:"
    echo -e "     ${YELLOW}cot-agents${NC}"
    echo ""
    echo "  4. Start using CoT in Claude Code:"
    echo -e "     ${YELLOW}cot <your task>${NC}"
    echo -e "     ${YELLOW}cot+ <complex task>${NC}"
    echo -e "     ${YELLOW}cot++ <very complex task>${NC}"
    echo ""
    echo -e "${BLUE}Available Agents:${NC}"
    echo "  - agent-team-architect.md     (Multi-agent orchestration)"
    echo "  - agent-code-reviewer.md      (Code quality & security)"
    echo "  - agent-test-engineer.md      (Testing & coverage)"
    echo "  - agent-security-auditor.md   (Security auditing)"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  - Full docs: $INSTALL_DIR/docs/"
    echo "  - Examples:  $INSTALL_DIR/examples/"
    echo "  - README:    $INSTALL_DIR/README.md"
    echo ""
    echo -e "${GREEN}Happy coding with enhanced reasoning! 🚀${NC}"
    echo ""
}

# Uninstall function (for reference)
show_uninstall_info() {
    log_info "To uninstall, run: $SCRIPT_DIR/uninstall.sh"
}

# Main installation flow
main() {
    print_header

    # Run installation steps
    check_prerequisites
    detect_os
    backup_existing
    create_directories
    copy_files
    generate_global_framework
    setup_aliases

    # Verify and complete
    if verify_installation; then
        print_footer
        print_instructions
        show_uninstall_info
        exit 0
    else
        log_error "Installation completed with errors. Please review the output above."
        exit 1
    fi
}

# Run main installation
main "$@"
