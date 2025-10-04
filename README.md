jenkins login
admin
admin123

ngrok pub: 
ngrok http 8080

jenkins run:
docker run --name jenkins4 -u root -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -it jenkins/jenkins:lts

setup: jenkins container:

docker exec -it jenkins5 bash

# Update package list
apt-get update

# Install Docker CLI (already might be there if using -v /var/run/docker.sock)
apt-get install -y docker.io

# Install Docker Compose v2 (plugin)
apt-get install -y curl
curl -SL https://github.com/docker/compose/releases/download/v2.30.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Verify
docker-compose --version
