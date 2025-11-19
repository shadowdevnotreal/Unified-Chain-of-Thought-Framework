#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Agent Recommendation Engine
Intelligent agent selection based on task analysis and historical performance
"""

import json
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class CoTIntensity(Enum):
    """Chain of Thought intensity levels"""
    COT = "cot"         # Standard thinking (4K tokens)
    COT_PLUS = "cot+"   # Enhanced thinking (10K tokens)
    COT_PLUS_PLUS = "cot++"  # Maximum thinking (32K tokens)


class TaskComplexity(Enum):
    """Task complexity categories"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AgentRecommendation:
    """Individual agent recommendation"""
    agent_name: str
    intensity: CoTIntensity
    confidence: float  # 0.0 to 1.0
    reason: str
    estimated_duration: str
    priority: int


@dataclass
class WorkflowRecommendation:
    """Complete workflow recommendation"""
    recommended_chain: List[AgentRecommendation]
    estimated_total_time: str
    success_probability: float
    similar_past_tasks: int
    complexity: TaskComplexity
    metadata: Dict


# Agent capability mapping
AGENT_CAPABILITIES = {
    "code-perfection-system": {
        "keywords": ["refactor", "fix", "improve", "clean", "perfect", "systematic", "zero rework"],
        "categories": ["code-quality", "systematic-development", "multi-phase"],
        "complexity": ["medium", "high", "critical"],
        "pairs_well_with": ["test-engineer", "code-reviewer"],
        "avg_duration_minutes": 12,
        "success_rate": 0.987
    },
    "security-auditor": {
        "keywords": ["security", "vulnerability", "audit", "owasp", "cve", "exploit", "auth"],
        "categories": ["security", "compliance", "authentication"],
        "complexity": ["medium", "high", "critical"],
        "pairs_well_with": ["code-reviewer", "code-perfection-system"],
        "avg_duration_minutes": 5,
        "success_rate": 1.0
    },
    "performance": {
        "keywords": ["slow", "optimize", "performance", "speed", "latency", "bottleneck", "cache"],
        "categories": ["performance", "optimization", "profiling"],
        "complexity": ["low", "medium", "high"],
        "pairs_well_with": ["code-reviewer", "database-optimizer"],
        "avg_duration_minutes": 8,
        "success_rate": 0.962
    },
    "test-engineer": {
        "keywords": ["test", "coverage", "unit test", "integration test", "e2e", "testing"],
        "categories": ["testing", "quality-assurance", "coverage"],
        "complexity": ["low", "medium", "high"],
        "pairs_well_with": ["code-perfection-system", "code-reviewer"],
        "avg_duration_minutes": 10,
        "success_rate": 0.979
    },
    "code-reviewer": {
        "keywords": ["review", "quality", "lint", "best practices", "code quality"],
        "categories": ["code-quality", "review", "standards"],
        "complexity": ["low", "medium"],
        "pairs_well_with": ["security-auditor", "performance"],
        "avg_duration_minutes": 6,
        "success_rate": 0.993
    },
    "documentation": {
        "keywords": ["document", "docs", "readme", "api docs", "guide", "tutorial"],
        "categories": ["documentation", "knowledge-sharing"],
        "complexity": ["low", "medium"],
        "pairs_well_with": ["team-architect"],
        "avg_duration_minutes": 7,
        "success_rate": 0.959
    },
    "team-architect": {
        "keywords": ["architecture", "design", "system design", "multi-agent", "orchestrate"],
        "categories": ["architecture", "design", "planning"],
        "complexity": ["high", "critical"],
        "pairs_well_with": ["security-auditor", "performance"],
        "avg_duration_minutes": 15,
        "success_rate": 0.989
    },
    "accessibility": {
        "keywords": ["accessibility", "wcag", "a11y", "screen reader", "aria"],
        "categories": ["accessibility", "compliance", "usability"],
        "complexity": ["low", "medium"],
        "pairs_well_with": ["code-reviewer"],
        "avg_duration_minutes": 7,
        "success_rate": 0.970
    },
    "refactoring-specialist": {
        "keywords": ["refactor", "legacy", "modernize", "technical debt", "code smell"],
        "categories": ["refactoring", "modernization", "tech-debt"],
        "complexity": ["medium", "high", "critical"],
        "pairs_well_with": ["test-engineer", "code-perfection-system"],
        "avg_duration_minutes": 18,
        "success_rate": 0.962
    },
    "migration-specialist": {
        "keywords": ["migrate", "upgrade", "migration", "version", "framework upgrade"],
        "categories": ["migration", "upgrade", "transformation"],
        "complexity": ["high", "critical"],
        "pairs_well_with": ["test-engineer", "database-optimizer"],
        "avg_duration_minutes": 25,
        "success_rate": 0.941
    },
    "devops-automation": {
        "keywords": ["devops", "ci/cd", "pipeline", "deployment", "infrastructure", "docker", "kubernetes"],
        "categories": ["devops", "automation", "infrastructure"],
        "complexity": ["medium", "high"],
        "pairs_well_with": ["security-auditor"],
        "avg_duration_minutes": 14,
        "success_rate": 0.964
    },
    "database-optimizer": {
        "keywords": ["database", "query", "sql", "index", "performance", "slow query"],
        "categories": ["database", "optimization", "performance"],
        "complexity": ["medium", "high"],
        "pairs_well_with": ["performance"],
        "avg_duration_minutes": 11,
        "success_rate": 0.952
    }
}


class AgentRecommender:
    """Intelligent agent recommendation system"""

    def __init__(self, historical_data: Optional[Dict] = None):
        self.historical_data = historical_data or {}
        self.agent_capabilities = AGENT_CAPABILITIES

    def analyze_task(self, task_description: str, context: Optional[Dict] = None) -> Dict:
        """
        Analyze task to determine characteristics

        Args:
            task_description: Description of the task
            context: Additional context (complexity, security_critical, etc.)

        Returns:
            Task analysis dict with complexity, categories, keywords
        """
        context = context or {}
        task_lower = task_description.lower()

        # Extract keywords
        found_keywords = []
        for agent, data in self.agent_capabilities.items():
            for keyword in data["keywords"]:
                if keyword in task_lower:
                    found_keywords.append((agent, keyword))

        # Determine complexity
        complexity = self._determine_complexity(task_description, context)

        # Detect categories
        categories = self._detect_categories(task_lower, found_keywords)

        # Security critical check
        security_critical = context.get("security_critical", False) or \
                          any(k in task_lower for k in ["auth", "security", "password", "token", "credential"])

        return {
            "complexity": complexity,
            "categories": categories,
            "keywords": found_keywords,
            "security_critical": security_critical,
            "estimated_scope": self._estimate_scope(task_description),
            "context": context
        }

    def recommend(
        self,
        task_description: str,
        context: Optional[Dict] = None
    ) -> WorkflowRecommendation:
        """
        Recommend optimal agent chain for a task

        Args:
            task_description: What needs to be done
            context: Additional context like complexity, criticality

        Returns:
            WorkflowRecommendation with agent chain and metadata
        """
        # Analyze the task
        analysis = self.analyze_task(task_description, context)

        # Score all agents
        agent_scores = self._score_agents(analysis)

        # Build recommended chain
        chain = self._build_agent_chain(agent_scores, analysis)

        # Calculate metadata
        total_time = sum(a.estimated_duration_minutes for a, _, _ in agent_scores if any(r.agent_name == a for r in chain))
        success_prob = self._calculate_success_probability(chain)
        similar_tasks = self._find_similar_tasks(task_description)

        return WorkflowRecommendation(
            recommended_chain=chain,
            estimated_total_time=self._format_duration(total_time),
            success_probability=success_prob,
            similar_past_tasks=similar_tasks,
            complexity=analysis["complexity"],
            metadata={
                "analysis": analysis,
                "total_agents": len(chain),
                "parallel_possible": self._can_parallelize(chain)
            }
        )

    def _determine_complexity(self, task_description: str, context: Dict) -> TaskComplexity:
        """Determine task complexity"""
        if context.get("complexity"):
            return TaskComplexity(context["complexity"])

        task_lower = task_description.lower()
        critical_keywords = ["critical", "production", "emergency", "urgent", "security"]
        high_keywords = ["refactor", "migrate", "architecture", "system design"]
        medium_keywords = ["implement", "add feature", "optimize"]

        if any(k in task_lower for k in critical_keywords):
            return TaskComplexity.CRITICAL
        elif any(k in task_lower for k in high_keywords):
            return TaskComplexity.HIGH
        elif any(k in task_lower for k in medium_keywords):
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.LOW

    def _detect_categories(self, task_lower: str, found_keywords: List) -> List[str]:
        """Detect task categories"""
        categories = set()
        for agent, keyword in found_keywords:
            categories.update(self.agent_capabilities[agent]["categories"])
        return list(categories)

    def _estimate_scope(self, task_description: str) -> str:
        """Estimate task scope"""
        word_count = len(task_description.split())
        if word_count < 10:
            return "small"
        elif word_count < 30:
            return "medium"
        else:
            return "large"

    def _score_agents(self, analysis: Dict) -> List[Tuple[str, float, str]]:
        """
        Score agents based on task analysis

        Returns:
            List of (agent_name, score, reason) tuples, sorted by score
        """
        scores = []

        for agent, capabilities in self.agent_capabilities.items():
            score = 0.0
            reasons = []

            # Keyword matching (40% weight)
            keyword_matches = sum(1 for a, _ in analysis["keywords"] if a == agent)
            if keyword_matches > 0:
                score += 0.4 * min(keyword_matches / 3.0, 1.0)
                reasons.append(f"{keyword_matches} keyword matches")

            # Category matching (30% weight)
            category_matches = len(set(capabilities["categories"]) & set(analysis["categories"]))
            if category_matches > 0:
                score += 0.3 * (category_matches / len(capabilities["categories"]))
                reasons.append(f"{category_matches} category matches")

            # Complexity suitability (20% weight)
            if analysis["complexity"].value in capabilities["complexity"]:
                score += 0.2
                reasons.append("suitable complexity")

            # Historical success rate (10% weight)
            score += 0.1 * capabilities["success_rate"]

            # Security boost
            if analysis["security_critical"] and agent == "security-auditor":
                score += 0.3
                reasons.append("security critical task")

            if score > 0:
                scores.append((agent, score, " + ".join(reasons)))

        return sorted(scores, key=lambda x: x[1], reverse=True)

    def _build_agent_chain(
        self,
        agent_scores: List[Tuple[str, float, str]],
        analysis: Dict
    ) -> List[AgentRecommendation]:
        """Build recommended agent chain"""
        chain = []
        used_agents = set()

        # Select primary agents (score > 0.3)
        for agent, score, reason in agent_scores:
            if score > 0.3 and len(chain) < 5:  # Max 5 agents
                intensity = self._select_intensity(agent, analysis)
                duration = self.agent_capabilities[agent]["avg_duration_minutes"]

                chain.append(AgentRecommendation(
                    agent_name=agent,
                    intensity=intensity,
                    confidence=min(score, 1.0),
                    reason=reason,
                    estimated_duration=self._format_duration(duration),
                    priority=len(chain) + 1
                ))
                used_agents.add(agent)

        # Add complementary agents based on pairs_well_with
        for agent in list(used_agents):
            pairs = self.agent_capabilities[agent]["pairs_well_with"]
            for pair_agent in pairs:
                if pair_agent not in used_agents and len(chain) < 5:
                    # Check if pair_agent scored at all
                    pair_score = next((s for a, s, _ in agent_scores if a == pair_agent), 0)
                    if pair_score > 0.15:  # Threshold for complementary agents
                        intensity = self._select_intensity(pair_agent, analysis)
                        duration = self.agent_capabilities[pair_agent]["avg_duration_minutes"]

                        chain.append(AgentRecommendation(
                            agent_name=pair_agent,
                            intensity=intensity,
                            confidence=pair_score * 0.8,  # Lower confidence for complementary
                            reason=f"pairs well with {agent}",
                            estimated_duration=self._format_duration(duration),
                            priority=len(chain) + 1
                        ))
                        used_agents.add(pair_agent)
                        break

        return chain

    def _select_intensity(self, agent: str, analysis: Dict) -> CoTIntensity:
        """Select appropriate CoT intensity for agent"""
        complexity = analysis["complexity"]
        security_critical = analysis["security_critical"]

        # Critical tasks always use cot++
        if complexity == TaskComplexity.CRITICAL:
            return CoTIntensity.COT_PLUS_PLUS

        # Security critical tasks use cot++ for security agent
        if security_critical and agent == "security-auditor":
            return CoTIntensity.COT_PLUS_PLUS

        # High complexity uses cot+
        if complexity == TaskComplexity.HIGH:
            return CoTIntensity.COT_PLUS

        # Medium complexity uses cot+ for complex agents
        if complexity == TaskComplexity.MEDIUM:
            complex_agents = ["team-architect", "code-perfection-system", "migration-specialist"]
            return CoTIntensity.COT_PLUS if agent in complex_agents else CoTIntensity.COT

        # Low complexity uses cot
        return CoTIntensity.COT

    def _calculate_success_probability(self, chain: List[AgentRecommendation]) -> float:
        """Calculate overall success probability"""
        if not chain:
            return 0.0

        # Combine agent success rates
        individual_rates = [
            self.agent_capabilities[rec.agent_name]["success_rate"]
            for rec in chain
        ]

        # Overall probability is product of individual rates
        overall = 1.0
        for rate in individual_rates:
            overall *= rate

        return round(overall, 3)

    def _find_similar_tasks(self, task_description: str) -> int:
        """Find similar historical tasks"""
        # TODO: Implement similarity search in historical data
        # For now, return mock data
        return len(task_description.split()) % 20  # Mock: 0-19 similar tasks

    def _can_parallelize(self, chain: List[AgentRecommendation]) -> bool:
        """Check if any agents can run in parallel"""
        # Some agents can run independently
        independent_agents = ["documentation", "accessibility", "test-engineer"]
        independent_count = sum(1 for rec in chain if rec.agent_name in independent_agents)
        return independent_count >= 2

    def _format_duration(self, minutes: int) -> str:
        """Format duration as human-readable string"""
        if minutes < 60:
            return f"{minutes}m"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}m" if mins > 0 else f"{hours}h"


def main():
    """Example usage"""
    recommender = AgentRecommender()

    # Example 1: Refactor authentication module
    print("=" * 60)
    print("Example 1: Refactor authentication module")
    print("=" * 60)

    result = recommender.recommend(
        task_description="Refactor authentication module with OAuth2 support",
        context={"complexity": "high", "security_critical": True}
    )

    print(f"\nComplexity: {result.complexity.value}")
    print(f"Estimated Time: {result.estimated_total_time}")
    print(f"Success Probability: {result.success_probability * 100}%")
    print(f"Similar Past Tasks: {result.similar_past_tasks}")
    print(f"\nRecommended Agent Chain ({len(result.recommended_chain)} agents):")

    for rec in result.recommended_chain:
        print(f"  {rec.priority}. {rec.agent_name} ({rec.intensity.value})")
        print(f"     Reason: {rec.reason}")
        print(f"     Confidence: {rec.confidence * 100:.1f}%")
        print(f"     Duration: {rec.estimated_duration}")
        print()

    # Example 2: Optimize slow database queries
    print("=" * 60)
    print("Example 2: Optimize slow database queries")
    print("=" * 60)

    result2 = recommender.recommend(
        task_description="Fix slow queries in user dashboard, optimize database performance",
        context={"complexity": "medium"}
    )

    print(f"\nComplexity: {result2.complexity.value}")
    print(f"Estimated Time: {result2.estimated_total_time}")
    print(f"Success Probability: {result2.success_probability * 100}%")
    print(f"\nRecommended Agent Chain ({len(result2.recommended_chain)} agents):")

    for rec in result2.recommended_chain:
        print(f"  {rec.priority}. {rec.agent_name} ({rec.intensity.value}) - {rec.reason}")


if __name__ == "__main__":
    main()
