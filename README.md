# Receipt API
### Test task for checkbox.ua
This is a simple API that allows you to create and share your receipts with others.
### Requirements
- Make
- Python 3.12^
- Poetry
- Docker
- Docker-compose

### Installation
1. Clone the repository
2. Install the dependencies with poetry `poetry install`
3. Create a copy of `.env.dist` as `.env` file in the root directory and fill it.
4. Start database in docker with `make docker-db`
5. Run migrations with `make migrate`
6. Run the application with `make dev`

### Testing
1. Start database in docker with `make docker-db`
2. Run tests with `make test`


### Generate Secret Key
You can generate a secret key for `.env` with `python -c "import secrets; print(secrets.token_urlsafe(32))"`