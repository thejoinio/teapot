
---

# Teapot

**Teapot** is a Django-based project designed to create helper services for **The Join**, a company. The project includes services for email submission, Telegram user verification, and Discord user verification.

## Features

- **Email Submission Service**: Receives and stores emails in a PostgreSQL database.
- **Telegram Verification Service**: Verifies if a given Telegram username or phone number is a member of a specified Telegram channel.
- **Discord Verification Service**: Checks if a given Discord user tag is a member of a specified Discord channel.

## Getting Started

### Prerequisites

Before setting up Teapot, ensure you have the following installed:

- Python 3.11+
- Django 4.x
- PostgreSQL
- pipenv (Python package manager)
- Heroku CLI (deployment)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/y<hostusername>/teapot.git
   cd teapot
   ```

2. **Install Dependencies**

   ```bash
   pipenv install --dev
   ```

3. **Activate the Virtual Environment**

   ```bash
   pipenv shell
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root of the project and add the following environment variables:

   ```bash
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=database_name
   DB_USER=database_user
   DB_PASS=database_password
   DB_HOST=localhost
   DB_PORT=5432
   TELEGRAM_API_ID=telegram_api_id
   TELEGRAM_API_HASH=telegram_api_hash
   TELEGRAM_CHANNEL=telegram_channel_name_or_id
   TELEGRAM_BOT=telegram_bot
   TELEGRAM_BOT_TOKEN=telegram_bot_token
   TELETHON_SESSION=telethon_session
   DISCORD_TOKEN=discord_token
   ```

5. **Set Up the Database**

   Apply the database migrations to set up the PostgreSQL database.

   ```bash
   python manage.py migrate
   ```

6. **Run the Application**

   Start the application using the `uvicorn` server:

   ```bash
   python manage.py runserver
   ```

   The application will be accessible at `http://localhost:8000`.

### Deployment on Heroku

1. **Access Heroku App**

   An Heroku App has been created to run the app. Contact the head of engineering to get access to the `staging` and `prod` apps.

2. **Deployment to Heroku**

   Push changes to a feature branch and create a PR to merge on `staging`. Accepted PRs are merged to main and auto-deployed.


### Usage

Teapot provides three main endpoints:

1. **Submit Email**

   - **Endpoint**: `POST /helper/submit-email/`
   - **Body**: JSON
     ```json
     {
       "address": "user@example.com"
     }
     ```

2. **Verify Telegram**

   - **Endpoint**: `POST /helper/verify-telegram/`
   - **Body**: JSON
     ```json
     {
       "username": "telegram_username"
     }
     ```

3. **Verify Discord**

   - **Endpoint**: `POST /herlper/verify-discord/`
   - **Body**: JSON
     ```json
     {
       "username": "discord_username"
     }
     ```

### Running Tests

To run the provided tests, use Postman or any other API testing tool. Import the provided Postman collection and environment to verify each endpoint.

### Contributing

We welcome contributions to Teapot! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push your branch and create a pull request.

### License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt) file for details.
