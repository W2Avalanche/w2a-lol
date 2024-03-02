
from utils import read_config, Configuration
config : Configuration = read_config('../configuration.json')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(config.database_user, config.database_password, config.database_host, config.database_port, config.database_name)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base = declarative_base()