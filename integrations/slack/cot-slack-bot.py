#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Slack Integration
Slash commands and bot for team collaboration
"""

import os
import json
from typing import Dict, List
from flask import Flask, request, jsonify
import sys
from pathlib import Path

# Add orchestrator to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "orchestrator"))

try:
    from recommender import AgentRecommender
except ImportError:
    AgentRecommender = None


app = Flask(__name__)

# Slack configuration (set via environment variables)
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN', '')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET', '')

# Initialize recommender
recommender = AgentRecommender() if AgentRecommender else None


@app.route('/slack/commands/cot', methods=['POST'])
def handle_cot_command():
    """
    Handle /cot slash command in Slack

    Usage:
      /cot review PR #1234
      /cot audit security high-priority
      /cot optimize database queries
    """
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    command_text = data.get('text', '').strip()

    if not command_text:
        return jsonify({
            "response_type": "ephemeral",
            "text": "ℹ️ *Unified CoT Framework v3.0*\n\n*Usage:*\n  /cot <task description>\n\n*Examples:*\n  /cot review PR #1234\n  /cot audit security\n  /cot optimize performance"
        })

    # Parse command
    action, description = parse_command(command_text)

    # Get recommendation
    if recommender:
        result = recommender.recommend(
            task_description=description,
            context={"source": "slack", "user": user_id}
        )

        # Format response
        response = format_slack_response(result, description)
    else:
        response = {
            "response_type": "in_channel",
            "text": f"🤖 Processing: {description}",
            "attachments": [{
                "color": "warning",
                "text": "⚠️ Orchestrator offline. Running in basic mode."
            }]
        }

    return jsonify(response)


@app.route('/slack/commands/cot-metrics', methods=['POST'])
def handle_metrics_command():
    """
    Handle /cot-metrics slash command

    Usage:
      /cot-metrics daily
      /cot-metrics weekly
      /cot-metrics team
    """
    data = request.form
    period = data.get('text', 'daily').strip().lower()

    # Mock metrics (in production, fetch from database)
    metrics = get_metrics_summary(period)

    response = {
        "response_type": "in_channel",
        "text": f"📊 *CoT Framework Metrics - {period.title()}*",
        "attachments": [{
            "color": "good",
            "fields": [
                {"title": "Tasks Completed", "value": str(metrics['tasks']), "short": True},
                {"title": "Success Rate", "value": f"{metrics['success_rate']}%", "short": True},
                {"title": "Avg Quality", "value": f"{metrics['quality']}/10", "short": True},
                {"title": "Time Saved", "value": f"{metrics['time_saved']}h", "short": True}
            ]
        }]
    }

    return jsonify(response)


@app.route('/slack/commands/cot-agents', methods=['POST'])
def handle_agents_command():
    """List available agents"""
    agents = [
        {"name": "Code Perfection System", "icon": "🎯", "desc": "Systematic code perfection"},
        {"name": "Security Auditor", "icon": "🔒", "desc": "Security & compliance"},
        {"name": "Performance Optimizer", "icon": "⚡", "desc": "Speed & efficiency"},
        {"name": "Test Engineer", "icon": "🧪", "desc": "Testing & coverage"},
        {"name": "Code Reviewer", "icon": "🔍", "desc": "Quality review"},
        {"name": "Documentation Generator", "icon": "📚", "desc": "Comprehensive docs"},
        {"name": "Team Architect", "icon": "🏗️", "desc": "System design"},
        {"name": "Accessibility Auditor", "icon": "♿", "desc": "WCAG compliance"},
        {"name": "Refactoring Specialist", "icon": "🔧", "desc": "Code modernization"},
        {"name": "Migration Specialist", "icon": "🚀", "desc": "Framework upgrades"},
        {"name": "DevOps Automation", "icon": "⚙️", "desc": "CI/CD & Infrastructure"},
        {"name": "Database Optimizer", "icon": "💾", "desc": "Query optimization"}
    ]

    text = "*Available Agents (12 Total)*\n\n"
    for agent in agents:
        text += f"{agent['icon']} *{agent['name']}*\n   _{agent['desc']}_\n\n"

    return jsonify({
        "response_type": "ephemeral",
        "text": text
    })


@app.route('/slack/events', methods=['POST'])
def handle_slack_events():
    """Handle Slack events (mentions, reactions, etc.)"""
    data = request.json

    # Handle challenge verification
    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']})

    event = data.get('event', {})
    event_type = event.get('type')

    if event_type == 'app_mention':
        handle_mention(event)

    return jsonify({'ok': True})


def handle_mention(event: Dict):
    """Handle bot mentions"""
    text = event.get('text', '').replace(f"<@{event.get('bot_id', '')}>", '').strip()
    channel = event.get('channel')

    # Parse and respond
    # In production, would post back to Slack channel
    print(f"Bot mentioned in {channel}: {text}")


def parse_command(text: str) -> tuple:
    """Parse command text into action and description"""
    parts = text.split(maxsplit=1)
    action = parts[0].lower() if parts else "analyze"
    description = parts[1] if len(parts) > 1 else text
    return action, description


def format_slack_response(result, description: str) -> Dict:
    """Format recommendation as Slack message"""
    agents_text = "\n".join([
        f"  {rec.priority}. *{rec.agent_name}* ({rec.intensity.value})\n"
        f"     _{rec.reason}_"
        for rec in result.recommended_chain
    ])

    return {
        "response_type": "in_channel",
        "text": f"🤖 *CoT Framework Analysis*",
        "attachments": [
            {
                "color": "good",
                "fields": [
                    {"title": "Task", "value": description, "short": False},
                    {"title": "Complexity", "value": result.complexity.value.upper(), "short": True},
                    {"title": "Est. Time", "value": result.estimated_total_time, "short": True},
                    {"title": "Success Rate", "value": f"{result.success_probability*100:.1f}%", "short": True},
                    {"title": "Similar Tasks", "value": str(result.similar_past_tasks), "short": True}
                ]
            },
            {
                "color": "#667eea",
                "title": f"Recommended Workflow ({len(result.recommended_chain)} agents)",
                "text": agents_text,
                "footer": "Unified CoT Framework v3.0",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
            }
        ]
    }


def get_metrics_summary(period: str) -> Dict:
    """Get metrics summary for period"""
    # Mock data - in production, fetch from database
    metrics_by_period = {
        "daily": {
            "tasks": 47,
            "success_rate": 97.3,
            "quality": 9.2,
            "time_saved": 5.2
        },
        "weekly": {
            "tasks": 312,
            "success_rate": 96.8,
            "quality": 9.1,
            "time_saved": 43.5
        },
        "monthly": {
            "tasks": 1247,
            "success_rate": 97.1,
            "quality": 9.3,
            "time_saved": 156.0
        },
        "team": {
            "tasks": 1247,
            "success_rate": 97.1,
            "quality": 9.3,
            "time_saved": 156.0
        }
    }

    return metrics_by_period.get(period, metrics_by_period["daily"])


if __name__ == '__main__':
    print("🚀 Unified CoT Framework - Slack Bot")
    print(f"   Orchestrator: {'Online' if recommender else 'Offline'}")
    print(f"   Port: 3000")
    print()
    app.run(host='0.0.0.0', port=3000, debug=True)
