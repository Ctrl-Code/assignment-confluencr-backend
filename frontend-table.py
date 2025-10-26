# install dependencies first:
# pip install sqlalchemy psycopg2-binary python-dotenv

from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

# Load Supabase credentials from .env file
# .env file example:
# DATABASE_URL=postgresql+psycopg2://postgres:<password>@<host>:6543/postgres
config = dotenv_values(".env")
DATABASE_URL = config.get("DATABASE_URL")

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Define the table model
class EmailData(Base):
    __tablename__ = "emails_table"
    email = Column(String(255), primary_key=True, nullable=False)
    data_json = Column(String, nullable=True)  # store JSON as string

# Create the table in Supabase
Base.metadata.create_all(engine)

print("Table 'emails_table' created successfully in Supabase!")
