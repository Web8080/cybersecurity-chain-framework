#!/usr/bin/env python3
"""
Sprint Manager - Agile Sprint Management Tool
Author: Victor Ibhafidon

Manages Agile sprints, tracks progress, and generates sprint reports.

WHAT IT DOES:
- Creates and manages sprint objects
- Tracks user stories and their status
- Calculates sprint progress and velocity
- Generates sprint summaries and burndown data
- Saves/loads sprints to/from JSON files
- Integrates with backlog_manager.py for story planning

HOW IT CONNECTS TO THE FRAMEWORK:
- Stores sprint data in agile/sprints/*.json
- Used for tracking Sprint 1, Sprint 2, etc.
- Provides progress tracking for Agile workflow
- Generates reports for sprint reviews

USAGE:
    from agile.tools.sprint_manager import SprintManager, UserStory, StoryStatus
    
    manager = SprintManager()
    sprint = manager.create_sprint(1, "Foundation", "2025-12-30", "2026-01-13", "...", 21)
    manager.save_sprint(sprint)
    summary = manager.get_sprint_summary(sprint)
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class StoryStatus(Enum):
    """Status of a user story"""
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    BLOCKED = "Blocked"


@dataclass
class UserStory:
    """Represents a user story"""
    id: str
    title: str
    description: str
    story_points: int
    priority: str
    status: StoryStatus
    assignee: Optional[str] = None
    tasks: List[str] = None
    epic: Optional[str] = None
    
    def __post_init__(self):
        if self.tasks is None:
            self.tasks = []


@dataclass
class Sprint:
    """Represents a sprint"""
    number: int
    name: str
    start_date: str
    end_date: str
    goal: str
    capacity: int
    stories: List[UserStory] = None
    velocity: Optional[int] = None
    
    def __post_init__(self):
        if self.stories is None:
            self.stories = []
    
    def get_completed_points(self) -> int:
        """Get total completed story points"""
        return sum(
            story.story_points 
            for story in self.stories 
            if story.status == StoryStatus.DONE
        )
    
    def get_progress(self) -> float:
        """Get sprint progress percentage"""
        if self.capacity == 0:
            return 0.0
        return (self.get_completed_points() / self.capacity) * 100
    
    def get_remaining_points(self) -> int:
        """Get remaining story points"""
        return self.capacity - self.get_completed_points()


class SprintManager:
    """Manages sprints and tracks progress"""
    
    def __init__(self, base_dir: str = "agile"):
        self.base_dir = base_dir
        self.sprints_dir = os.path.join(base_dir, "sprints")
        self.current_sprint: Optional[Sprint] = None
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.sprints_dir, exist_ok=True)
    
    def create_sprint(self, number: int, name: str, start_date: str, 
                     end_date: str, goal: str, capacity: int) -> Sprint:
        """Create a new sprint"""
        sprint = Sprint(
            number=number,
            name=name,
            start_date=start_date,
            end_date=end_date,
            goal=goal,
            capacity=capacity
        )
        return sprint
    
    def add_story_to_sprint(self, sprint: Sprint, story: UserStory):
        """Add a user story to a sprint"""
        sprint.stories.append(story)
    
    def update_story_status(self, sprint: Sprint, story_id: str, 
                           new_status: StoryStatus):
        """Update the status of a user story"""
        for story in sprint.stories:
            if story.id == story_id:
                story.status = new_status
                return True
        return False
    
    def save_sprint(self, sprint: Sprint):
        """Save sprint to file"""
        filename = f"sprint_{sprint.number:03d}.json"
        filepath = os.path.join(self.sprints_dir, filename)
        
        # Convert to dict for JSON serialization
        sprint_dict = {
            "number": sprint.number,
            "name": sprint.name,
            "start_date": sprint.start_date,
            "end_date": sprint.end_date,
            "goal": sprint.goal,
            "capacity": sprint.capacity,
            "velocity": sprint.velocity,
            "stories": [
                {
                    "id": story.id,
                    "title": story.title,
                    "description": story.description,
                    "story_points": story.story_points,
                    "priority": story.priority,
                    "status": story.status.value,
                    "assignee": story.assignee,
                    "tasks": story.tasks,
                    "epic": story.epic
                }
                for story in sprint.stories
            ]
        }
        
        with open(filepath, 'w') as f:
            json.dump(sprint_dict, f, indent=2)
    
    def load_sprint(self, sprint_number: int) -> Optional[Sprint]:
        """Load a sprint from file"""
        filename = f"sprint_{sprint_number:03d}.json"
        filepath = os.path.join(self.sprints_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        sprint = Sprint(
            number=data["number"],
            name=data["name"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            goal=data["goal"],
            capacity=data["capacity"],
            velocity=data.get("velocity")
        )
        
        for story_data in data.get("stories", []):
            story = UserStory(
                id=story_data["id"],
                title=story_data["title"],
                description=story_data["description"],
                story_points=story_data["story_points"],
                priority=story_data["priority"],
                status=StoryStatus(story_data["status"]),
                assignee=story_data.get("assignee"),
                tasks=story_data.get("tasks", []),
                epic=story_data.get("epic")
            )
            sprint.stories.append(story)
        
        return sprint
    
    def get_sprint_summary(self, sprint: Sprint) -> str:
        """Generate a summary of the sprint"""
        summary = []
        summary.append("=" * 80)
        summary.append(f"SPRINT {sprint.number}: {sprint.name}")
        summary.append("=" * 80)
        summary.append(f"Goal: {sprint.goal}")
        summary.append(f"Duration: {sprint.start_date} to {sprint.end_date}")
        summary.append(f"Capacity: {sprint.capacity} story points")
        summary.append("")
        
        completed = sprint.get_completed_points()
        remaining = sprint.get_remaining_points()
        progress = sprint.get_progress()
        
        summary.append(f"Progress: {completed}/{sprint.capacity} points ({progress:.1f}%)")
        summary.append(f"Remaining: {remaining} points")
        summary.append("")
        
        summary.append("Stories:")
        for story in sprint.stories:
            status_icon = {
                StoryStatus.DONE: "✅",
                StoryStatus.IN_PROGRESS: "🔄",
                StoryStatus.BLOCKED: "🚫",
                StoryStatus.TODO: "⏳"
            }.get(story.status, "❓")
            
            summary.append(
                f"  {status_icon} [{story.id}] {story.title} "
                f"({story.story_points} pts, {story.status.value})"
            )
        
        summary.append("")
        summary.append("=" * 80)
        
        return "\n".join(summary)
    
    def generate_burndown_data(self, sprint: Sprint) -> List[Dict]:
        """Generate burndown chart data"""
        # This would ideally track daily progress
        # For now, return current state
        return [
            {
                "day": 1,
                "planned": sprint.capacity,
                "completed": sprint.get_completed_points(),
                "remaining": sprint.get_remaining_points()
            }
        ]


def main():
    """Example usage"""
    manager = SprintManager()
    
    # Create example sprint
    today = datetime.now()
    start_date = today.strftime("%Y-%m-%d")
    end_date = (today + timedelta(days=14)).strftime("%Y-%m-%d")
    
    sprint = manager.create_sprint(
        number=1,
        name="Foundation & Core Features",
        start_date=start_date,
        end_date=end_date,
        goal="Establish foundation and complete core attack chain analysis features",
        capacity=21
    )
    
    # Add example stories
    story1 = UserStory(
        id="US-001",
        title="Improve Chain Validation Logic",
        description="Enhance validation with better error messages",
        story_points=3,
        priority="High",
        status=StoryStatus.IN_PROGRESS,
        tasks=["Enhance validation", "Add tests", "Update docs"]
    )
    
    story2 = UserStory(
        id="US-005",
        title="Target-Specific Chain Templates",
        description="Create templates for each target",
        story_points=8,
        priority="High",
        status=StoryStatus.TODO,
        tasks=["Juice Shop templates", "DVWA templates", "bWAPP templates"]
    )
    
    manager.add_story_to_sprint(sprint, story1)
    manager.add_story_to_sprint(sprint, story2)
    
    # Save sprint
    manager.save_sprint(sprint)
    
    # Display summary
    print(manager.get_sprint_summary(sprint))
    
    # Load and display
    loaded_sprint = manager.load_sprint(1)
    if loaded_sprint:
        print("\n" + "=" * 80)
        print("LOADED SPRINT")
        print("=" * 80)
        print(manager.get_sprint_summary(loaded_sprint))


if __name__ == "__main__":
    main()


