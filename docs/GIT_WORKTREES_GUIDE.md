# Git Worktrees with Claude Code

Quick reference guide for using git worktrees to run multiple Claude Code sessions in parallel.

## Quick Start

```bash
# Create a new worktree
git worktree add ../project-name -b branch-name

# Enter the worktree
cd ../project-name

# Set up environment (IMPORTANT!)
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run Claude Code
claude
```

## Key Rules

### ✅ What Worktrees Are Great For
- **Parallel Claude sessions** on different branches simultaneously
- **Complete isolation** - changes in one worktree don't affect others
- **Shared Git history** - all worktrees use the same repository
- Working on different features/bugfixes at the same time

### ⚠️ Critical Rules
1. **Different agents = Different files** - Each Claude session should modify separate files or you'll have conflicts
2. **Initialize every worktree** - Run `npm install`, `pip install`, setup config files in EACH worktree (they don't inherit node_modules/venv)
3. **No built-in agent communication** - Multiple agents can't directly talk to each other (use shared `.claude/shared-context.md` file as workaround)

### 💰 Cost Awareness
Multiple concurrent Claude sessions burn tokens fast. 3-5 agents running in parallel can exceed monthly limits quickly.

## For This Project

Parallelize work on the three agents:

```bash
# Main directory
cd ~/EEA_Industrial_Emissions_Data

# Create separate worktrees for each agent
git worktree add ../eea-lead-gen -b feature/enhanced-lead-gen
git worktree add ../eea-evaluation -b feature/enhanced-eval
git worktree add ../eea-proposals -b feature/enhanced-proposals

# Each Claude session works in isolation, then merge back to main
```

## Common Commands

```bash
git worktree list              # See all active worktrees
git worktree remove ../path    # Delete a worktree
git worktree prune             # Clean up stale worktrees
```

## Environment Setup Template

For each new worktree:

```bash
cd ../new-worktree

# Python setup
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy any local config files if needed
cp ../.claude/settings.local.json .claude/settings.local.json
cp ../.env .env                  # If using environment variables

# Start Claude Code
claude
```

## Best Practices

1. **Use descriptive names**: `../eea-dioxin-scoring` instead of `../wt2`
2. **Isolate tasks**: Each worktree focuses on one specific feature/fix
3. **Separate files**: Agent A modifies `lead_generation_agent.py`, Agent B modifies `proposal_generation_agent.py`
4. **Document context**: Use `.claude/CLAUDE.md` to explain what each worktree should do
5. **Regular cleanup**: Remove finished worktrees to avoid clutter

```bash
# Example of good isolation:
# Worktree 1: Refactors lead_generation_agent.py only
# Worktree 2: Adds new tools to lead_evaluation_agent.py only
# Worktree 3: Updates proposal_generation_agent.py only
```

## Cleanup When Done

```bash
# List what you have
git worktree list

# Remove finished worktrees
git worktree remove ../eea-lead-gen
git worktree remove ../eea-evaluation
git worktree remove ../eea-proposals

# Prune stale references
git worktree prune

# Back to main
cd ~/EEA_Industrial_Emissions_Data
```

## Summary

Worktrees enable true parallel development with Claude Code, but require:
- ✅ Different agents work on different files
- ✅ Full environment setup in each worktree
- ✅ Awareness of token costs with multiple sessions
- ✅ Clear file isolation to avoid conflicts

Perfect for your multi-agent architecture where lead generation, evaluation, and proposal agents can be enhanced independently!
