from sqlmodel import SQLModel, create_engine
from models import user_model, flight_model



from dotenv import load_dotenv
import os


# load environment variables
load_dotenv()


__sql_conn_url = os.getenv("POSTGRES_CONN_STRING")

engine = create_engine(__sql_conn_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()