#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Task Management System
Track task execution, history, and results
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import uuid


class TaskStatus(Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """Represents a task in the system"""
    id: str
    title: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    agent: Optional[str] = None
    intensity: str = "cot"
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_seconds: Optional[float] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    tags: List[str] = None
    metadata: Dict = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


class TaskManager:
    """Manage task execution and history"""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path.home() / ".claude" / "tasks" / "tasks.db"

        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                priority TEXT NOT NULL,
                agent TEXT,
                intensity TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                completed_at TEXT,
                duration_seconds REAL,
                result TEXT,
                error TEXT,
                tags TEXT,
                metadata TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS task_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT NOT NULL,
                agent TEXT NOT NULL,
                intensity TEXT NOT NULL,
                started_at TEXT NOT NULL,
                completed_at TEXT,
                duration_seconds REAL,
                status TEXT NOT NULL,
                quality_score REAL,
                tokens_used INTEGER,
                cost_usd REAL,
                output TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created ON tasks(created_at DESC)
        ''')

        self.conn.commit()

    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        agent: Optional[str] = None,
        intensity: str = "cot",
        tags: List[str] = None,
        metadata: Dict = None
    ) -> str:
        """Create a new task"""
        task_id = str(uuid.uuid4())[:8]

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            agent=agent,
            intensity=intensity,
            tags=tags or [],
            metadata=metadata or {}
        )

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (
                id, title, description, status, priority, agent, intensity,
                created_at, started_at, completed_at, duration_seconds,
                result, error, tags, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task.id,
            task.title,
            task.description,
            task.status.value,
            task.priority.value,
            task.agent,
            task.intensity,
            task.created_at,
            task.started_at,
            task.completed_at,
            task.duration_seconds,
            json.dumps(task.result) if task.result else None,
            task.error,
            json.dumps(task.tags),
            json.dumps(task.metadata)
        ))

        self.conn.commit()
        return task_id

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_task(row)
        return None

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        result: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        """Update task status and result"""
        cursor = self.conn.cursor()

        updates = {'status': status.value}

        if status == TaskStatus.RUNNING and not self.get_task(task_id).started_at:
            updates['started_at'] = datetime.now().isoformat()

        if status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            updates['completed_at'] = datetime.now().isoformat()

            # Calculate duration
            task = self.get_task(task_id)
            if task.started_at:
                start = datetime.fromisoformat(task.started_at)
                end = datetime.fromisoformat(updates['completed_at'])
                updates['duration_seconds'] = (end - start).total_seconds()

        if result:
            updates['result'] = json.dumps(result)

        if error:
            updates['error'] = error

        # Build update query
        set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [task_id]

        cursor.execute(f'UPDATE tasks SET {set_clause} WHERE id = ?', values)
        self.conn.commit()

    def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        limit: int = 50
    ) -> List[Task]:
        """List tasks with optional filters"""
        cursor = self.conn.cursor()

        conditions = []
        params = []

        if status:
            conditions.append("status = ?")
            params.append(status.value)

        if priority:
            conditions.append("priority = ?")
            params.append(priority.value)

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        cursor.execute(f'''
            SELECT * FROM tasks
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ?
        ''', params + [limit])

        return [self._row_to_task(row) for row in cursor.fetchall()]

    def record_execution(
        self,
        task_id: str,
        agent: str,
        intensity: str,
        status: TaskStatus,
        duration_seconds: float = 0,
        quality_score: float = 0,
        tokens_used: int = 0,
        cost_usd: float = 0,
        output: str = ""
    ):
        """Record a task execution"""
        cursor = self.conn.cursor()

        cursor.execute('''
            INSERT INTO task_executions (
                task_id, agent, intensity, started_at, completed_at,
                duration_seconds, status, quality_score, tokens_used,
                cost_usd, output
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            task_id,
            agent,
            intensity,
            datetime.now().isoformat(),
            datetime.now().isoformat(),
            duration_seconds,
            status.value,
            quality_score,
            tokens_used,
            cost_usd,
            output
        ))

        self.conn.commit()

    def get_task_history(self, task_id: str) -> List[Dict]:
        """Get execution history for a task"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT * FROM task_executions
            WHERE task_id = ?
            ORDER BY started_at DESC
        ''', (task_id,))

        return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict:
        """Get task statistics"""
        cursor = self.conn.cursor()

        # Total tasks by status
        cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM tasks
            GROUP BY status
        ''')
        by_status = {row['status']: row['count'] for row in cursor.fetchall()}

        # Total tasks by priority
        cursor.execute('''
            SELECT priority, COUNT(*) as count
            FROM tasks
            GROUP BY priority
        ''')
        by_priority = {row['priority']: row['count'] for row in cursor.fetchall()}

        # Average duration
        cursor.execute('''
            SELECT AVG(duration_seconds) as avg_duration
            FROM tasks
            WHERE status = 'completed' AND duration_seconds IS NOT NULL
        ''')
        avg_duration = cursor.fetchone()['avg_duration'] or 0

        # Success rate
        cursor.execute('''
            SELECT
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                COUNT(*) as total
            FROM tasks
            WHERE status IN ('completed', 'failed')
        ''')
        row = cursor.fetchone()
        success_rate = (row['completed'] / row['total']) if row['total'] > 0 else 0

        # Total tokens and cost
        cursor.execute('''
            SELECT
                SUM(tokens_used) as total_tokens,
                SUM(cost_usd) as total_cost
            FROM task_executions
        ''')
        row = cursor.fetchone()

        return {
            "by_status": by_status,
            "by_priority": by_priority,
            "average_duration_seconds": round(avg_duration, 2),
            "success_rate": round(success_rate, 3),
            "total_tokens_used": row['total_tokens'] or 0,
            "total_cost_usd": round(row['total_cost'] or 0, 2)
        }

    def search_tasks(self, query: str, limit: int = 20) -> List[Task]:
        """Search tasks by title or description"""
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT * FROM tasks
            WHERE title LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (f'%{query}%', f'%{query}%', limit))

        return [self._row_to_task(row) for row in cursor.fetchall()]

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        """Convert database row to Task object"""
        return Task(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=TaskStatus(row['status']),
            priority=TaskPriority(row['priority']),
            agent=row['agent'],
            intensity=row['intensity'],
            created_at=row['created_at'],
            started_at=row['started_at'],
            completed_at=row['completed_at'],
            duration_seconds=row['duration_seconds'],
            result=json.loads(row['result']) if row['result'] else None,
            error=row['error'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )

    def close(self):
        """Close database connection"""
        self.conn.close()


def demo_tasks():
    """Demonstration of task management"""
    print("📋 Task Management System Demo\n")
    print("=" * 60)

    manager = TaskManager()

    # Create tasks
    print("\n📝 Creating tasks...")

    task1 = manager.create_task(
        title="Refactor authentication",
        description="Modernize authentication with OAuth2",
        priority=TaskPriority.HIGH,
        agent="code-perfection-system",
        intensity="cot++",
        tags=["security", "refactoring"]
    )
    print(f"  ✓ Created task: {task1}")

    task2 = manager.create_task(
        title="Optimize database queries",
        description="Fix N+1 queries in user endpoint",
        priority=TaskPriority.CRITICAL,
        agent="database-optimizer",
        intensity="cot+",
        tags=["performance", "database"]
    )
    print(f"  ✓ Created task: {task2}")

    task3 = manager.create_task(
        title="Add unit tests",
        description="Increase test coverage to 80%",
        priority=TaskPriority.MEDIUM,
        agent="test-engineer",
        intensity="cot",
        tags=["testing", "quality"]
    )
    print(f"  ✓ Created task: {task3}")

    # Update task status
    print("\n🚀 Executing tasks...")
    manager.update_task_status(task1, TaskStatus.RUNNING)
    print(f"  ⏳ {task1}: RUNNING")

    import time
    time.sleep(0.5)

    manager.update_task_status(
        task1,
        TaskStatus.COMPLETED,
        result={"quality_score": 9.5, "artifacts": ["auth-refactored.js"]}
    )
    print(f"  ✅ {task1}: COMPLETED")

    # Record execution
    manager.record_execution(
        task_id=task1,
        agent="code-perfection-system",
        intensity="cot++",
        status=TaskStatus.COMPLETED,
        duration_seconds=125.3,
        quality_score=9.5,
        tokens_used=15234,
        cost_usd=0.45,
        output="Authentication refactored successfully"
    )

    # List tasks
    print("\n📋 All Tasks:")
    all_tasks = manager.list_tasks(limit=10)
    for task in all_tasks:
        status_icon = "✅" if task.status == TaskStatus.COMPLETED else "⏳" if task.status == TaskStatus.RUNNING else "📝"
        print(f"  {status_icon} [{task.priority.value.upper()}] {task.title}")
        print(f"     Agent: {task.agent} ({task.intensity})")
        print(f"     Status: {task.status.value}")
        if task.duration_seconds:
            print(f"     Duration: {task.duration_seconds:.1f}s")
        print()

    # Get statistics
    print("📊 Statistics:")
    stats = manager.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Search tasks
    print("\n🔍 Search 'database':")
    results = manager.search_tasks("database")
    for task in results:
        print(f"  • {task.title} ({task.status.value})")

    manager.close()


if __name__ == "__main__":
    demo_tasks()
