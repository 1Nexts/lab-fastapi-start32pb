# lab_fastapi

## Project setup
```
FastAPI
apt install python3-pip
pip3 install --no-cache-dir -r requirements.txt
pip3 install "uvicorn[standard]"

Docker
apt install docker.io

docker run -d -p 3306:3306 --name mariadb \
  -e ALLOW_EMPTY_PASSWORD=no \
  -e MARIADB_ROOT_PASSWORD=aNrwlOvWxG \
  -e MARIADB_USER=admin_game \
  -e MARIADB_PASSWORD=aNrwlOvWxG \
  -e MARIADB_DATABASE=admin_game \
  bitnami/mariadb:latest

PM2
npm install pm2 -g

```

### Compiles and hot-reloads for development
```
#run pm2
pm2 start 'uvicorn app.main:app --host 0.0.0.0 --port 8000' --name=startapi
pm2 save
pm2 resurrect *load save
pm2 startup *auto start

#run docker image
docker run --name ufaphpmyadmin -d --link mariadb:db -p 9981:80 phpmyadmin

Auto start container
docker update --restart always mariadb
docker update --restart always phpmyadmin
```
