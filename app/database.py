from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Make sure to properly escape special characters in the password if needed

DATABASE_URL = "mysql+pymysql://root:Amneal%40123@localhost/epbx_logs"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
