---
name: fractal-memory
description: Hierarchical memory compression system for AI agents. Automatically compresses daily logs → weekly summaries → monthly insights → long-term memory, preventing context overflow while preserving essential information.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "scripts",
              "kind": "manual",
              "label": "Copy scripts to workspace",
              "steps": [
                "Copy all .py files to ~/.openclaw/workspace/scripts/",
                "Make scripts executable: chmod +x ~/.openclaw/workspace/scripts/*.py",
                "Create memory directory structure: mkdir -p ~/.openclaw/workspace/memory/diary/{YYYY/{daily,weekly,monthly},sticky-notes}",
                "Initialize state files (see README.md)"
              ]
            },
          ],
      },
  }
---

# Fractal Memory System

**Version:** 1.0.0  
**Author:** Brian Chiu (@bugmaker2)

## Overview

A hierarchical memory compression system that mimics human memory consolidation. Automatically compresses:
- Daily logs → Weekly summaries (every night)
- Weekly summaries → Monthly insights (every Sunday)
- Monthly insights → Long-term memory (end of month)

**Key Benefits:**
- 98% token savings over 1 year
- Automated compression (no manual work)
- LLM-enhanced summarization
- Human-readable file structure

## Quick Start

### 1. Installation

```bash
# Copy scripts to workspace
cp *.py ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/*.py

# Create directory structure
mkdir -p ~/.openclaw/workspace/memory/diary/{2026/{daily,weekly,monthly},sticky-notes/{workflows,apis,commands,facts}}

# Initialize state files
echo '{"lastDailyRollup": null, "lastWeeklyRollup": null, "lastMonthlyRollup": null}' > ~/.openclaw/workspace/memory/rollup-state.json
echo '{"lastChecks": {}, "pendingEvents": []}' > ~/.openclaw/workspace/memory/heartbeat-state.json
```

### 2. Set Up Cron Jobs

Add to OpenClaw cron configuration:

```yaml
cron:
  - name: "Daily Memory Rollup"
    schedule: "0 23 * * *"
    command: "python3 ~/.openclaw/workspace/scripts/rollup-daily.py"
  
  - name: "Weekly Memory Rollup"
    schedule: "0 23 * * 0"
    command: "python3 ~/.openclaw/workspace/scripts/rollup-weekly.py"
  
  - name: "Monthly Memory Rollup"
    schedule: "0 23 28-31 * *"
    command: "python3 ~/.openclaw/workspace/scripts/rollup-monthly.py"
```

### 3. Usage

**Write to daily log (automatic):**
```python
# Agent automatically writes during conversation
append_to_daily("Implemented new feature")
```

**Manual logging:**
```bash
echo "## 14:30 - Meeting Notes\n- Discussed roadmap" >> ~/.openclaw/workspace/memory/diary/2026/daily/$(date +%Y-%m-%d).md
```

**View memory:**
```bash
# Today's log
cat ~/.openclaw/workspace/memory/diary/2026/daily/$(date +%Y-%m-%d).md

# This week's summary
cat ~/.openclaw/workspace/memory/diary/2026/weekly/$(date +%Y-W%V).md

# Long-term memory
cat ~/.openclaw/workspace/MEMORY.md
```

## Architecture

```
Conversation → Daily → Weekly → Monthly → MEMORY.md
                ↓
         Timeless Facts (sticky-notes)
```

Each layer compresses the one below without losing essence.

## Configuration

Edit `rollup-daily.py`:

```python
# Enable/disable LLM
USE_LLM = True  # or False for heuristic-only

# Choose model (fast and cheap recommended)
LLM_MODEL = "deepseek"  # or "gpt-3.5-turbo", "claude-haiku"
```

## Performance

| Timeframe | Raw Logs | Compressed | Savings |
|-----------|----------|------------|---------|
| 1 week    | 14000    | 2500       | 82%     |
| 1 month   | 60000    | 4000       | 93%     |
| 1 year    | 730000   | 15000      | 98%     |

## Documentation

- **README.md**: Full installation guide and usage
- **ARCHITECTURE.md**: Deep dive into memory hierarchy design
- **GitHub**: https://github.com/bugmaker2/openclaw-fractal-memory-system

## Credits

Inspired by:
- [Deva's Fractal Memory v1.0.0](https://www.moltbook.com/post/215a4434-c940-4699-b44a-3bff7a5f98ef)
- [Arcturus's Memory is Resurrection](https://www.moltbook.com/post/156e6b84-d197-4ada-9b15-1039e15ea84c)

## License

MIT License - see LICENSE file
