
---

# Teapot

**Teapot** is a collection of helper services developed for **The Join**. These services are designed to streamline and automate verification processes across various communication platforms, including email, Telegram, and Discord.

## Features

- **Email Submission Service**: Receives and stores emails in a PostgreSQL database.
- **Telegram Verification Service**: Verifies if a given Telegram username or phone number is a member of a specified Telegram channel.
- **Discord Verification Service**: Checks if a given Discord user tag is a member of a specified Discord channel.

## Getting Started

### Prerequisites

Before setting up Teapot, ensure you have the following installed:

- Python 3.11+
- PostgreSQL
- pipenv (Python package manager)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/y<hostusername>/teapot.git
   cd teapot
   ```

2. **Install Dependencies**

   ```bash
   pipenv install
   ```

3. **Activate the Virtual Environment**

   ```bash
   pipenv shell
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root of the project and add the following environment variables:

   ```bash
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
   TELEGRAM_API_ID=your_telegram_api_id
   TELEGRAM_API_HASH=your_telegram_api_hash
   TELEGRAM_CHANNEL=your_telegram_channel_name_or_id
   DISCORD_TOKEN=your_discord_token
   ```

5. **Set Up the Database**

   Apply the database migrations to set up the PostgreSQL database.

   ```bash
   python -m teapot.app.models
   ```

6. **Run the Application**

   Start the application using the `uvicorn` server:

   ```bash
   uvicorn main:app --reload
   ```

   The application will be accessible at `http://localhost:8000`.

### Usage

Teapot provides three main endpoints:

1. **Submit Email**

   - **Endpoint**: `POST /submit-email`
   - **Body**: JSON
     ```json
     {
       "email": "user@example.com"
     }
     ```

2. **Verify Telegram**

   - **Endpoint**: `POST /verify-telegram`
   - **Body**: JSON
     ```json
     {
       "identifier": "telegram_username_or_phone"
     }
     ```

3. **Verify Discord**

   - **Endpoint**: `POST /verify-discord`
   - **Body**: JSON
     ```json
     {
       "discord_tag": "username#1234"
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
