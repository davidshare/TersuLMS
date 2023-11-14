# TersuLMS
A learning management system


## Start the app
`uvicorn src.main:app --reload`

## Run migrations
`alembic revision --autogenerate -m "<description of migration>"` [//]: <> Create the migration
`alembic upgrade head` [//]: <> update the database

## Important urls
### FastAPI documentation
- http://<HOST>:8000/doc
- http://<HOST>:8000/redoc

### Best practices adopted
- https://github.com/zhanymkanov/fastapi-best-practices