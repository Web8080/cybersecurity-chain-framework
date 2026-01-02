# Real-Time Target Status Dashboard

**Author:** Victor Ibhafidon

## Overview

Web-based dashboard for monitoring pentesting targets and attack chains in real-time.

## Features

- **Real-Time Status Updates**: WebSocket-based live updates every 5 seconds
- **Target Management**: Start/stop targets directly from the UI
- **Chain Monitoring**: View all attack chains with their details
- **Visual Status Indicators**: Color-coded status for quick identification
- **Responsive Design**: Works on desktop and mobile devices

## Usage

### Start the Dashboard

```bash
cd dashboard
python3 app.py
```

Then open your browser to: http://localhost:5000

### API Endpoints

- `GET /api/targets` - Get all targets with status
- `POST /api/targets/<id>/start` - Start a target
- `POST /api/targets/<id>/stop` - Stop a target
- `GET /api/chains` - Get all attack chains

### WebSocket Events

- `status_update` - Real-time target status updates
- `request_status` - Request current status from server

## Requirements

- Flask
- Flask-SocketIO
- Python 3.9+

## Architecture

- **Backend**: Flask with SocketIO for real-time updates
- **Frontend**: Vanilla JavaScript with Socket.IO client
- **Integration**: Uses `target_manager.py` and `chain_analyzer.py`
