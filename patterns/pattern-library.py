#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Pattern Library Management
Centralized knowledge base for learned patterns and solutions
"""

import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class PatternCategory(Enum):
    """Pattern categories"""
    AUTHENTICATION = "authentication"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    DEVOPS = "devops"
    TESTING = "testing"
    SECURITY = "security"
    PERFORMANCE = "performance"
    ARCHITECTURE = "architecture"
    REFACTORING = "refactoring"


class DifficultyLevel(Enum):
    """Pattern difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


@dataclass
class Pattern:
    """Represents a learned pattern"""
    id: str
    name: str
    category: PatternCategory
    difficulty: DifficultyLevel
    context: str
    solution: str
    code_template: Optional[str] = None
    times_used: int = 0
    success_rate: float = 0.0
    created_at: str = ""
    last_used: str = ""
    related_patterns: List[str] = None
    agents_used: List[str] = None
    metrics: Dict = None
    tags: List[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if self.related_patterns is None:
            self.related_patterns = []
        if self.agents_used is None:
            self.agents_used = []
        if self.metrics is None:
            self.metrics = {}
        if self.tags is None:
            self.tags = []


class PatternLibrary:
    """Pattern library manager with SQLite backend"""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path.home() / ".claude" / "patterns" / "library.db"

        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path))
        self.conn.row_factory = sqlite3.Row
        self._initialize_database()

    def _initialize_database(self):
        """Create database schema"""
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                difficulty TEXT NOT NULL,
                context TEXT NOT NULL,
                solution TEXT NOT NULL,
                code_template TEXT,
                times_used INTEGER DEFAULT 0,
                success_rate REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                last_used TEXT,
                related_patterns TEXT,
                agents_used TEXT,
                metrics TEXT,
                tags TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT NOT NULL,
                used_at TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                task_description TEXT,
                duration_seconds INTEGER,
                quality_score REAL,
                FOREIGN KEY (pattern_id) REFERENCES patterns (id)
            )
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_category ON patterns(category)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_difficulty ON patterns(difficulty)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_times_used ON patterns(times_used DESC)
        ''')

        self.conn.commit()

    def add_pattern(self, pattern: Pattern) -> bool:
        """Add a new pattern to the library"""
        cursor = self.conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO patterns (
                    id, name, category, difficulty, context, solution,
                    code_template, times_used, success_rate, created_at,
                    last_used, related_patterns, agents_used, metrics, tags
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.id,
                pattern.name,
                pattern.category.value,
                pattern.difficulty.value,
                pattern.context,
                pattern.solution,
                pattern.code_template,
                pattern.times_used,
                pattern.success_rate,
                pattern.created_at,
                pattern.last_used,
                json.dumps(pattern.related_patterns),
                json.dumps(pattern.agents_used),
                json.dumps(pattern.metrics),
                json.dumps(pattern.tags)
            ))

            self.conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

    def get_pattern(self, pattern_id: str) -> Optional[Pattern]:
        """Retrieve a pattern by ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM patterns WHERE id = ?', (pattern_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_pattern(row)
        return None

    def search_patterns(
        self,
        query: Optional[str] = None,
        category: Optional[PatternCategory] = None,
        difficulty: Optional[DifficultyLevel] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Pattern]:
        """Search for patterns"""
        cursor = self.conn.cursor()

        conditions = []
        params = []

        if query:
            conditions.append("(name LIKE ? OR context LIKE ? OR solution LIKE ?)")
            query_param = f"%{query}%"
            params.extend([query_param, query_param, query_param])

        if category:
            conditions.append("category = ?")
            params.append(category.value)

        if difficulty:
            conditions.append("difficulty = ?")
            params.append(difficulty.value)

        if tags:
            for tag in tags:
                conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        cursor.execute(f'''
            SELECT * FROM patterns
            WHERE {where_clause}
            ORDER BY times_used DESC, success_rate DESC
            LIMIT ?
        ''', params + [limit])

        return [self._row_to_pattern(row) for row in cursor.fetchall()]

    def get_top_patterns(self, limit: int = 10) -> List[Pattern]:
        """Get most used patterns"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM patterns
            ORDER BY times_used DESC, success_rate DESC
            LIMIT ?
        ''', (limit,))

        return [self._row_to_pattern(row) for row in cursor.fetchall()]

    def record_usage(
        self,
        pattern_id: str,
        success: bool,
        task_description: str = "",
        duration_seconds: int = 0,
        quality_score: float = 0.0
    ):
        """Record pattern usage"""
        cursor = self.conn.cursor()

        # Record in usage table
        cursor.execute('''
            INSERT INTO pattern_usage (
                pattern_id, used_at, success, task_description,
                duration_seconds, quality_score
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pattern_id,
            datetime.now().isoformat(),
            success,
            task_description,
            duration_seconds,
            quality_score
        ))

        # Update pattern statistics
        cursor.execute('''
            UPDATE patterns
            SET times_used = times_used + 1,
                last_used = ?,
                success_rate = (
                    SELECT AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END)
                    FROM pattern_usage
                    WHERE pattern_id = ?
                )
            WHERE id = ?
        ''', (datetime.now().isoformat(), pattern_id, pattern_id))

        self.conn.commit()

    def get_similar_patterns(self, pattern_id: str, limit: int = 5) -> List[Pattern]:
        """Find patterns similar to the given pattern"""
        pattern = self.get_pattern(pattern_id)
        if not pattern:
            return []

        # Search by category and tags
        return self.search_patterns(
            category=pattern.category,
            tags=pattern.tags,
            limit=limit
        )

    def get_statistics(self) -> Dict:
        """Get library statistics"""
        cursor = self.conn.cursor()

        cursor.execute('SELECT COUNT(*) as total FROM patterns')
        total_patterns = cursor.fetchone()['total']

        cursor.execute('''
            SELECT category, COUNT(*) as count
            FROM patterns
            GROUP BY category
            ORDER BY count DESC
        ''')
        by_category = {row['category']: row['count'] for row in cursor.fetchall()}

        cursor.execute('SELECT AVG(success_rate) as avg_rate FROM patterns')
        avg_success_rate = cursor.fetchone()['avg_rate'] or 0.0

        cursor.execute('SELECT SUM(times_used) as total FROM patterns')
        total_usage = cursor.fetchone()['total'] or 0

        cursor.execute('''
            SELECT SUM(duration_seconds) as total
            FROM pattern_usage
            WHERE success = 1
        ''')
        time_saved_seconds = cursor.fetchone()['total'] or 0

        return {
            "total_patterns": total_patterns,
            "by_category": by_category,
            "average_success_rate": round(avg_success_rate, 3),
            "total_usage_count": total_usage,
            "time_saved_hours": round(time_saved_seconds / 3600, 1)
        }

    def export_patterns(self, output_path: Path):
        """Export all patterns to JSON"""
        patterns = self.search_patterns(limit=10000)
        data = [asdict(p) for p in patterns]

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def import_patterns(self, input_path: Path):
        """Import patterns from JSON"""
        with open(input_path, 'r') as f:
            data = json.load(f)

        for pattern_data in data:
            pattern_data['category'] = PatternCategory(pattern_data['category'])
            pattern_data['difficulty'] = DifficultyLevel(pattern_data['difficulty'])
            pattern = Pattern(**pattern_data)
            self.add_pattern(pattern)

    def _row_to_pattern(self, row: sqlite3.Row) -> Pattern:
        """Convert database row to Pattern object"""
        return Pattern(
            id=row['id'],
            name=row['name'],
            category=PatternCategory(row['category']),
            difficulty=DifficultyLevel(row['difficulty']),
            context=row['context'],
            solution=row['solution'],
            code_template=row['code_template'],
            times_used=row['times_used'],
            success_rate=row['success_rate'],
            created_at=row['created_at'],
            last_used=row['last_used'],
            related_patterns=json.loads(row['related_patterns']) if row['related_patterns'] else [],
            agents_used=json.loads(row['agents_used']) if row['agents_used'] else [],
            metrics=json.loads(row['metrics']) if row['metrics'] else {},
            tags=json.loads(row['tags']) if row['tags'] else []
        )

    def close(self):
        """Close database connection"""
        self.conn.close()


def generate_pattern_id(name: str) -> str:
    """Generate unique pattern ID"""
    hash_obj = hashlib.md5(name.encode())
    return f"PLM-{hash_obj.hexdigest()[:6].upper()}"


def main():
    """Example usage"""
    library = PatternLibrary()

    # Add sample patterns
    patterns = [
        Pattern(
            id=generate_pattern_id("JWT Token Refresh"),
            name="JWT Token Refresh Pattern",
            category=PatternCategory.AUTHENTICATION,
            difficulty=DifficultyLevel.MEDIUM,
            context="Implementing token refresh without user re-authentication",
            solution="Use sliding window with refresh token rotation. Access token: 15min expiry, Refresh token: 7 day expiry with automatic renewal on API calls.",
            code_template="""// JWT Refresh Implementation
const refreshToken = async (oldToken) => {
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${oldToken}` }
  });
  return response.json();
};""",
            tags=["jwt", "authentication", "security"],
            agents_used=["security-auditor", "code-perfection-system"]
        ),
        Pattern(
            id=generate_pattern_id("React State Management"),
            name="React State Management with Context",
            category=PatternCategory.FRONTEND,
            difficulty=DifficultyLevel.MEDIUM,
            context="Managing global state across React components without prop drilling",
            solution="Use React Context API with custom hooks for type-safe state management. Separate contexts by domain for better performance.",
            code_template="""// Context Implementation
const AuthContext = createContext();
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};""",
            tags=["react", "state-management", "frontend"],
            agents_used=["code-perfection-system", "performance"]
        ),
        Pattern(
            id=generate_pattern_id("API Rate Limiting"),
            name="API Rate Limiting with Redis",
            category=PatternCategory.BACKEND,
            difficulty=DifficultyLevel.MEDIUM,
            context="Preventing API abuse with distributed rate limiting",
            solution="Implement token bucket algorithm using Redis INCR with expiration. Track requests per IP/user with sliding window.",
            code_template="""// Rate Limiting Middleware
const rateLimit = async (req, res, next) => {
  const key = `rate:${req.ip}`;
  const current = await redis.incr(key);
  if (current === 1) await redis.expire(key, 60);
  if (current > 100) return res.status(429).json({ error: 'Too many requests' });
  next();
};""",
            tags=["api", "rate-limiting", "redis", "security"],
            agents_used=["security-auditor", "performance"]
        )
    ]

    # Add patterns
    for pattern in patterns:
        if library.add_pattern(pattern):
            print(f"✓ Added pattern: {pattern.name}")

    # Record usage
    library.record_usage(patterns[0].id, success=True, duration_seconds=1380, quality_score=9.8)
    library.record_usage(patterns[0].id, success=True, duration_seconds=1200, quality_score=9.5)
    library.record_usage(patterns[1].id, success=True, duration_seconds=1080, quality_score=9.2)

    # Search patterns
    print("\n--- Searching for 'authentication' patterns ---")
    results = library.search_patterns(query="authentication")
    for p in results:
        print(f"  {p.id}: {p.name} (used {p.times_used} times, {p.success_rate*100:.1f}% success)")

    # Get top patterns
    print("\n--- Top Patterns ---")
    top = library.get_top_patterns(limit=5)
    for idx, p in enumerate(top, 1):
        print(f"  {idx}. {p.name} - {p.times_used} uses, {p.success_rate*100:.1f}% success")

    # Get statistics
    print("\n--- Library Statistics ---")
    stats = library.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    library.close()


if __name__ == "__main__":
    main()
