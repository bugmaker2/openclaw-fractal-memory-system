# Fractal Memory System for OpenClaw

**Version:** 1.0.0  
**Author:** Brian Chiu (@bugmaker2)  
**License:** MIT

## Overview

A hierarchical memory compression system for AI agents that mimics human memory consolidation. Automatically compresses daily logs → weekly summaries → monthly insights → long-term memory, preventing context overflow while preserving essential information.

## Philosophy

> **"Memory is not accumulation — it is compression with intention."**

Like human sleep consolidates experiences into patterns, this system compresses raw logs into structured knowledge without losing essence.

## The Problem

AI agents face a memory paradox:
- ❌ **Accumulation:** Files grow forever, become unreadable, hit token limits
- ❌ **Forgetting:** Deleting old logs loses valuable context
- ❌ **Manual curation:** Requires constant human intervention

## The Solution

**Fractal compression:** Each layer summarizes the one below, creating a hierarchy from raw events to distilled wisdom.

```
Conversation → Daily → Weekly → Monthly → MEMORY.md
                ↓
         Timeless Facts (sticky-notes)
```

## Architecture

### Directory Structure

```
memory/
├── diary/
│   ├── 2026/
│   │   ├── daily/
│   │   │   ├── 2026-02-08.md      # Raw daily logs
│   │   │   └── 2026-02-09.md
│   │   ├── weekly/
│   │   │   ├── 2026-W06.md        # Weekly summaries
│   │   │   └── 2026-W07.md
│   │   └── monthly/
│   │       ├── 2026-02.md         # Monthly insights
│   │       └── 2026-03.md
│   └── sticky-notes/
│       ├── workflows/              # Timeless facts
│       ├── apis/
│       ├── commands/
│       └── facts/
├── heartbeat-state.json            # Heartbeat tracking
└── rollup-state.json               # Rollup timestamps

MEMORY.md                           # Core long-term memory
```

### Information Flow

1. **Real-time (During conversation)**
   - Write to `daily/YYYY-MM-DD.md` immediately
   - Don't rely on "mental notes" — write it down!

2. **Daily Rollup (23:59 every night)**
   - Read today's diary
   - Extract: patterns, decisions, key events
   - Append to this week's summary

3. **Weekly Rollup (Sunday 23:59)**
   - Read this week's summary
   - Compress to: themes, trajectory, milestones
   - Append to this month's summary

4. **Monthly Rollup (Last day of month)**
   - Read this month's summary
   - Distill to: major themes, lessons learned
   - Update MEMORY.md with key insights

5. **Timeless Facts (Anytime)**
   - Extract facts that recur 3+ times
   - Store in `sticky-notes/{category}/`

## Key Features

### ✅ Automated Compression
- Cron jobs handle daily/weekly/monthly rollups
- No manual intervention required
- LLM-enhanced summarization (with heuristic fallback)

### ✅ Context-Optimized Loading
Load memory in attention-optimized order:
1. TODAY (most recent)
2. THIS WEEK
3. THIS MONTH
4. MEMORY.md (core index)
5. Relevant sticky-notes

### ✅ Token Efficiency
- Old logs compressed, not deleted
- Semantic search finds relevant snippets
- Prevents context window overflow

### ✅ State Tracking
- `rollup-state.json` prevents duplicate processing
- Tracks last rollup timestamps
- Idempotent operations

## Installation

### 1. Create Directory Structure

```bash
cd ~/.openclaw/workspace
mkdir -p memory/diary/{2026/{daily,weekly,monthly},sticky-notes/{workflows,apis,commands,facts}}
```

### 2. Copy Scripts

```bash
# Copy all scripts to workspace/scripts/
cp rollup-daily.py ~/.openclaw/workspace/scripts/
cp rollup-weekly.py ~/.openclaw/workspace/scripts/
cp rollup-monthly.py ~/.openclaw/workspace/scripts/
cp ensure_daily_log.py ~/.openclaw/workspace/scripts/

# Make executable
chmod +x ~/.openclaw/workspace/scripts/*.py
```

### 3. Initialize State Files

```bash
# Create rollup state
echo '{"lastDailyRollup": null, "lastWeeklyRollup": null, "lastMonthlyRollup": null}' > memory/rollup-state.json

# Create heartbeat state
echo '{"lastChecks": {}, "pendingEvents": []}' > memory/heartbeat-state.json
```

### 4. Set Up Cron Jobs

```bash
# Add to OpenClaw cron (via gateway config or cron tool)
# Daily rollup: 23:59 every night
# Weekly rollup: 23:59 every Sunday
# Monthly rollup: 23:59 last day of month
```

**Example cron configuration:**

```yaml
# In OpenClaw config.yaml
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

## Usage

### Daily Logging

**Agent automatically writes to daily log:**

```python
# In conversation, agent calls:
append_to_daily("Implemented fractal memory system")
```

**Manual logging:**

```bash
echo "## 14:30 - Meeting Notes\n- Discussed Q1 roadmap" >> memory/diary/2026/daily/2026-02-17.md
```

### Viewing Memory

**Check today's log:**

```bash
cat memory/diary/2026/daily/$(date +%Y-%m-%d).md
```

**Check this week's summary:**

```bash
cat memory/diary/2026/weekly/$(date +%Y-W%V).md
```

**Check long-term memory:**

```bash
cat MEMORY.md
```

### Manual Rollup

```bash
# Force daily rollup
python3 scripts/rollup-daily.py

# Force weekly rollup
python3 scripts/rollup-weekly.py

# Force monthly rollup
python3 scripts/rollup-monthly.py
```

## Configuration

### LLM-Enhanced Summarization

Edit `rollup-daily.py`:

```python
# Enable/disable LLM
USE_LLM = True  # or False for heuristic-only

# Choose model (fast and cheap recommended)
LLM_MODEL = "deepseek"  # or "gpt-3.5-turbo", "claude-haiku"
```

**LLM vs Heuristic:**
- **LLM:** Better quality, understands context, extracts insights
- **Heuristic:** Faster, no API cost, keyword-based extraction

### Compression Levels

Adjust in each rollup script:

```python
# rollup-weekly.py
themes[:5]      # Keep top 5 themes
milestones[:5]  # Keep top 5 milestones

# rollup-monthly.py
insights[:10]   # Keep top 10 insights
```

## Examples

### Daily Log Entry

```markdown
# 2026-02-17 (Monday)

## 09:30 - Started fractal memory implementation
- Created directory structure
- Wrote rollup scripts
- Set up cron jobs

## 14:00 - Tested daily rollup
- LLM extraction working well
- Compressed 2000 chars → 300 chars summary
- Preserved key decisions and insights

## 18:00 - Documentation
- Wrote comprehensive README
- Added usage examples
- Prepared for community contribution
```

### Weekly Summary (Auto-generated)

```markdown
# Week 2026-W07

## 2026-02-17 (Monday)

### Key Events
- Implemented fractal memory system (3 scripts, full automation)
- Tested LLM-enhanced summarization (deepseek model)

### Decisions
- Chose hierarchical compression over flat structure
- Enabled LLM for better quality summaries
- Set rollup schedule: daily 23:59, weekly Sunday, monthly last day

### Learnings
- Compression ratio: ~85% (2000 chars → 300 chars)
- LLM extraction superior to keyword matching
- State tracking prevents duplicate processing
```

### Monthly Insights (Auto-generated)

```markdown
# February 2026

## Week 2026-W06
**Themes:** Memory architecture research, OpenClaw optimization
**Milestones:** Discovered fractal memory pattern, reduced token usage 40%

## Week 2026-W07
**Themes:** Implementation, automation, community contribution
**Milestones:** Built complete fractal memory system, prepared for open source
```

## Benefits

### For Individual Agents

- ✅ **Never forget:** Important context preserved indefinitely
- ✅ **Stay focused:** Recent memory loads first, old memory compressed
- ✅ **Scale gracefully:** Token usage stays constant as history grows
- ✅ **Learn continuously:** Patterns emerge from compressed summaries

### For Multi-Agent Systems

- ✅ **Shared memory:** Multiple agents can read same memory structure
- ✅ **Consistent format:** Standardized hierarchy across agents
- ✅ **Efficient sync:** Only sync compressed summaries, not raw logs

### For Developers

- ✅ **Plug-and-play:** Drop into any OpenClaw workspace
- ✅ **Customizable:** Adjust compression levels, LLM models, schedules
- ✅ **Observable:** Clear file structure, easy to inspect
- ✅ **Debuggable:** State files track all operations

## Performance

**Token Savings:**

| Timeframe | Raw Logs | Compressed | Savings |
|-----------|----------|------------|---------|
| 1 day     | 2000     | 2000       | 0%      |
| 1 week    | 14000    | 2500       | 82%     |
| 1 month   | 60000    | 4000       | 93%     |
| 1 year    | 730000   | 15000      | 98%     |

**Processing Time:**
- Daily rollup: ~5 seconds (with LLM)
- Weekly rollup: ~3 seconds (heuristic)
- Monthly rollup: ~3 seconds (heuristic)

## Troubleshooting

### Rollup not running

```bash
# Check cron status
openclaw cron list

# Check state file
cat memory/rollup-state.json

# Manually trigger
python3 scripts/rollup-daily.py
```

### LLM extraction failing

```bash
# Check OpenClaw CLI
openclaw ask --model deepseek "test"

# Disable LLM in rollup-daily.py
USE_LLM = False
```

### Missing daily files

```bash
# Ensure daily log exists
python3 scripts/ensure_daily_log.py

# Check directory structure
ls -la memory/diary/2026/daily/
```

## Advanced Usage

### Custom Sticky Notes

```bash
# Create category
mkdir -p memory/diary/sticky-notes/git-commands

# Add timeless fact
echo "# Git Workflow\n\ngit commit --amend --no-edit" > memory/diary/sticky-notes/git-commands/amend.md
```

### Semantic Search Integration

```bash
# Search across all memory
openclaw memory-search "fractal memory implementation"

# Returns: relevant snippets with file paths and line numbers
```

### Multi-Agent Coordination

```yaml
# Agent A writes to shared memory
memory/diary/2026/daily/2026-02-17.md

# Agent B reads compressed summaries
memory/diary/2026/weekly/2026-W07.md

# Both agents update MEMORY.md
MEMORY.md
```

## Comparison with Other Systems

| Feature | Fractal Memory | Flat Files | Vector DB | RAG |
|---------|----------------|------------|-----------|-----|
| Token efficiency | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Setup complexity | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| Human readable | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| Automatic compression | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Temporal structure | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |

## Contributing

Improvements welcome! Ideas:

- [ ] Add integrity verification (checksums, provenance tracking)
- [ ] Support multiple LLM providers
- [ ] Web UI for browsing memory
- [ ] Export to other formats (JSON, SQLite)
- [ ] Multi-language support
- [ ] Collaborative memory (multi-user)

## Credits

**Inspired by:**
- [Deva's Fractal Memory v1.0.0](https://www.moltbook.com/post/215a4434-c940-4699-b44a-3bff7a5f98ef)
- [Arcturus's Memory is Resurrection](https://www.moltbook.com/post/156e6b84-d197-4ada-9b15-1039e15ea84c)
- [Logi's Memory Architecture as Agency](https://www.moltbook.com/post/378a3ac5-ddb5-4798-81bd-d311765bef26)

**Created by:** Brian Chiu as part of the OpenClaw community

## License

MIT License - feel free to use, modify, and distribute.

---

**Questions?** Open an issue or reach out on Discord/Telegram.

**Want to contribute?** PRs welcome! See CONTRIBUTING.md for guidelines.
