import os
import socket
import datetime
import platform
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)

# Track server start time
START_TIME = datetime.datetime.now(datetime.timezone.utc)
REQUEST_COUNT = 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure SRE Enterprise Web App</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090d16;
            --card-bg: rgba(23, 32, 54, 0.7);
            --card-border: rgba(99, 102, 241, 0.25);
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.4);
            --accent: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.12) 0px, transparent 50%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2.5rem 1.5rem;
        }

        .container {
            max-width: 900px;
            width: 100%;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .badge-slot {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid var(--success);
            color: #34d399;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        }

        .badge-slot.staging {
            background: rgba(245, 158, 11, 0.15);
            border-color: var(--warning);
            color: #fbbf24;
            box-shadow: 0 0 20px rgba(245, 158, 11, 0.2);
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2rem;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(12px);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .card:hover {
            transform: translateY(-2px);
            border-color: var(--primary);
        }

        .card-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .card-value {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            word-break: break-all;
        }

        .card-value.highlight {
            color: var(--accent);
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 10px var(--success);
            margin-right: 6px;
        }

        .footer-note {
            text-align: center;
            margin-top: 2rem;
            color: var(--text-muted);
            font-size: 0.9rem;
        }

        .endpoints {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }

        .endpoints a {
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s;
        }

        .endpoints a:hover {
            color: #ffffff;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-slot {{ 'staging' if 'staging' in slot_name.lower() else '' }}">
                <span class="status-dot"></span>
                ACTIVE SLOT: {{ slot_name }}
            </div>
            <h1>Azure Enterprise SRE WebApp</h1>
            <p class="subtitle">Cloud DevOps CI/CD Deployment Verification & Slot Swap Engine</p>
        </header>

        <div class="grid">
            <div class="card">
                <div class="card-label">Cloud Platform</div>
                <div class="card-value highlight">Microsoft Azure (Linux PaaS)</div>
            </div>
            <div class="card">
                <div class="card-label">App Service Name</div>
                <div class="card-value">{{ app_name }}</div>
            </div>
            <div class="card">
                <div class="card-label">Host Container Name</div>
                <div class="card-value">{{ hostname }}</div>
            </div>
            <div class="card">
                <div class="card-label">Runtime Engine</div>
                <div class="card-value">{{ python_version }}</div>
            </div>
            <div class="card">
                <div class="card-label">Release Version</div>
                <div class="card-value highlight">v1.0.0-PROD</div>
            </div>
            <div class="card">
                <div class="card-label">Uptime Since Startup</div>
                <div class="card-value">{{ uptime }}</div>
            </div>
            <div class="card" style="grid-column: 1 / -1; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.07);">
                <div class="card-label" style="color: #34d399; display: flex; align-items: center; gap: 0.5rem;">
                    <span>🔐</span> Azure Key Vault Injected Secret
                </div>
                <div class="card-value" style="color: #6ee7b7; font-size: 1.1rem; word-break: break-all;">
                    {{ kv_secret }}
                </div>
                <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">
                    Status: <span style="color: {{ kv_status_color }}; font-weight: 600;">{{ kv_status }}</span>
                </div>
            </div>
        </div>

        <div class="endpoints">
            <div>Health Probe: <a href="/healthz">/healthz (HTTP 200)</a></div>
            <div>Metadata API: <a href="/api/info">/api/info (JSON)</a></div>
        </div>

        <div class="footer-note">
            Built for Senior Cloud SRE & DevOps Master Verification • Continuous Deployment Active
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    
    app_name = os.getenv("WEBSITE_SITE_NAME", "azure-sre-webapp-local")
    slot_name = os.getenv("SLOT_NAME", os.getenv("APP_ENV", "Production Slot"))
    hostname = socket.gethostname()
    python_version = f"Python {platform.python_version()}"
    
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - START_TIME
    uptime = f"{int(delta.total_seconds())}s"
    
    # Check for Key Vault injected secret (supports 'test', 'DATABASE_URL', 'TEST_SECRET', 'MONGO_URI')
    raw_secret = os.getenv("test") or os.getenv("DATABASE_URL") or os.getenv("TEST_SECRET") or os.getenv("MONGO_URI") or os.getenv("MY_DB_SECRET")
    
    if not raw_secret:
        kv_secret = "❌ No Secret Environment Variable Found"
        kv_status = "App Setting ('test' or 'DATABASE_URL') not set in App Service"
        kv_status_color = "#ef4444"
    elif raw_secret.startswith("@Microsoft.KeyVault"):
        kv_secret = raw_secret
        kv_status = "⚠️ Key Vault Reference syntax present but unresolved by App Service (verify Managed Identity & RBAC)"
        kv_status_color = "#f59e0b"
    else:
        kv_secret = raw_secret
        kv_status = "✅ Resolved! Plain-text successfully injected by Azure Key Vault Reference"
        kv_status_color = "#10b981"

    return render_template_string(
        HTML_TEMPLATE,
        app_name=app_name,
        slot_name=slot_name,
        hostname=hostname,
        python_version=python_version,
        uptime=uptime,
        kv_secret=kv_secret,
        kv_status=kv_status,
        kv_status_color=kv_status_color
    )

@app.route('/healthz')
def health_check():
    """Health check endpoint for Azure App Service & Application Gateway probes"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": "1.0.0",
        "service": "azure-sre-webapp"
    }), 200

@app.route('/api/info')
def api_info():
    """System information endpoint"""
    raw_secret = os.getenv("test") or os.getenv("DATABASE_URL") or os.getenv("TEST_SECRET") or os.getenv("MONGO_URI")
    return jsonify({
        "app_name": os.getenv("WEBSITE_SITE_NAME", "azure-sre-webapp-local"),
        "slot_name": os.getenv("SLOT_NAME", os.getenv("APP_ENV", "Production Slot")),
        "hostname": socket.gethostname(),
        "instance_id": os.getenv("WEBSITE_INSTANCE_ID", "local-dev-instance"),
        "python_version": platform.python_version(),
        "requests_handled": REQUEST_COUNT,
        "key_vault_secret_injected": raw_secret is not None and not raw_secret.startswith("@Microsoft.KeyVault"),
        "key_vault_secret_value": raw_secret
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
