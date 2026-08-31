# 🚀 Django + MySQL Production Deployment with Docker on AWS

This repository contains a containerized **Django** web application connected to a **MySQL** database. It is designed to be fully portable, allowing you to develop seamlessly on a Windows machine and deploy flawlessly to a free-tier Linux VPS on **AWS (Amazon Web Services) EC2** using Docker.

---

## 🛠️ Architecture Overview

- **Web Application**: Django running inside a Python-based Linux container.
- **Database**: MySQL Server running inside a persistent, isolated container.
- **Orchestration**: Docker Compose manages container networking, environment variables, and volume storage.

---

## 💻 Local Development Setup (Windows / macOS)

### Prerequisites
Make sure you have [Docker Desktop](https://docker.com) installed and running on your computer.

### Steps to Run Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```

2. **Launch the containers:**
   ```bash
   docker compose up --build
   ```

3. **Run database migrations (First-time setup):**
   Open a new terminal tab and execute:
   ```bash
   docker compose exec web python manage.py migrate
   ```

4. **Create a superuser (Admin panel access):**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   *Your app will now be live locally at `http://localhost:8000`.*

---

## ☁️ Production Deployment on AWS EC2 (Step-by-Step)

Follow these steps to deploy your live project on the AWS Free Tier for 12 months.

### Phase 1: Server Setup (AWS Console)
1. Go to **AWS EC2 Dashboard** and click **Launch Instance**.
2. Select **Ubuntu Server 24.04 LTS** (Free Tier Eligible).
3. Choose instance type **t2.micro** (or `t3.micro` based on region).
4. Create and download a new **Key Pair** (`.pem` file). Keep this secure!
5. In **Network Settings**, check boxes to:
   - Allow **SSH** (Port 22)
   - Allow **HTTP** (Port 80)
   - Allow **HTTPS** (Port 443)
6. Click **Launch**.

### Phase 2: Server Configuration (Via SSH)
1. Open your terminal, navigate to your `.pem` key folder, and log into your server:
   ```bash
   ssh -i your_key.pem ubuntu@your_aws_public_ip
   ```
2. **Install Docker Engine & Compose:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   curl -fsSL https://docker.com -o get-docker.sh && sudo sh get-docker.sh
   sudo apt install docker-compose-plugin -y
   sudo usermod -aG docker $USER
   ```
3. **Exit and log back in** for the permissions to take effect:
   ```bash
   exit
   ssh -i your_key.pem ubuntu@your_aws_public_ip
   ```

### Phase 3: Project Deployment
1. **Clone your repository onto the server:**
   ```bash
   git clone https://github.com
   cd your-repo-name
   ```
2. **Configure Django Production Settings (`settings.py`):**
   Ensure your configuration values are updated for safe deployment:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your_aws_public_ip', 'localhost', '127.0.0.1']
   ```
3. **Launch the production app in the background:**
   ```bash
   docker compose up --build -d
   ```
   *-d runs the container in detached mode, keeping it alive even after you close the terminal.*

4. **Run migrations on the cloud database:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

---

## 🔒 Production Best Practices Implemented

- **Data Persistence**: MySQL uses Docker named volumes (`mysql_data`). If a container crashes or restarts, **no data is lost**.
- **Security Isolation**: The MySQL database container is not exposed to the public internet; it can only talk internally to the Django app container over a secure Docker network.
- **Environment Isolation**: Separate build contexts ensure Windows system bugs do not disrupt the production environment hosted on Linux.

---

## 📝 Useful Docker Maintenance Commands

- **Check running status:** `docker ps`
- **View app logs in real time:** `docker compose logs -f web`
- **Stop all services gracefully:** `docker compose down`
- **Restart containers after a code update:** `docker compose down && docker compose up --build -d`
