# 1. 베이스 이미지 선택
FROM python:3.9-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY service_inputgenerator1.py .
COPY oom_inputgenerator2.py .
COPY mce_inputgenerator3.py .
COPY disk_inputgenerator4.py .
COPY auth_inputgenerator5.py .

# 5. 컨테이너 실행 시 사용할 포트를 노출
EXPOSE 8080

# 6. 애플리케이션 실행
CMD ["python", "service_inputgenerator1.py"]
CMD ["python", "oom_inputgenerator2.py"]
CMD ["python", "mce_inputgenerator3.py"]
CMD ["python", "disk_inputgenerator4.py"]
CMD ["python", "auth_inputgenerator5.py"]
