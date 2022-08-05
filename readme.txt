#Deploy fastapi
- https://fastapi.tiangolo.com/deployment/

apt install python3-pip
pip3 install --no-cache-dir -r requirements.txt
pip3 install "uvicorn[standard]"

uvicorn main:app --reload
pm2 start 'uvicorn app.main:app --host 0.0.0.0 --port 8000' --name=startapi


#Docker
apt install docker.io

1 install mysql + phpmyadmin
docker run -d -p 3306:3306 --name mariadb \ 
-e ALLOW_EMPTY_PASSWORD=no \ 
-e MARIADB_ROOT_PASSWORD=Pass1234xxx \ 
-e MARIADB_USER=admin_game \ 
-e MARIADB_PASSWORD=Pass1234xxx \ 
-e MARIADB_DATABASE=admin_game \ bitnami/mariadb:latest

2 Run 
docker run --name ufaphpmyadmin -d --link mariadb:db -p 9981:80 phpmyadmin

3 Auto start
docker update --restart always mariadb
docker update --restart always phpmyadmin
