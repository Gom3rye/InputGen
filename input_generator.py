import time
import random
import json
import sys
import threading
from flask import Flask, Response
from datetime import datetime

# --- 프로메테우스를 위한 메트릭 값 저장 변수 ---
simulated_cpu_usage = 0.0
simulated_memory_usage = 0.0
failed_logins_total = 0
http_requests_total = 0

# --- Flask 웹 애플리케이션 생성 (Prometheus 메트릭 노출용) ---
app = Flask(__name__)

@app.route('/metrics')
def metrics():
    """프로메테우스가 수집할 메트릭을 형식에 맞게 노출하는 엔드포인트"""
    metric_data = []
    metric_data.append('# HELP simulated_cpu_usage_percent The simulated CPU usage of the server.')
    metric_data.append('# TYPE simulated_cpu_usage_percent gauge')
    metric_data.append(f'simulated_cpu_usage_percent {simulated_cpu_usage}')
    
    metric_data.append('\n# HELP simulated_memory_usage_percent The simulated memory usage of the server.')
    metric_data.append('# TYPE simulated_memory_usage_percent gauge')
    metric_data.append(f'simulated_memory_usage_percent {simulated_memory_usage}')

    metric_data.append('\n# HELP failed_logins_total Total number of failed login attempts.')
    metric_data.append('# TYPE failed_logins_total counter')
    metric_data.append(f'failed_logins_total {failed_logins_total}')

    metric_data.append('\n# HELP http_requests_total Total number of http requests.')
    metric_data.append('# TYPE http_requests_total counter')
    metric_data.append(f'http_requests_total {http_requests_total}')
    
    return Response("\n".join(metric_data), mimetype='text/plain')

def log_generator():
    """백그라운드에서 계속해서 JSON 형식의 로그를 생성하는 함수"""
    global simulated_cpu_usage, simulated_memory_usage, failed_logins_total, http_requests_total
    
    users = ["user-a", "user-b", "admin", "guest"]
    ips = ["192.168.1.10", "10.0.0.5", "172.16.0.8", "203.0.113.25"]
    
    while True:
    	# 0.1초에서 1.5초 사이의 랜덤한 간격으로 로그 생성
        time.sleep(random.uniform(0.1, 1.5))
        
        log_type = random.choices(
            population=["login_success", "login_fail", "request", "system_metric", "error"],
            weights=[0.3, 0.1, 0.4, 0.15, 0.05],
            k=1
        )[0]

        # 기본 로그 구조
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "log_type": log_type
        }

        # 시나리오에 따라 로그 필드 추가 및 메트릭 값 업데이트
        if log_type == "login_success":
            log_entry.update({"level": "info", "event": "success", "user": random.choice(users), "ip": random.choice(ips)})
            
        elif log_type == "login_fail":
            log_entry.update({"level": "warning", "event": "failed", "user": random.choice(users), "ip": random.choice(ips), "message": "Failed login attempt"})
            failed_logins_total += 1

        elif log_type == "request":
            status = random.choices(population=[200, 404, 500], weights=[0.9, 0.07, 0.03], k=1)[0]
            log_entry.update({"level": "info", "ip": random.choice(ips), "http_status": status, "path": "/api/data"})
            http_requests_total += 1
            
        elif log_type == "system_metric":
            simulated_cpu_usage = round(random.uniform(10.0, 99.9), 2)
            simulated_memory_usage = round(random.uniform(20.0, 95.0), 2)
            level = "info" if simulated_cpu_usage <= 90.0 else "warning"
            log_entry.update({"level": level, "metrics": {"cpu_usage": simulated_cpu_usage, "memory_usage": simulated_memory_usage}})

        elif log_type == "error":
            log_entry.update({"level": "error", "message": "Database connection timeout"})

        # 최종 JSON 로그를 한 줄로 출력
        # sys.stdout.flush()는 버퍼링 없이 즉시 출력되도록 보장
        print(json.dumps(log_entry))
        sys.stdout.flush()

if __name__ == '__main__':
	# 로그 생성 스레드를 데몬으로 설정하여 메인 스레드 종료 시 함께 종료되도록 함
    log_thread = threading.Thread(target=log_generator, daemon=True)
    log_thread.start()
    # Flask 웹 서버 실행 (메트릭 노출)
    # host='0.0.0.0' 은 컨테이너 외부에서 접근 가능하도록 설정
    app.run(host='0.0.0.0', port=8080)
