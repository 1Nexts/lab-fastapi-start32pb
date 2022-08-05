#Deploy fastapi
- https://fastapi.tiangolo.com/deployment/

apt install python3-pip
pip3 install --no-cache-dir -r requirements.txt
pip3 install "uvicorn[standard]"

uvicorn app.main:app --reload


#pm2
pm2 start 'uvicorn app.main:app --host 0.0.0.0 --port 8000' --name=startapi
pm2 save
pm2 resurrect *load save
pm2 startup *auto start


#Docker

1 install docker
apt install docker.io

2 install mariadb phpmyadmin
docker run -d -p 3306:3306 --name mariadb \
  -e ALLOW_EMPTY_PASSWORD=no \
  -e MARIADB_ROOT_PASSWORD=aNrwlOvWxG \
  -e MARIADB_USER=admin_game \
  -e MARIADB_PASSWORD=aNrwlOvWxG \
  -e MARIADB_DATABASE=admin_game \
  bitnami/mariadb:latest

3 Run 
docker run --name ufaphpmyadmin -d --link mariadb:db -p 9981:80 phpmyadmin

4 Auto start
docker update --restart always mariadb
docker update --restart always phpmyadmin
