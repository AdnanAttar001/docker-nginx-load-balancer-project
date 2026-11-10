# 🚀 Two-Tier Docker Application with Nginx Load Balancer & Reverse Proxy

![Docker](https://img.shields.io/badge/Docker-Containerization-blue?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-green?logo=nginx)
![Python](https://img.shields.io/badge/Python-Flask-yellow?logo=python)
![Ubuntu](https://img.shields.io/badge/OS-Ubuntu-orange?logo=ubuntu)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📌 Project Overview

This project demonstrates the implementation of a real-world two-tier web application using Docker, Nginx, and Python Flask.

Nginx is configured as a reverse proxy and load balancer to distribute incoming HTTP requests across two independent Flask application containers.

The entire infrastructure is deployed using Docker CLI commands and custom Dockerfiles.

**No Docker Compose is used in this project.**

## 🎯 Project Objectives

- Containerize a Python Flask web application.
- Create custom Docker images using Dockerfiles.
- Deploy multiple backend application containers.
- Configure Nginx as a reverse proxy.
- Implement Round Robin load balancing.
- Configure Docker bridge networking.
- Implement application health checks.
- Simulate backend failures and test basic failover.
- Troubleshoot Docker containers and Nginx connectivity.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Ubuntu Linux | Host operating system |
| Docker | Containerization |
| Dockerfile | Image creation |
| Nginx | Reverse proxy and load balancer |
| Python Flask | Backend application |
| Gunicorn | Python application server |
| Docker Networking | Container communication |
| Git & GitHub | Version control |

## 🏗️ Architecture

```text
                  INTERNET
                      |
                      |
                  USER / CLIENT
                      |
                      |
                HOST PORT 8080
                      |
                      |
             NGINX LOAD BALANCER
                (PORT 80)
                      |
              REVERSE PROXY
                      |
               DOCKER NETWORK
                  app-network
                      |
              ROUND ROBIN ROUTING
                 /         \
                /           \
               /             \
         APP SERVER 1     APP SERVER 2
          Container        Container
          Flask App        Flask App
          Port 5000        Port 5000
               \             /
                \           /
                 \         /
               APPLICATION RESPONSE
                      |
                      |
                   CLIENT
```

### Architecture Explanation

1. User sends an HTTP request to the host server on port 8080.
2. Docker forwards the request to the Nginx container on port 80.
3. Nginx receives the request as a reverse proxy.
4. Nginx distributes requests across two Flask backend containers.
5. Flask processes the incoming requests.
6. The application response returns through Nginx to the client.

## 📂 Project Structure

```text
nginx-docker-project/
│
├── application/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
│
└── README.md
```

## ⚙️ Prerequisites

Before starting, make sure you have:

- Ubuntu Linux 22.04 or later.
- Docker installed.
- Basic Linux command knowledge.
- Git installed.
- Internet connectivity for downloading Docker images.

Verify Docker:

```bash
docker --version
```

## 🚀 Installation and Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/docker-nginx-load-balancer-project.git
```

Navigate into the project:

```bash
cd docker-nginx-load-balancer-project
```

### Step 2: Build the Flask Application Image

```bash
cd application

sudo docker build -t flask-app:v1 .
```

Verify the image:

```bash
sudo docker images
```

### Step 3: Create Docker Network

```bash
sudo docker network create app-network
```

Verify:

```bash
sudo docker network ls
```

### Step 4: Deploy Backend Application Containers

Deploy the first application:

```bash
sudo docker run -d \
--name app1 \
--network app-network \
-e APP_VERSION=v1 \
--restart unless-stopped \
flask-app:v1
```

Deploy the second application:

```bash
sudo docker run -d \
--name app2 \
--network app-network \
-e APP_VERSION=v2 \
--restart unless-stopped \
flask-app:v1
```

Verify running containers:

```bash
sudo docker ps
```

### Step 5: Build Nginx Docker Image

Navigate to the Nginx directory:

```bash
cd ../nginx
```

Build the image:

```bash
sudo docker build -t nginx-lb:v1 .
```

### Step 6: Deploy Nginx Load Balancer

```bash
sudo docker run -d \
--name nginx-lb \
--network app-network \
-p 8080:80 \
--restart unless-stopped \
nginx-lb:v1
```

Verify all containers:

```bash
sudo docker ps
```

## 🌐 Application Access

Open your browser:

```text
http://localhost:8080
```

For a remote Ubuntu server:

```text
http://YOUR_SERVER_IP:8080
```

## 🧪 Application Testing

### 1. Test Homepage

```bash
curl http://localhost:8080/
```

### 2. Test Health Endpoint

```bash
curl http://localhost:8080/health
```

### 3. Test API Endpoint

```bash
curl http://localhost:8080/api/info
```

### 4. Test Load Balancing

Execute multiple requests:

```bash
for i in {1..10}; do
  curl -s http://localhost:8080/api/info
  echo
done
```

Expected result:

Requests should be distributed between app1 and app2 using Nginx Round Robin load balancing.

### 5. Test Backend Failure

Stop the first backend:

```bash
sudo docker stop app1
```

Send multiple requests:

```bash
for i in {1..10}; do
  curl -s http://localhost:8080/api/info
  echo
done
```

Expected result:

Requests should continue to be served by app2.

Restart the first backend:

```bash
sudo docker start app1
```

Test again:

```bash
curl http://localhost:8080/api/info
```

Both backend containers should participate in load balancing again.

## 🔍 Docker Management Commands

| Command | Description |
|---|---|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker images` | List Docker images |
| `docker logs nginx-lb` | View Nginx logs |
| `docker logs app1` | View app1 logs |
| `docker logs app2` | View app2 logs |
| `docker network ls` | List Docker networks |
| `docker inspect app1` | Inspect container details |
| `docker exec -it app1 sh` | Enter application container |
| `docker restart nginx-lb` | Restart Nginx |

## 🛠️ Troubleshooting

### Issue 1: 502 Bad Gateway

Possible causes:
- Backend containers are stopped.
- Nginx cannot resolve backend container names.
- Application is not listening on port 5000.
- Containers are not connected to the same Docker network.

Check:

```bash
sudo docker ps -a
sudo docker logs app1
sudo docker logs app2
sudo docker logs nginx-lb
```

### Issue 2: Application Not Accessible

Check port mapping:

```bash
sudo docker port nginx-lb
```

Check listening ports:

```bash
sudo ss -tulnp
```

Check firewall:

```bash
sudo ufw status
```

### Issue 3: Nginx Configuration Error

```bash
sudo docker exec nginx-lb nginx -t
```

Display the loaded configuration:

```bash
sudo docker exec nginx-lb nginx -T
```

## 📈 Future Enhancements

Planned improvements:

- Implement HTTPS using SSL/TLS certificates.
- Integrate Prometheus and Grafana monitoring.
- Configure centralized logging.
- Implement CI/CD using GitHub Actions.
- Add Docker image vulnerability scanning.
- Implement container resource limits.
- Introduce automated deployment and monitoring.
- Integrate a persistent database as an additional application component.

## 🎓 Key Learning Outcomes

After completing this project, you will understand:

- Docker image creation and container deployment.
- Dockerfile instructions.
- Docker bridge networking.
- Nginx reverse proxy configuration.
- Nginx Round Robin load balancing.
- Backend application deployment.
- Container health checks.
- Basic failure handling and recovery.
- Linux-based Docker troubleshooting.

## 👨‍💻 Author

**Adnan Attar**

GitHub: https://github.com/AdnanAttar001

---

⭐ If you find this project useful, consider giving the repository a star!

