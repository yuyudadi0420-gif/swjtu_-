import os
import redis
import requests
from flask import Flask, jsonify

app = Flask(__name__)

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None) or None

def get_redis():
    return redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )

@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok"})

@app.route("/api/redis/set/<key>/<value>")
def redis_set(key, value):
    r = get_redis()
    r.set(key, value)
    return jsonify({"result": "ok", "key": key, "value": value})

@app.route("/api/redis/get/<key>")
def redis_get(key):
    r = get_redis()
    value = r.get(key)
    return jsonify({"key": key, "value": value})

@app.route("/api/info")
def info():
    # requests 包示例用途：获取本机公网 IP
    try:
        ip = requests.get("https://api.ipify.org", timeout=3).text
    except Exception:
        ip = "unavailable"
    return jsonify({
        "redis_host": REDIS_HOST,
        "redis_port": REDIS_PORT,
        "public_ip": ip,
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
