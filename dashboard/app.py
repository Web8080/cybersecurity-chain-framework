#!/usr/bin/env python3
"""
Real-Time Target Status Dashboard
Author: Victor Ibhafidon

WHAT IT DOES:
- Web-based dashboard showing all target statuses
- Real-time status updates via WebSocket
- Start/stop targets from UI
- Display running chains per target
- Target health monitoring

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses target_manager.py for target management
- Integrates with chain_analyzer.py to show chains per target
- Provides web interface for framework operations
- Real-time updates for active monitoring

USAGE:
    python dashboard/app.py
    Then visit http://localhost:5000
"""

import sys
import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from targets.target_manager import TargetManager, TargetStatus
from chains.chain_analyzer import ChainAnalyzer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'attack-chain-analyzer-dashboard'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize managers
target_manager = TargetManager()
chain_analyzer = ChainAnalyzer()

# Load existing chains
def load_chains():
    """Load chains from JSON files"""
    chains_dir = os.path.join(os.path.dirname(__file__), '..', 'chains', 'chain_templates', 'exports')
    if os.path.exists(chains_dir):
        import json
        for filename in os.listdir(chains_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(chains_dir, filename), 'r') as f:
                        chain_data = json.load(f)
                        chain = chain_analyzer.import_chain(os.path.join(chains_dir, filename))
                except:
                    pass

load_chains()

# Background thread for status updates
def background_status_updates():
    """Send status updates every 5 seconds"""
    while True:
        time.sleep(5)
        statuses = target_manager.check_all_status()
        status_data = {}
        for name, target in target_manager.targets.items():
            status = statuses.get(name, TargetStatus.UNKNOWN)
            status_data[name] = {
                'name': target.name,
                'status': status.value,
                'url': target.url,
                'type': target.target_type,
                'description': target.description
            }
        socketio.emit('status_update', status_data)

# Start background thread
status_thread = threading.Thread(target=background_status_updates, daemon=True)
status_thread.start()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/targets', methods=['GET'])
def get_targets():
    """Get all targets with their status"""
    statuses = target_manager.check_all_status()
    targets_data = []
    
    for name, target in target_manager.targets.items():
        status = statuses.get(name, TargetStatus.UNKNOWN)
        targets_data.append({
            'id': name,
            'name': target.name,
            'type': target.target_type,
            'status': status.value,
            'url': target.url,
            'port': target.port,
            'description': target.description
        })
    
    return jsonify(targets_data)

@app.route('/api/targets/<target_id>/start', methods=['POST'])
def start_target(target_id):
    """Start a target"""
    success = target_manager.start_target(target_id)
    if success:
        return jsonify({'success': True, 'message': f'Target {target_id} started'})
    else:
        return jsonify({'success': False, 'message': f'Failed to start {target_id}'}), 500

@app.route('/api/targets/<target_id>/stop', methods=['POST'])
def stop_target(target_id):
    """Stop a target"""
    success = target_manager.stop_target(target_id)
    if success:
        return jsonify({'success': True, 'message': f'Target {target_id} stopped'})
    else:
        return jsonify({'success': False, 'message': f'Failed to stop {target_id}'}), 500

@app.route('/api/chains', methods=['GET'])
def get_chains():
    """Get all chains"""
    chains_data = []
    for chain in chain_analyzer.chains:
        chains_data.append({
            'title': chain.title,
            'description': chain.description,
            'impact': chain.impact.value,
            'steps': len(chain.steps),
            'tags': list(chain.tags)
        })
    return jsonify(chains_data)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to dashboard'})

@socketio.on('request_status')
def handle_status_request():
    """Handle status request"""
    statuses = target_manager.check_all_status()
    status_data = {}
    for name, target in target_manager.targets.items():
        status = statuses.get(name, TargetStatus.UNKNOWN)
        status_data[name] = {
            'name': target.name,
            'status': status.value,
            'url': target.url,
            'type': target.target_type
        }
    emit('status_update', status_data)

if __name__ == '__main__':
    print("=" * 80)
    print("REAL-TIME TARGET STATUS DASHBOARD")
    print("=" * 80)
    print("\nStarting dashboard server...")
    print("Access the dashboard at: http://localhost:5001")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    socketio.run(app, host='0.0.0.0', port=5001, debug=False, allow_unsafe_werkzeug=True)
