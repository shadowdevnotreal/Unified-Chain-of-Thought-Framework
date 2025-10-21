#!/bin/bash

# Unified CoT Framework Installation Verification Script
# Version: 2.0.0

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="$HOME/cot-framework"
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$CLAUDE_DIR/agents"
GLOBAL_FILE="$CLAUDE_DIR/GLOBAL_COT_FRAMEWORK.md"

# Counters
PASSED=0
FAILED=0
WARNINGS=0

# Logging functions
log_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

log_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

log_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}  Unified CoT Framework - Installation Verification${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Check directory structure
check_directories() {
    echo -e "${BLUE}[1/6] Checking Directory Structure${NC}"
    echo ""

    if [ -d "$INSTALL_DIR" ]; then
        log_pass "Framework directory exists: $INSTALL_DIR"
    else
        log_fail "Framework directory missing: $INSTALL_DIR"
    fi

    if [ -d "$CLAUDE_DIR" ]; then
        log_pass "Claude directory exists: $CLAUDE_DIR"
    else
        log_fail "Claude directory missing: $CLAUDE_DIR"
    fi

    if [ -d "$AGENTS_DIR" ]; then
        log_pass "Agents directory exists: $AGENTS_DIR"
    else
        log_fail "Agents directory missing: $AGENTS_DIR"
    fi

    if [ -d "$INSTALL_DIR/docs" ]; then
        log_pass "Docs directory exists"
    else
        log_warn "Docs directory missing (optional)"
    fi

    if [ -d "$INSTALL_DIR/examples" ]; then
        log_pass "Examples directory exists"
    else
        log_warn "Examples directory missing (optional)"
    fi

    echo ""
}

# Check core files
check_core_files() {
    echo -e "${BLUE}[2/6] Checking Core Files${NC}"
    echo ""

    if [ -f "$GLOBAL_FILE" ]; then
        log_pass "Global framework file exists"

        # Check file size
        size=$(stat -f%z "$GLOBAL_FILE" 2>/dev/null || stat -c%s "$GLOBAL_FILE" 2>/dev/null)
        if [ "$size" -gt 100 ]; then
            log_pass "Global file has content (${size} bytes)"
        else
            log_fail "Global file is too small (${size} bytes)"
        fi
    else
        log_fail "Global framework file missing: $GLOBAL_FILE"
    fi

    if [ -f "$INSTALL_DIR/README.md" ]; then
        log_pass "README.md exists"
    else
        log_warn "README.md missing"
    fi

    if [ -f "$INSTALL_DIR/LICENSE" ]; then
        log_pass "LICENSE file exists"
    else
        log_warn "LICENSE file missing (optional)"
    fi

    echo ""
}

# Check documentation
check_documentation() {
    echo -e "${BLUE}[3/6] Checking Documentation${NC}"
    echo ""

    local doc_count=0
    for doc in "cot.md" "cot-expanded.md" "cot-quick-reference.md" "unified-cot-system.md"; do
        if [ -f "$INSTALL_DIR/docs/$doc" ]; then
            log_pass "Found: docs/$doc"
            ((doc_count++))
        else
            log_warn "Missing: docs/$doc"
        fi
    done

    if [ $doc_count -ge 2 ]; then
        log_pass "Sufficient documentation found ($doc_count files)"
    else
        log_fail "Insufficient documentation ($doc_count files)"
    fi

    echo ""
}

# Check agents
check_agents() {
    echo -e "${BLUE}[4/6] Checking Agent Templates${NC}"
    echo ""

    local agent_count=0
    local expected_agents=(
        "agent-team-architect.md"
        "agent-code-reviewer.md"
        "agent-test-engineer.md"
        "agent-security-auditor.md"
    )

    for agent in "${expected_agents[@]}"; do
        if [ -f "$AGENTS_DIR/$agent" ]; then
            log_pass "Found: $agent"
            ((agent_count++))
        else
            log_warn "Missing: $agent"
        fi
    done

    log_info "Total agents found: $agent_count/${#expected_agents[@]}"

    if [ $agent_count -ge 1 ]; then
        log_pass "At least one agent template available"
    else
        log_fail "No agent templates found"
    fi

    echo ""
}

# Check shell aliases
check_aliases() {
    echo -e "${BLUE}[5/6] Checking Shell Aliases${NC}"
    echo ""

    # Detect shell RC file
    if [ -n "$BASH_VERSION" ]; then
        SHELL_RC="$HOME/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.profile"
    fi

    if [ ! -f "$SHELL_RC" ]; then
        log_fail "Shell RC file not found: $SHELL_RC"
        echo ""
        return
    fi

    log_info "Checking: $SHELL_RC"
    echo ""

    local aliases=("cot-docs" "cot-read" "cot-full" "cot-agents" "cot-version")
    local alias_count=0

    for alias_name in "${aliases[@]}"; do
        if grep -q "alias $alias_name=" "$SHELL_RC" 2>/dev/null; then
            log_pass "Alias configured: $alias_name"
            ((alias_count++))
        else
            log_warn "Alias missing: $alias_name"
        fi
    done

    if [ $alias_count -ge 3 ]; then
        log_pass "Most aliases configured ($alias_count/5)"
    else
        log_warn "Some aliases missing ($alias_count/5)"
    fi

    echo ""
}

# Test alias functionality
test_aliases() {
    echo -e "${BLUE}[6/6] Testing Alias Functionality${NC}"
    echo ""

    # Source the RC file to load aliases
    if [ -n "$BASH_VERSION" ]; then
        source "$HOME/.bashrc" 2>/dev/null || true
    elif [ -n "$ZSH_VERSION" ]; then
        source "$HOME/.zshrc" 2>/dev/null || true
    fi

    # Test cot-version
    if command -v cot-version &> /dev/null; then
        version_output=$(cot-version 2>/dev/null)
        if [[ "$version_output" == *"2.0.0"* ]]; then
            log_pass "cot-version command works (v2.0.0)"
        else
            log_warn "cot-version output unexpected: $version_output"
        fi
    else
        log_warn "cot-version alias not loaded (restart shell or run 'source $SHELL_RC')"
    fi

    # Test cot-docs
    if command -v cot-docs &> /dev/null; then
        log_pass "cot-docs command available"
    else
        log_warn "cot-docs alias not loaded"
    fi

    # Test cot-agents
    if command -v cot-agents &> /dev/null; then
        log_pass "cot-agents command available"
    else
        log_warn "cot-agents alias not loaded"
    fi

    echo ""
}

# Print summary
print_summary() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${BLUE}  Verification Summary${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${GREEN}Passed:${NC}   $PASSED"
    echo -e "${RED}Failed:${NC}   $FAILED"
    echo -e "${YELLOW}Warnings:${NC} $WARNINGS"
    echo ""

    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ Installation verification PASSED!${NC}"
        echo ""
        echo "Your Unified CoT Framework installation is working correctly."
        echo ""
        echo "Next steps:"
        echo "  1. Restart your terminal or run: source $SHELL_RC"
        echo "  2. Try: cot-version"
        echo "  3. Try: cot-docs"
        echo "  4. Start using: cot <your task>"
        echo ""
        return 0
    elif [ $FAILED -le 2 ] && [ $PASSED -ge 10 ]; then
        echo -e "${YELLOW}⚠ Installation verification PASSED with warnings${NC}"
        echo ""
        echo "Installation mostly complete but some issues detected."
        echo "Review the failed checks above and consider reinstalling."
        echo ""
        return 0
    else
        echo -e "${RED}✗ Installation verification FAILED${NC}"
        echo ""
        echo "Installation has critical issues. Please:"
        echo "  1. Review the errors above"
        echo "  2. Try reinstalling: ./install.sh"
        echo "  3. Check permissions and file paths"
        echo ""
        return 1
    fi
}

# Main verification flow
main() {
    print_header
    check_directories
    check_core_files
    check_documentation
    check_agents
    check_aliases
    test_aliases
    print_summary
}

# Run main verification
main "$@"
