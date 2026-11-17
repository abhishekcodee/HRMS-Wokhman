"""
Environment-Driven Database Configuration Generator for Frappe HRMS.

Reads standard database environment variables and dynamically injects them into
Frappe's site_config.json, ensuring database credentials and connection hosts
are controlled 100% via your environment (Docker/Kubernetes/Systemd).
"""

import os
import json
import sys

def configure_site_database(site_name: str, site_dir: str):
    config_path = os.path.join(site_dir, site_name, "site_config.json")
    
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            config = {}

    # Override database connection parameters from environment variables
    db_host = os.environ.get("DB_HOST") or os.environ.get("MYSQL_HOST") or os.environ.get("POSTGRES_HOST")
    db_port = os.environ.get("DB_PORT") or os.environ.get("MYSQL_PORT") or os.environ.get("POSTGRES_PORT")
    db_name = os.environ.get("DB_NAME") or os.environ.get("MYSQL_DATABASE") or os.environ.get("POSTGRES_DB")
    db_password = os.environ.get("DB_PASSWORD") or os.environ.get("MYSQL_PASSWORD") or os.environ.get("POSTGRES_PASSWORD")
    db_user = os.environ.get("DB_USER") or os.environ.get("MYSQL_USER") or os.environ.get("POSTGRES_USER")
    db_type = os.environ.get("DB_TYPE", "mariadb").lower()

    if db_host:
        config["db_host"] = db_host
    if db_port:
        config["db_port"] = int(db_port)
    if db_name:
        config["db_name"] = db_name
    if db_password:
        config["db_password"] = db_password
    if db_type:
        config["db_type"] = db_type

    # Redis environment configuration
    redis_cache = os.environ.get("REDIS_CACHE")
    redis_queue = os.environ.get("REDIS_QUEUE")
    redis_socketio = os.environ.get("REDIS_SOCKETIO")

    if redis_cache:
        config["redis_cache"] = redis_cache
    if redis_queue:
        config["redis_queue"] = redis_queue
    if redis_socketio:
        config["redis_socketio"] = redis_socketio

    # Sovereign privacy enforcement
    config["enable_telemetry"] = 0
    config["telemetry"] = 0
    config["push_relay_server_url"] = ""

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"[SUCCESS] Configured database for site '{site_name}' via environment variables at: {config_path}")
    print(f"          Target Host: {config.get('db_host', 'localhost')}:{config.get('db_port', 3306)} | Database: {config.get('db_name')}")

if __name__ == "__main__":
    target_site = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SITE_NAME", "hrms.local")
    bench_sites_dir = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("SITES_DIR", "/home/frappe/frappe-bench/sites")
    configure_site_database(target_site, bench_sites_dir)
