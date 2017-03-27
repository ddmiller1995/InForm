# This is a compilation of a number of specific commands for our docker images that may be useful

```bash
# Build all of our images
docker-compose build

# Bring up all project containers in the background
docker-compose up -d

# See that status of all of the running containers on your docker host
docker-compose ps

# Bring down all running containers from this project
docker-compose down

# Collect static files
docker exec -it dg01 python manage.py collectstatic

# Attach to the nginx container's bash shell
docker exec -ti ng01 bash

# Attach to the gunicorn container's bash shell
docker exec -ti dg01 bash

# View the nginx container's logs
docker-compose logs nginx  

# View the gunicorn container's logs
docker-compose logs web  
```
