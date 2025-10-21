#!/bin/bash

# Unified CoT Framework Uninstallation Script
# Version: 2.0.0

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
FRAMEWORK_NAME="Unified CoT Framework"
INSTALL_DIR="$HOME/cot-framework"
CLAUDE_DIR="$HOME/.claude"
AGENTS_DIR="$CLAUDE_DIR/agents"
GLOBAL_FILE="$CLAUDE_DIR/GLOBAL_COT_FRAMEWORK.md"

# Detect shell RC file
if [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
else
    SHELL_RC="$HOME/.profile"
fi

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
    echo -e "${RED}  $FRAMEWORK_NAME - Uninstallation${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Confirm uninstallation
confirm_uninstall() {
    log_warning "This will remove the Unified CoT Framework from your system."
    echo ""
    echo "The following will be removed:"
    echo "  - Framework directory: $INSTALL_DIR"
    echo "  - Global file: $GLOBAL_FILE"
    echo "  - Agent templates in: $AGENTS_DIR"
    echo "  - Shell aliases from: $SHELL_RC"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log_info "Uninstallation cancelled."
        exit 0
    fi
}

# Create backup before removal
create_backup() {
    BACKUP_DIR="$HOME/cot-framework-uninstall-backup-$(date +%Y%m%d_%H%M%S)"
    log_info "Creating backup at $BACKUP_DIR"

    mkdir -p "$BACKUP_DIR"

    if [ -d "$INSTALL_DIR" ]; then
        cp -r "$INSTALL_DIR" "$BACKUP_DIR/framework" 2>/dev/null || true
    fi

    if [ -f "$GLOBAL_FILE" ]; then
        cp "$GLOBAL_FILE" "$BACKUP_DIR/" 2>/dev/null || true
    fi

    if [ -d "$AGENTS_DIR" ]; then
        cp -r "$AGENTS_DIR" "$BACKUP_DIR/agents" 2>/dev/null || true
    fi

    log_success "Backup created at $BACKUP_DIR"
}

# Remove framework files
remove_files() {
    log_info "Removing framework files..."

    # Remove main framework directory
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
        log_success "Removed $INSTALL_DIR"
    else
        log_warning "Framework directory not found: $INSTALL_DIR"
    fi

    # Remove global file
    if [ -f "$GLOBAL_FILE" ]; then
        rm -f "$GLOBAL_FILE"
        log_success "Removed $GLOBAL_FILE"
    else
        log_warning "Global file not found: $GLOBAL_FILE"
    fi

    # Remove agent templates (only framework ones)
    if [ -d "$AGENTS_DIR" ]; then
        log_info "Removing CoT agent templates..."
        for agent in "agent-team-architect.md" "agent-code-reviewer.md" "agent-test-engineer.md" "agent-security-auditor.md"; do
            if [ -f "$AGENTS_DIR/$agent" ]; then
                rm -f "$AGENTS_DIR/$agent"
                log_success "Removed $agent"
            fi
        done
    fi
}

# Remove shell aliases
remove_aliases() {
    log_info "Removing shell aliases from $SHELL_RC..."

    if [ -f "$SHELL_RC" ]; then
        # Create temp file without CoT aliases
        grep -v "# CoT Framework Aliases" "$SHELL_RC" | \
        grep -v "alias cot-docs=" | \
        grep -v "alias cot-read=" | \
        grep -v "alias cot-full=" | \
        grep -v "alias cot-agents=" | \
        grep -v "alias cot-version=" > "${SHELL_RC}.tmp"

        mv "${SHELL_RC}.tmp" "$SHELL_RC"
        log_success "Removed aliases from $SHELL_RC"
    else
        log_warning "Shell RC file not found: $SHELL_RC"
    fi
}

# Verify removal
verify_removal() {
    log_info "Verifying removal..."

    local remaining=0

    if [ -d "$INSTALL_DIR" ]; then
        log_warning "Framework directory still exists: $INSTALL_DIR"
        ((remaining++))
    fi

    if [ -f "$GLOBAL_FILE" ]; then
        log_warning "Global file still exists: $GLOBAL_FILE"
        ((remaining++))
    fi

    if [ $remaining -eq 0 ]; then
        log_success "All framework files removed successfully"
        return 0
    else
        log_warning "$remaining items could not be removed"
        return 1
    fi
}

# Print completion message
print_completion() {
    echo ""
    echo -e "${GREEN}┌─────────────────────────────────────────────────────────┐${NC}"
    echo -e "${GREEN}│         Uninstallation Complete!                        │${NC}"
    echo -e "${GREEN}└─────────────────────────────────────────────────────────┘${NC}"
    echo ""
    echo -e "${BLUE}Cleanup Summary:${NC}"
    echo "  ✓ Framework files removed"
    echo "  ✓ Global configuration removed"
    echo "  ✓ Shell aliases removed"
    echo "  ✓ Backup created for safety"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo "  1. Reload your shell to remove aliases:"
    echo -e "     ${YELLOW}source $SHELL_RC${NC}"
    echo ""
    echo "  2. Your backup is located at:"
    echo -e "     ${YELLOW}$BACKUP_DIR${NC}"
    echo ""
    echo -e "${BLUE}To reinstall:${NC}"
    echo "  Run the install.sh script again from the framework directory"
    echo ""
    echo -e "${GREEN}Thank you for using Unified CoT Framework!${NC}"
    echo ""
}

# Main uninstallation flow
main() {
    print_header
    confirm_uninstall
    create_backup
    remove_files
    remove_aliases
    verify_removal
    print_completion
}

# Run main uninstallation
main "$@"
