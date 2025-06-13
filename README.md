# Project Setup and Run Instructions

Follow these steps to set up and run the project from scratch:

## Prerequisites

1. Install **Docker** and **Docker Compose** on your system.
2. Ensure you have an active internet connection.

---

## Steps to Run the Project

### 1. Clone the Repository

```bash
git clone git@github.com:XusanDev07/tgbot_shop.git
cd tgbot_shop
```

### 2. Configure Environment Variables
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env

### 3. Build Docker Images

```bash
docker-compose build
```

### 4. Apply Migrations

Run the following command to create the database tables:

```bash
docker-compose run web python manage.py migrate
```

### 5. Create a Superuser (Optional)

To access the Django admin panel, create a superuser:

```bash
docker-compose run web python manage.py createsuperuser
```

### 6. Start the Services

Run the following command to start both the Django application and the Telegram bot:

```bash
docker-compose up --build
```
