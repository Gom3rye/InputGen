import time
import random
import sys
from datetime import datetime

# 커널 메시지에 사용될 가상 타임스탬프
kernel_timestamp = random.uniform(30000, 40000)

def generate_nginx_log():
    """Nginx의 access.log와 유사한 포맷의 로그를 생성합니다."""
    ips = ["142.250.204.110", "157.240.22.35", "8.8.8.8", "1.1.1.1"]
    methods = ["GET", "POST", "PUT"]
    paths = ["/api/v1/users/123", "/static/img/logo.png", "/login", "/admin"]
    statuses = [200, 201, 404, 401, 500]
    
    ip = random.choice(ips)
    user = "user" + str(random.randint(1, 5)) if random.random() > 0.5 else "-"
    ts = datetime.now().strftime('%d/%b/%Y:%H:%M:%S %z')
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choices(population=statuses, weights=[0.7, 0.1, 0.1, 0.05, 0.05], k=1)[0]
    bytes_sent = random.randint(100, 50000)
    
    return f'{ip} - {user} [{ts}] "{method} {path} HTTP/1.1" {status} {bytes_sent}'

def generate_auth_log():
    """auth.log (sshd)와 유사한 포맷의 로그를 생성합니다."""
    users = ["root", "admin", "kyla", "dev", "attacker", "jiwoo", "leeejjju"]
    ips = ["104.28.231.109", "10.0.1.100", "211.34.56.78"]
    hostname = "prod-bastion-01"
    pid = random.randint(10000, 20000)
    ts = datetime.now().strftime('%b %d %H:%M:%S')
    
    if random.random() > 0.3:
        return f"{ts} {hostname} sshd[{pid}]: Accepted password for {random.choice(users)} from {random.choice(ips)} port 49152 ssh2"
    else:
        return f"{ts} {hostname} sshd[{pid}]: Failed password for invalid user {random.choice(users)} from {random.choice(ips)} port 54321 ssh2"

def generate_kernel_error_log():
    """dmesg와 유사한 멀티라인 하드웨어 에러 로그를 생성합니다."""
    global kernel_timestamp
    kernel_timestamp += random.uniform(10, 1000)
    ts = kernel_timestamp
    
    pid = random.randint(10000, 20000)
    return (
        f"[{ts:.6f}] Out of memory: Killed process {pid} (java) total-vm:{random.randint(1000000,2000000)}kB, anon-rss:{random.randint(700000,900000)}kB\n"
        f"[{ts + 0.000007:.6f}] CPU: {random.randint(0,3)} PID: {pid} Comm: java Not tainted 5.15.0-107-generic #117-Ubuntu\n"
        f"[{ts + 0.000027:.6f}] oom_reaper: reaped process {pid} (java), now anon-rss:0"
    )

if __name__ == "__main__":
    while True:
        # 1초에서 3초 사이의 랜덤한 간격으로 로그 생성
        time.sleep(random.uniform(1.0, 3.0))
        
        log_function = random.choices(
            population=[generate_nginx_log, generate_auth_log, generate_kernel_error_log],
            weights=[0.6, 0.3, 0.1], # 일반 Nginx 로그가 더 자주 발생하도록 가중치 부여
            k=1
        )[0]
        
        log_message = log_function()
        
        # 최종 Plaintext 로그를 표준 출력으로 내보냄
        print(log_message)
        sys.stdout.flush()
