#!/usr/bin/env python3
"""
Product Backlog Manager - Agile Management Tool
Author: Victor Ibhafidon

Manages the product backlog for Agile development workflow.

WHAT IT DOES:
- Parses user stories from markdown backlog file
- Tracks backlog items with priorities and story points
- Filters items by priority, epic, or status
- Generates backlog summaries and statistics
- Integrates with sprint_manager.py for sprint planning

HOW IT CONNECTS TO THE FRAMEWORK:
- Reads from docs/product_backlog.md
- Used by sprint_manager.py to plan sprints
- Provides backlog statistics for planning
- Supports Agile methodology workflow

USAGE:
 from agile.tools.backlog_manager import BacklogManager
 
 manager = BacklogManager()
 summary = manager.generate_summary()
 high_priority = manager.get_items_by_priority(Priority.HIGH)
"""

import os
import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class Priority(Enum):
 """Story priority"""
 HIGH = "High"
 MEDIUM = "Medium"
 LOW = "Low"

@dataclass
class BacklogItem:
 """Represents a backlog item"""
 id: str
 title: str
 description: str
 story_points: int
 priority: Priority
 epic: str
 status: str = "Backlog"
 acceptance_criteria: List[str] = None
 
 def __post_init__(self):
 if self.acceptance_criteria is None:
 self.acceptance_criteria = []

class BacklogManager:
 """Manages product backlog"""
 
 def __init__(self, backlog_file: str = "docs/product_backlog.md"):
 self.backlog_file = backlog_file
 self.items: List[BacklogItem] = []
 self._load_from_markdown()
 
 def _load_from_markdown(self):
 """Load backlog items from markdown file"""
 if not os.path.exists(self.backlog_file):
 return
 
 with open(self.backlog_file, 'r') as f:
 content = f.read()
 
 # Parse user stories from markdown
 # Look for patterns like "### US-001: Title"
 pattern = r'### (US-\d+): (.+?)(?=###|$)'
 matches = re.finditer(pattern, content, re.DOTALL)
 
 for match in matches:
 story_id = match.group(1)
 rest = match.group(2)
 
 # Extract title (first line)
 lines = rest.strip().split('\n')
 title = lines[0].strip() if lines else "Untitled"
 
 # Extract other fields (simplified parsing)
 # In a real implementation, you'd parse more carefully
 item = BacklogItem(
 id=story_id,
 title=title,
 description="", # Would parse from markdown
 story_points=0, # Would parse from markdown
 priority=Priority.MEDIUM, # Would parse from markdown
 epic="Unknown" # Would parse from markdown
 )
 self.items.append(item)
 
 def add_item(self, item: BacklogItem):
 """Add an item to the backlog"""
 self.items.append(item)
 
 def get_items_by_priority(self, priority: Priority) -> List[BacklogItem]:
 """Get items filtered by priority"""
 return [item for item in self.items if item.priority == priority]
 
 def get_items_by_epic(self, epic: str) -> List[BacklogItem]:
 """Get items filtered by epic"""
 return [item for item in self.items if item.epic == epic]
 
 def get_total_points(self) -> int:
 """Get total story points in backlog"""
 return sum(item.story_points for item in self.items)
 
 def generate_summary(self) -> str:
 """Generate backlog summary"""
 summary = []
 summary.append("=" * 80)
 summary.append("PRODUCT BACKLOG SUMMARY")
 summary.append("=" * 80)
 summary.append(f"Total Items: {len(self.items)}")
 summary.append(f"Total Story Points: {self.get_total_points()}")
 summary.append("")
 
 # By priority
 high = len(self.get_items_by_priority(Priority.HIGH))
 medium = len(self.get_items_by_priority(Priority.MEDIUM))
 low = len(self.get_items_by_priority(Priority.LOW))
 
 summary.append("By Priority:")
 summary.append(f" High: {high}")
 summary.append(f" Medium: {medium}")
 summary.append(f" Low: {low}")
 summary.append("")
 
 # By epic
 epics = {}
 for item in self.items:
 if item.epic not in epics:
 epics[item.epic] = 0
 epics[item.epic] += 1
 
 summary.append("By Epic:")
 for epic, count in sorted(epics.items()):
 summary.append(f" {epic}: {count} items")
 
 summary.append("")
 summary.append("=" * 80)
 
 return "\n".join(summary)

def main():
 """Example usage"""
 manager = BacklogManager()
 print(manager.generate_summary())

if __name__ == "__main__":
 main()

