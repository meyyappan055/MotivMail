# MotivMail

MotivMail is a web application that sends daily motivational quotes to subscribers via email.

## Tech Stack

- **Backend Framework**: FastAPI
- **Database**: MySQL with SQLAlchemy ORM
- **Scheduler**: APScheduler

## Features

- Fetches motivational quotes from [Quotable API]((https://api.quotable.io)]) - an open source API
- Initially fetches 100 quotes and stores them in the database for faster access. When the stored quotes run out, it fetches more from the API.
- Sends daily emails with quotes to subscribers

## Installation

To get started with MotivMail, follow these steps:

1. **Installation**:
   ```sh
   git clone https://github.com/meyyappan055/MotivMail.git
   cd MotivMail
   pip install -r requirements.txt


## Running the Application
Start the FastAPI server:
```sh
uvicorn backend.app.main:app --reload
