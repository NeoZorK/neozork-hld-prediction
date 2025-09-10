# Getting Started

Welcome to the Pocket Hedge Fund development environment. This guide will help you set up your development environment and start contributing.

## Clone the Repository

Get the source code

```bash

git clone https://github.com/pockethedgefund/neozork-hld-prediction.git
cd neozork-hld-prediction

```

## Set Up Python Environment

Create and activate virtual environment

```bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

```

## Set Up Environment Variables

Configure your development environment

```bash

cp .env.example .env
# Edit .env with your configuration

```

## Start Development Services

Launch database and Redis

```bash

docker-compose up -d postgres redis

```

## Run Database Migrations

Set up the database schema

```bash

alembic upgrade head

```

## Start the Development Server

Launch the FastAPI application

```bash

uvicorn src.pocket_hedge_fund.main:app --reload --host 0.0.0.0 --port 8000

```

