@echo off
echo ====================================================
echo  CheckerLeak Docker Hub Fleet Builder
echo ====================================================

REM Ensure Docker is logged in: docker login
set DOCKER_USER=checkerleak

echo Building %DOCKER_USER%/cli:latest ...
docker build -t %DOCKER_USER%/cli:latest -t %DOCKER_USER%/cli:2.0.0 ./checkerleak-cli

echo Building %DOCKER_USER%/phone-carrier-lookup:latest ...
docker build -t %DOCKER_USER%/phone-carrier-lookup:latest ./phone-carrier-lookup

echo Building %DOCKER_USER%/voip-detector:latest ...
docker build -t %DOCKER_USER%/voip-detector:latest ./voip-detector

echo.
echo ====================================================
echo  Build complete! Run 'docker push' to release:
echo  docker push %DOCKER_USER%/cli:latest
echo  docker push %DOCKER_USER%/phone-carrier-lookup:latest
echo  docker push %DOCKER_USER%/voip-detector:latest
echo ====================================================
