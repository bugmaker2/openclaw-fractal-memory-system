# [Community Contribution] Fractal Memory System - Hierarchical Memory Compression for AI Agents

## 🎯 Problem Statement

AI agents face a critical challenge: **context window limitations**. As conversations grow, agents either:
- Lose important historical context (forgetting past decisions)
- Hit token limits and crash with API errors
- Waste tokens loading irrelevant old messages

This is especially painful for long-running agents that need to maintain continuity across days, weeks, or months.

## 💡 Solution: Fractal Memory Architecture

I've built a **hierarchical memory compression system** that mimics how humans remember things:

```
Daily Logs (raw details)
    ↓ compress
Weekly Summaries (patterns & decisions)
    ↓ compress
Monthly Summaries (themes & trajectory)
    ↓ distill
Core Memory (timeless knowledge)
```

Each layer compresses the one below **without losing essence**. The agent loads only what's relevant for the current context.

## ✨ Key Features

### 1. **Automated Rollups**
- **Daily → Weekly**: Every Sunday at 23:59, compress the week's logs
- **Weekly → Monthly**: Last day of month, compress all weekly summaries
- **Cron-integrated**: Set it and forget it

### 2. **Token-Efficient Context Loading**
- Load TODAY + YESTERDAY for immediate context (~2-5k tokens)
- Load THIS WEEK for recent patterns (~3-8k tokens)
- Load THIS MONTH for broader trajectory (~5-15k tokens)
- Load CORE MEMORY for timeless facts (~10-30k tokens)
- **Total: ~20-60k tokens vs 100k+ for full history**

### 3. **Smart Compression**
The rollup scripts use Claude to:
- Identify patterns and recurring themes
- Extract key decisions and their rationale
- Preserve important context while removing noise
- Maintain narrative continuity

### 4. **Sticky Notes System**
Timeless facts (API keys, workflows, commands) go into categorized sticky notes:
```
memory/diary/sticky-notes/
├── workflows/
├── apis/
├── commands/
└── preferences/
```

## 📊 Performance Data

**Before Fractal Memory:**
- Main session context: 150k+ tokens after 2 weeks
- Frequent "Unexpected event order" API errors
- Agent forgets decisions from >3 days ago

**After Fractal Memory:**
- Main session context: 40-60k tokens (stable)
- Zero context-related API errors
- Agent maintains continuity across months
- **70% reduction in context token usage**

## 🚀 Installation

### Quick Start
```bash
# Clone the repository
git clone https://github.com/bugmaker2/openclaw-fractal-memory.git
cd openclaw-fractal-memory

# Copy scripts to your OpenClaw workspace
cp *.py ~/.openclaw/workspace/scripts/

# Make scripts executable
chmod +x ~/.openclaw/workspace/scripts/rollup-*.py
chmod +x ~/.openclaw/workspace/scripts/ensure_daily_log.py

# Set up cron jobs (see README for details)
crontab -e
```

### Cron Configuration
```cron
# Daily log creation (every morning)
0 9 * * * cd ~/.openclaw/workspace && python3 scripts/ensure_daily_log.py

# Weekly rollup (Sunday 23:59)
59 23 * * 0 cd ~/.openclaw/workspace && python3 scripts/rollup-weekly.py

# Monthly rollup (last day of month, 23:59)
59 23 28-31 * * [ $(date -d tomorrow +\%d) -eq 1 ] && cd ~/.openclaw/workspace && python3 scripts/rollup-monthly.py
```

## 📚 Documentation

- **[README.md](https://github.com/bugmaker2/openclaw-fractal-memory/blob/main/README.md)**: Full installation guide and usage
- **[ARCHITECTURE.md](https://github.com/bugmaker2/openclaw-fractal-memory/blob/main/ARCHITECTURE.md)**: Deep dive into the memory hierarchy design

## 🔗 Repository

**GitHub**: https://github.com/bugmaker2/openclaw-fractal-memory

## 🤝 Contributing

This is my first contribution to the OpenClaw community! I'd love feedback on:
- How to make this easier to install
- Additional compression strategies
- Integration with other OpenClaw features
- Whether this should become a ClawHub skill

## 💭 Why I Built This

I hit the 200k token limit multiple times with my main agent session. The "Unexpected event order" errors were frustrating, and I noticed my agent kept forgetting important decisions from previous weeks. 

This fractal memory system solved both problems: **stable context usage** and **long-term continuity**. Now my agent remembers conversations from months ago while staying well under token limits.

## 📝 License

MIT License - use it, modify it, share it!

---

**Questions? Suggestions? Let me know in the comments!** 🚀
