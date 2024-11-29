## 1. Database Setup

## You need to initialize the PostgreSQL database with the provided SQL schema and role configuration.

## Steps:

## 1. Ensure PostgreSQL is running:

## If using Docker Compose, it will start with docker-compose up (see Docker setup below).

## Alternatively, if running PostgreSQL locally, start the service and create the piquest_db database.



## 2. Run Schema and Role Scripts:

## If using Docker Compose, you can set up an initialization script in the database service to automatically run schema.sql and roles.sql.

## Otherwise, connect to your PostgreSQL instance and execute:

## psql -U your_postgres_user -d piquest_db -f database/schema.sql
## psql -U your_postgres_user -d piquest_db -f database/roles.sql



## 3. Update .env with Database Credentials:

## Create an .env file in the backend directory (or use environment variables in Docker) and add:

## DATABASE_URL=postgresql://gameuser:your_secure_password@database/piquest_db
JWT_SECRET_KEY=your_jwt_secret_key




