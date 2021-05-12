# Flask starter
Simple Python Flask backend server starter project.

___

###### _Note: Instructions are MacOS-specific_

## Setup

Setup the project by installing the requirements and running a [PostgreSQL](https://www.postgresql.org/) database locally.

1. Install requirements

    ```
    pip install -r requirements.txt
    ```

2. Run a PostgreSQL database

    * Download and install [postgres.app](https://postgresapp.com/)

    * Open Postgres and enter `localhost` as the host when prompted

    * Click `Start` to run Postgres

        ![alt text](docs/postgres-app-running.png)

    * Execute SQL command to create a test database

        ```
        postgres=# CREATE DATABASE flask_starter;
        ```

## Testing

Test the project by running the [Flask](https://flask.palletsprojects.com/en/2.0.x/) app locally and querying the API using [Postman](https://www.postman.com/).

1. Add `.env` file to the root project directory

    ```
    AUTH_TOKEN_LIFESPAN_SEC=180
    DATABASE_URL=postgresql:///flask_starter
    FLASK_ENV=development
    SECRET_KEY=add-your-secret-key-here
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    ```

2. Run the Flask app locally

    ```
    python app.py
    ```
3. Query the API using Postman

    * Download [Postman](https://www.postman.com/downloads/)

    * Import [this](docs/flask_starter.postman_collection.json) test collection

    * Executing Postman requests to the Flask app running locally

        * Include request parameters under `Body` (form data)

            ![alt text](docs/postman-request-body.png)

        * Include the authentication token under `Headers`

            ![alt text](docs/postman-request-headers.png)

## Deployment

Deploy the project on [Heroku](https://heroku.com) for free.

1. [Create](https://dashboard.heroku.com/new-app) a new Heroku app

    * Add all constants from `.env` to your app, except `DATABASE_URL`

        * `Settings` -> `Config Vars`

2. Connect the Heroku app to a [GitHub](https://github.com/) repo containing this codebase.

    ![alt text](docs/heroku-connect-github.png)

    * Enable `Automatic Deployment` from branch `main`

3. Add the [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql) add-on.

    ![alt text](docs/heroku-postgres-addon.png)

    * This will add the DATABASE_URL` to your Heroku app
