@echo off

:wait_for_docker
cd C:\code\InForm
docker-compose ps
set /A docker_running = %ERRORLEVEL%
set /A docker_off = "-1"

If %docker_running% == %docker_off% (
    echo "Docker is not running yet. Sleeping for 2 seconds and then checking again"
    SLEEP 2
    GOTO wait_for_docker
)

echo "RESTARTING DOCKER"
cd C:\code\InForm
SLEEP 30
docker-compose down
docker-compose up -d
PAUSE