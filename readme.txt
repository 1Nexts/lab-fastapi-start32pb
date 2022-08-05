Deploy
- https://fastapi.tiangolo.com/deployment/


- apt install python3-pip
- pip3 install --no-cache-dir -r requirements.txt
- pip3 install "uvicorn[standard]"

- uvicorn main:app --reload
- pm2 start 'uvicorn app.main:app --host 0.0.0.0 --port 8000' --name=startapi