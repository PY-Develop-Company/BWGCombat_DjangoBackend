
# Requirements
- Install Docker via link (https://docs.docker.com/desktop/install/windows-install/);
- Install MongoDB UI extencion (https://www.mongodb.com/try/download/compass);
![image](https://github.com/JustKovalchuk/JustKovalchuk/assets/86592772/db2aaceb-a42e-47ab-99b9-9ed231b1087a)

# How to run the project
Firstly create ```.env``` file in project root folder with following parameters:
```
MONGO_DB_HOST=mongo
MONGO_DB_PORT=27017
MONGO_DB_NAME=bwg_combat_mongo_db
MONGO_DB_USERNAME=root
MONGO_DB_PASSWORD=root
```
Than run folowing commands to configure Docker and install all requirements:
```
docker build .
docker-compose build
```

To **start the app** use command:
```
docker-compose up
```
To **stop the app** press ```CTRL-C```
To delete all containers use command:
```
docker-compose down
```

Usefull commands:
- to **execute command** with new app creation or applying mighration use sintax (and **put your command into ""**):
```
docker-compose run --rm app sh -c ""
```