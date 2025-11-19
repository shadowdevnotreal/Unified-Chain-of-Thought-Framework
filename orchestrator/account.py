#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Account & API Information
Track API usage, limits, and cost for logged-in Claude accounts
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class APIUsage:
    """API usage information"""
    period: str  # daily, weekly, monthly
    requests_made: int
    tokens_input: int
    tokens_output: int
    tokens_total: int
    cost_usd: float
    average_request_tokens: float
    peak_usage_hour: Optional[str] = None


@dataclass
class AccountInfo:
    """Account information"""
    user_id: str
    plan: str  # free, pro, team, enterprise
    api_key_prefix: str
    created_at: str
    last_active: str
    total_requests: int
    total_tokens: int
    total_cost_usd: float


@dataclass
class RateLimits:
    """Rate limit information"""
    requests_per_minute: int
    requests_per_day: int
    tokens_per_minute: int
    tokens_per_day: int
    current_rpm: int
    current_tpm: int
    rpm_limit_reached: bool
    tpm_limit_reached: bool


class AccountManager:
    """Manage account information and API usage"""

    def __init__(self, config_path: Optional[Path] = None):
        if config_path is None:
            config_path = Path.home() / ".claude" / "account" / "usage.json"

        config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path = config_path
        self.usage_data = self._load_usage_data()

    def _load_usage_data(self) -> Dict:
        """Load usage data from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {
            "account": {},
            "daily_usage": [],
            "weekly_usage": [],
            "monthly_usage": []
        }

    def _save_usage_data(self):
        """Save usage data to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.usage_data, f, indent=2)

    def get_account_info(self) -> AccountInfo:
        """Get account information"""
        # In production, this would query the Claude API
        # For now, return mock data based on environment

        api_key = os.getenv('ANTHROPIC_API_KEY', '')
        api_key_prefix = api_key[:8] + '...' if api_key else 'Not configured'

        # Determine plan from API key or usage
        plan = self._determine_plan()

        return AccountInfo(
            user_id=os.getenv('USER', 'unknown'),
            plan=plan,
            api_key_prefix=api_key_prefix,
            created_at=self.usage_data.get('account', {}).get('created_at', datetime.now().isoformat()),
            last_active=datetime.now().isoformat(),
            total_requests=self.usage_data.get('account', {}).get('total_requests', 0),
            total_tokens=self.usage_data.get('account', {}).get('total_tokens', 0),
            total_cost_usd=self.usage_data.get('account', {}).get('total_cost_usd', 0.0)
        )

    def _determine_plan(self) -> str:
        """Determine account plan based on usage patterns"""
        total_tokens = self.usage_data.get('account', {}).get('total_tokens', 0)

        if total_tokens > 1000000:
            return "enterprise"
        elif total_tokens > 100000:
            return "team"
        elif total_tokens > 10000:
            return "pro"
        else:
            return "free"

    def get_rate_limits(self) -> RateLimits:
        """Get current rate limit information"""
        # Rate limits vary by plan
        account = self.get_account_info()

        limits_by_plan = {
            "free": {
                "rpm": 5,
                "rpd": 100,
                "tpm": 10000,
                "tpd": 100000
            },
            "pro": {
                "rpm": 50,
                "rpd": 10000,
                "tpm": 100000,
                "tpd": 5000000
            },
            "team": {
                "rpm": 100,
                "rpd": 50000,
                "tpm": 200000,
                "tpd": 10000000
            },
            "enterprise": {
                "rpm": 500,
                "rpd": 500000,
                "tpm": 1000000,
                "tpd": 50000000
            }
        }

        limits = limits_by_plan.get(account.plan, limits_by_plan["free"])

        # Get current usage
        current_rpm = self._get_current_rpm()
        current_tpm = self._get_current_tpm()

        return RateLimits(
            requests_per_minute=limits["rpm"],
            requests_per_day=limits["rpd"],
            tokens_per_minute=limits["tpm"],
            tokens_per_day=limits["tpd"],
            current_rpm=current_rpm,
            current_tpm=current_tpm,
            rpm_limit_reached=(current_rpm >= limits["rpm"]),
            tpm_limit_reached=(current_tpm >= limits["tpm"])
        )

    def _get_current_rpm(self) -> int:
        """Get requests in the last minute"""
        # Mock implementation
        return 3

    def _get_current_tpm(self) -> int:
        """Get tokens in the last minute"""
        # Mock implementation
        return 1500

    def get_usage(self, period: str = "daily") -> APIUsage:
        """Get usage for a specific period"""
        usage_data = self.usage_data.get(f"{period}_usage", [])

        if not usage_data:
            return APIUsage(
                period=period,
                requests_made=0,
                tokens_input=0,
                tokens_output=0,
                tokens_total=0,
                cost_usd=0.0,
                average_request_tokens=0.0
            )

        latest = usage_data[-1] if usage_data else {}

        return APIUsage(
            period=period,
            requests_made=latest.get('requests', 0),
            tokens_input=latest.get('tokens_input', 0),
            tokens_output=latest.get('tokens_output', 0),
            tokens_total=latest.get('tokens_total', 0),
            cost_usd=latest.get('cost_usd', 0.0),
            average_request_tokens=latest.get('avg_tokens', 0.0),
            peak_usage_hour=latest.get('peak_hour')
        )

    def record_usage(
        self,
        tokens_input: int,
        tokens_output: int,
        cost_usd: float
    ):
        """Record API usage"""
        today = datetime.now().date().isoformat()

        # Update account totals
        if 'account' not in self.usage_data:
            self.usage_data['account'] = {}

        account = self.usage_data['account']
        account['total_requests'] = account.get('total_requests', 0) + 1
        account['total_tokens'] = account.get('total_tokens', 0) + tokens_input + tokens_output
        account['total_cost_usd'] = account.get('total_cost_usd', 0.0) + cost_usd
        account['last_updated'] = datetime.now().isoformat()

        # Update daily usage
        daily = self.usage_data.get('daily_usage', [])
        if not daily or daily[-1].get('date') != today:
            daily.append({
                'date': today,
                'requests': 0,
                'tokens_input': 0,
                'tokens_output': 0,
                'tokens_total': 0,
                'cost_usd': 0.0
            })

        daily[-1]['requests'] += 1
        daily[-1]['tokens_input'] += tokens_input
        daily[-1]['tokens_output'] += tokens_output
        daily[-1]['tokens_total'] += tokens_input + tokens_output
        daily[-1]['cost_usd'] += cost_usd

        self.usage_data['daily_usage'] = daily[-30:]  # Keep last 30 days

        self._save_usage_data()

    def get_usage_trends(self) -> Dict:
        """Get usage trends over time"""
        daily = self.usage_data.get('daily_usage', [])

        if len(daily) < 2:
            return {
                "trend": "insufficient_data",
                "change_percent": 0,
                "recommendation": "Need more data to analyze trends"
            }

        # Compare last 7 days to previous 7 days
        last_7 = daily[-7:] if len(daily) >= 7 else daily
        prev_7 = daily[-14:-7] if len(daily) >= 14 else []

        last_7_total = sum(d.get('tokens_total', 0) for d in last_7)
        prev_7_total = sum(d.get('tokens_total', 0) for d in prev_7) if prev_7 else last_7_total

        if prev_7_total > 0:
            change_percent = ((last_7_total - prev_7_total) / prev_7_total) * 100
        else:
            change_percent = 0

        trend = "increasing" if change_percent > 10 else "decreasing" if change_percent < -10 else "stable"

        recommendations = {
            "increasing": "Usage is increasing. Consider upgrading plan if nearing limits.",
            "decreasing": "Usage is decreasing. Monitor for any issues or reduced productivity.",
            "stable": "Usage is stable. Current plan seems appropriate."
        }

        return {
            "trend": trend,
            "change_percent": round(change_percent, 1),
            "recommendation": recommendations[trend],
            "last_7_days_tokens": last_7_total,
            "previous_7_days_tokens": prev_7_total
        }

    def get_cost_projection(self, days: int = 30) -> Dict:
        """Project costs based on current usage"""
        daily = self.usage_data.get('daily_usage', [])

        if not daily:
            return {
                "projection_days": days,
                "projected_cost_usd": 0.0,
                "daily_average_usd": 0.0
            }

        # Calculate daily average from last 7 days
        last_7 = daily[-7:] if len(daily) >= 7 else daily
        daily_avg = sum(d.get('cost_usd', 0) for d in last_7) / len(last_7)

        projected_cost = daily_avg * days

        return {
            "projection_days": days,
            "projected_cost_usd": round(projected_cost, 2),
            "daily_average_usd": round(daily_avg, 2),
            "confidence": "high" if len(last_7) >= 7 else "low"
        }

    def export_usage_report(self, output_path: Path):
        """Export usage report to file"""
        account = self.get_account_info()
        daily_usage = self.get_usage("daily")
        limits = self.get_rate_limits()
        trends = self.get_usage_trends()
        projection = self.get_cost_projection()

        report = {
            "generated_at": datetime.now().isoformat(),
            "account": asdict(account),
            "usage": {
                "daily": asdict(daily_usage)
            },
            "limits": asdict(limits),
            "trends": trends,
            "cost_projection_30_days": projection
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)


def demo_account():
    """Demonstration of account management"""
    print("👤 Account & API Information Demo\n")
    print("=" * 60)

    manager = AccountManager()

    # Get account info
    print("\n📋 Account Information:")
    account = manager.get_account_info()
    print(f"  User: {account.user_id}")
    print(f"  Plan: {account.plan}")
    print(f"  API Key: {account.api_key_prefix}")
    print(f"  Total Requests: {account.total_requests:,}")
    print(f"  Total Tokens: {account.total_tokens:,}")
    print(f"  Total Cost: ${account.total_cost_usd:.2f}")

    # Get rate limits
    print("\n⚡ Rate Limits:")
    limits = manager.get_rate_limits()
    print(f"  Requests/min: {limits.current_rpm}/{limits.requests_per_minute}")
    print(f"  Requests/day: {limits.requests_per_day:,}")
    print(f"  Tokens/min: {limits.current_tpm:,}/{limits.tokens_per_minute:,}")
    print(f"  Tokens/day: {limits.tokens_per_day:,}")

    if limits.rpm_limit_reached or limits.tpm_limit_reached:
        print("  ⚠️  Rate limit reached!")
    else:
        print("  ✅ Within limits")

    # Record some usage
    print("\n📝 Recording usage...")
    manager.record_usage(tokens_input=1000, tokens_output=2000, cost_usd=0.15)
    manager.record_usage(tokens_input=1500, tokens_output=2500, cost_usd=0.20)
    print("  ✓ Recorded 2 requests")

    # Get usage
    print("\n📊 Daily Usage:")
    usage = manager.get_usage("daily")
    print(f"  Requests: {usage.requests_made}")
    print(f"  Input Tokens: {usage.tokens_input:,}")
    print(f"  Output Tokens: {usage.tokens_output:,}")
    print(f"  Total Tokens: {usage.tokens_total:,}")
    print(f"  Cost: ${usage.cost_usd:.2f}")

    # Get trends
    print("\n📈 Usage Trends:")
    trends = manager.get_usage_trends()
    print(f"  Trend: {trends['trend']}")
    print(f"  Change: {trends['change_percent']:+.1f}%")
    print(f"  Recommendation: {trends['recommendation']}")

    # Cost projection
    print("\n💰 Cost Projection (30 days):")
    projection = manager.get_cost_projection()
    print(f"  Daily Average: ${projection['daily_average_usd']:.2f}")
    print(f"  30-Day Projection: ${projection['projected_cost_usd']:.2f}")
    print(f"  Confidence: {projection['confidence']}")

    # Export report
    report_path = Path("/tmp/usage-report.json")
    manager.export_usage_report(report_path)
    print(f"\n📄 Report exported to: {report_path}")


if __name__ == "__main__":
    demo_account()
