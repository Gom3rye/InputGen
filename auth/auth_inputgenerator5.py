# auth_inputgen_metrics.py

import time
import random
import sys
import socket
from datetime import datetime, timezone, timedelta
import threading
from prometheus_client import Counter, generate_latest
from fastapi import FastAPI, Response
import uvicorn

# ✅ Prometheus 메트릭 정의
auth_attempts_total = Counter(
    'auth_attempts_total',
    'Total SSH authentication attempts',
    ['result']
)

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


def generate_auth_log():
    users = ["root", "admin", "kyla", "dev", "attacker", "guest"]
    ips = ["104.28.231.109", "10.0.1.100", "211.34.56.78", "192.168.1.1"]
    hostname = socket.gethostname()
    pid = random.randint(10000, 20000)
    ts = datetime.now(timezone(timedelta(hours=9)))

    if random.random() > 0.3:
        user = random.choice(users[:-2])
        message = f"Accepted password for {user} from {random.choice(ips)} port {random.randint(40000, 60000)} ssh2"
        result = "success"
    else:
        user = random.choice(users)
        message = f"Failed password for invalid user {user} from {random.choice(ips)} port {random.randint(40000, 60000)} ssh2"
        result = "failed"

    # 📊 메트릭 업데이트
    auth_attempts_total.labels(result=result).inc()

    return f"{ts} {hostname} sshd[{pid}]: {message}"


def log_loop():
    while True:
        time.sleep(random.uniform(1.0, 10.0))
        log_message = generate_auth_log()
        print(log_message)
        sys.stdout.flush()


if __name__ == "__main__":
    threading.Thread(target=log_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8080)
