
name: Palace of Quests – Run Tests and Build

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test_and_build:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        ports:
          - "5432:5432"
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd="pg_isready -U test_user"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    env:
      DATABASE_URL: postgres://test_user:test_password@localhost:5432/test_db

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.9"

      - name: Cache Python dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Wait for Postgres to be ready
        run: |
          for i in {1..10}; do
            pg_isready -h localhost -U test_user && break
            sleep 2
          done

      - name: Run tests with coverage
        run: |
          pytest --disable-warnings --cov=app --cov-report=xml

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage.xml

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "16"

      - name: Cache Node.js dependencies
        uses: actions/cache@v4
        with:
          path: |
            ~/.npm
            ~/.yarn/cache
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json', '**/yarn.lock') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install Node.js dependencies
        run: npm ci

      - name: Build frontend
        run: npm run build

      - name: Upload frontend build artifact
        uses: actions/upload-artifact@v4
        with:
          name: palace-of-quests-build
          path: build/
