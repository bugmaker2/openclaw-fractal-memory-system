#!/usr/bin/env python3
"""
Daily Rollup Script - Fractal Memory System (LLM-Enhanced)

Reads today's diary entry, uses LLM to extract patterns/decisions/key events,
and appends to this week's summary.

Run: python3 rollup-daily.py
Cron: 0 23 * * * cd ~/.openclaw/workspace && python3 rollup-daily.py
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
DIARY_DIR = MEMORY_DIR / "diary"
STATE_FILE = MEMORY_DIR / "rollup-state.json"

# LLM Configuration
USE_LLM = True  # Set to False to use heuristic extraction
LLM_MODEL = "deepseek"  # Fast and cheap for summarization

def get_week_number(date):
    """Get ISO week number (YYYY-Wnn format)"""
    return date.strftime("%Y-W%V")

def load_state():
    """Load rollup state from JSON"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "lastDailyRollup": None,
        "lastWeeklyRollup": None,
        "lastMonthlyRollup": None,
        "currentWeek": None,
        "currentMonth": None
    }

def save_state(state):
    """Save rollup state to JSON"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def read_daily_file(date):
    """Read daily diary file"""
    year = date.strftime("%Y")
    daily_file = DIARY_DIR / year / "daily" / f"{date.strftime('%Y-%m-%d')}.md"
    
    if not daily_file.exists():
        return None
    
    with open(daily_file, 'r', encoding='utf-8') as f:
        return f.read()

def extract_summary_llm(content, date):
    """
    Use LLM to extract key patterns, decisions, and events.
    
    This provides much better summarization than heuristics.
    """
    prompt = f"""You are a memory organization assistant. Extract key information from the following log and generate a concise daily summary.

**Date:** {date.strftime('%Y-%m-%d (%A)')}

**Original Log:**
{content}

**Extraction Requirements:**
1. **Key Events** - What important things were accomplished today
2. **Decisions & Reasoning** - What decisions were made and why
3. **Learning & Insights** - What new knowledge or skills were learned
4. **Follow-ups** - Items that need future attention
5. **Problems & Solutions** - Issues encountered and how they were resolved

**Output Format:**
Use Markdown, concise and clear, preserve key data and details.
Use ### headings for each section. Skip sections with no content.

**Example:**
### Key Events
- Completed stats-viz skill development (2 iterations, final version polished)
- Implemented new automation workflow

### Decisions & Reasoning
- Chose to subscribe to technical channels (avoid noise)
- Decided to integrate community best practices into existing system

### Learning & Insights
- 50+ agents independently discovered the same three-layer memory architecture
- "Write immediately" principle: Mental notes don't survive to next session

Now extract today's log:"""

    try:
        # Call OpenClaw's LLM via subprocess
        result = subprocess.run(
            ['openclaw', 'ask', '--model', LLM_MODEL, '--'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            summary = result.stdout.strip()
            if summary and len(summary) > 50:
                return summary
        
        print(f"⚠️  LLM extraction failed, falling back to heuristic")
        return None
        
    except Exception as e:
        print(f"⚠️  LLM error: {e}, falling back to heuristic")
        return None

def extract_summary_heuristic(content):
    """
    Heuristic-based extraction (fallback).
    
    Simple keyword matching for when LLM is unavailable.
    """
    if not content or len(content.strip()) < 50:
        return None
    
    lines = content.split('\n')
    summary_lines = []
    
    # Extract headers and important markers
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Keep headers (but skip top-level)
        if line.startswith('##') and not line.startswith('###'):
            summary_lines.append(line)
        # Keep lines with decision markers
        elif any(marker in line.lower() for marker in ['decided', 'learned', 'created', 'implemented', 'fixed', 'discovered', 'completed']):
            summary_lines.append(f"- {line}")
        # Keep lines with important keywords
        elif any(keyword in line.lower() for keyword in ['important', 'critical', 'key', 'milestone', 'breakthrough', 'insight']):
            summary_lines.append(f"- {line}")
    
    if not summary_lines:
        return "- Activity logged (no major events extracted)"
    
    return '\n'.join(summary_lines)

def extract_summary(content, date):
    """
    Extract summary using LLM or heuristic fallback.
    """
    if USE_LLM:
        llm_summary = extract_summary_llm(content, date)
        if llm_summary:
            return llm_summary
    
    # Fallback to heuristic
    return extract_summary_heuristic(content)

def append_to_weekly(date, summary):
    """Append daily summary to weekly file"""
    year = date.strftime("%Y")
    week = get_week_number(date)
    weekly_dir = DIARY_DIR / year / "weekly"
    weekly_dir.mkdir(parents=True, exist_ok=True)
    
    weekly_file = weekly_dir / f"{week}.md"
    
    # Create or append
    if not weekly_file.exists():
        header = f"# Week {week}\n\n"
        with open(weekly_file, 'w', encoding='utf-8') as f:
            f.write(header)
    
    # Append daily summary
    with open(weekly_file, 'a', encoding='utf-8') as f:
        f.write(f"\n## {date.strftime('%Y-%m-%d (%A)')}\n\n")
        f.write(summary)
        f.write("\n")

def main():
    """Main rollup logic"""
    print("🧠 Daily Rollup - Fractal Memory System (LLM-Enhanced)")
    print("=" * 50)
    
    # Load state
    state = load_state()
    
    # Determine which day to process
    today = datetime.now()
    target_date = today.date()
    
    # Check if we already processed today
    last_rollup = state.get("lastDailyRollup")
    if last_rollup:
        last_date = datetime.fromisoformat(last_rollup).date()
        if last_date == target_date:
            print(f"✓ Already processed {target_date}")
            return
    
    print(f"📅 Processing: {target_date}")
    print(f"🤖 LLM Mode: {'Enabled' if USE_LLM else 'Disabled'} (Model: {LLM_MODEL})")
    
    # Read daily file
    content = read_daily_file(target_date)
    if not content:
        print(f"⚠️  No diary file found for {target_date}")
        print(f"   Expected: memory/diary/{target_date.year}/daily/{target_date}.md")
        return
    
    print(f"📖 Read {len(content)} characters from daily file")
    
    # Extract summary
    summary = extract_summary(content, target_date)
    if not summary:
        print("⚠️  No significant content to summarize")
        return
    
    print(f"✨ Extracted summary ({len(summary)} characters)")
    
    # Append to weekly
    append_to_weekly(target_date, summary)
    week = get_week_number(target_date)
    print(f"✓ Appended to weekly summary: {week}")
    
    # Update state
    state["lastDailyRollup"] = today.isoformat()
    state["currentWeek"] = week
    state["currentMonth"] = target_date.strftime("%Y-%m")
    save_state(state)
    
    print("✓ State saved")
    print("=" * 50)
    print("✓ Daily rollup complete!")

if __name__ == "__main__":
    main()
