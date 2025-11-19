#!/usr/bin/env python3
"""
Unified CoT Framework v3.0 - Webhook Server
Receive and send notifications for task events
"""

import json
import hmac
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration (set via environment or config file)
WEBHOOK_SECRET = "your-webhook-secret-here"
REGISTERED_WEBHOOKS: List[Dict] = []


class WebhookEvent:
    """Webhook event types"""
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    AGENT_STARTED = "agent.started"
    AGENT_COMPLETED = "agent.completed"
    PATTERN_LEARNED = "pattern.learned"
    QUALITY_THRESHOLD = "quality.threshold"


def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify webhook signature"""
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


def send_webhook(url: str, event_type: str, data: Dict):
    """Send webhook notification"""
    payload = {
        "event": event_type,
        "timestamp": datetime.now().isoformat(),
        "data": data
    }

    # Sign payload
    payload_bytes = json.dumps(payload).encode()
    signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()

    try:
        response = requests.post(
            url,
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-CoT-Signature": signature,
                "X-CoT-Event": event_type
            },
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Webhook delivery failed: {e}")
        return False


@app.route('/webhooks/register', methods=['POST'])
def register_webhook():
    """Register a new webhook endpoint"""
    data = request.json
    url = data.get('url')
    events = data.get('events', [])
    name = data.get('name', 'Unnamed Webhook')

    if not url:
        return jsonify({"error": "URL required"}), 400

    webhook = {
        "id": len(REGISTERED_WEBHOOKS) + 1,
        "name": name,
        "url": url,
        "events": events,
        "created_at": datetime.now().isoformat(),
        "active": True
    }

    REGISTERED_WEBHOOKS.append(webhook)

    return jsonify({
        "success": True,
        "webhook": webhook
    }), 201


@app.route('/webhooks/list', methods=['GET'])
def list_webhooks():
    """List registered webhooks"""
    return jsonify({
        "webhooks": REGISTERED_WEBHOOKS,
        "total": len(REGISTERED_WEBHOOKS)
    })


@app.route('/webhooks/delete/<int:webhook_id>', methods=['DELETE'])
def delete_webhook(webhook_id: int):
    """Delete a webhook"""
    global REGISTERED_WEBHOOKS
    REGISTERED_WEBHOOKS = [w for w in REGISTERED_WEBHOOKS if w['id'] != webhook_id]

    return jsonify({"success": True})


@app.route('/webhooks/test', methods=['POST'])
def test_webhook():
    """Test webhook delivery"""
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL required"}), 400

    # Send test event
    success = send_webhook(url, "test.ping", {
        "message": "This is a test webhook from Unified CoT Framework v3.0"
    })

    return jsonify({
        "success": success,
        "message": "Test webhook sent" if success else "Webhook delivery failed"
    })


@app.route('/webhooks/receive', methods=['POST'])
def receive_webhook():
    """Receive webhook from external service"""
    signature = request.headers.get('X-CoT-Signature', '')
    payload = request.get_data()

    if not verify_signature(payload, signature):
        return jsonify({"error": "Invalid signature"}), 401

    data = request.json
    event_type = request.headers.get('X-CoT-Event')

    # Process event
    print(f"Received webhook: {event_type}")
    print(f"Data: {json.dumps(data, indent=2)}")

    return jsonify({"success": True})


def notify_task_completed(task_id: str, agent: str, result: Dict):
    """Notify all webhooks of task completion"""
    event_data = {
        "task_id": task_id,
        "agent": agent,
        "status": result.get("status"),
        "quality_score": result.get("quality_score"),
        "duration": result.get("duration"),
        "artifacts": result.get("artifacts", [])
    }

    for webhook in REGISTERED_WEBHOOKS:
        if not webhook['active']:
            continue

        if WebhookEvent.TASK_COMPLETED in webhook['events']:
            send_webhook(webhook['url'], WebhookEvent.TASK_COMPLETED, event_data)


def notify_pattern_learned(pattern: Dict):
    """Notify when new pattern is learned"""
    event_data = {
        "pattern_id": pattern.get("id"),
        "name": pattern.get("name"),
        "category": pattern.get("category"),
        "times_used": pattern.get("times_used"),
        "success_rate": pattern.get("success_rate")
    }

    for webhook in REGISTERED_WEBHOOKS:
        if not webhook['active']:
            continue

        if WebhookEvent.PATTERN_LEARNED in webhook['events']:
            send_webhook(webhook['url'], WebhookEvent.PATTERN_LEARNED, event_data)


if __name__ == '__main__':
    print("🔗 Unified CoT Framework - Webhook Server")
    print(f"   Port: 3001")
    print()
    print("Available endpoints:")
    print("  POST   /webhooks/register   - Register new webhook")
    print("  GET    /webhooks/list       - List webhooks")
    print("  DELETE /webhooks/delete/:id - Delete webhook")
    print("  POST   /webhooks/test       - Test webhook")
    print("  POST   /webhooks/receive    - Receive external webhook")
    print()

    app.run(host='0.0.0.0', port=3001, debug=True)
