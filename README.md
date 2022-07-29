$ pip install -r requirements.txt

$ alembic init migirations

env.py should be changed accordingly

create models

$ alembic revision --autogenerate -m "initial"

$ alembic upgrade head