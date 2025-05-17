# utils/database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config.settings import Config

Base = declarative_base()

class PerformanceResult(Base):
    __tablename__ = 'performance_results'
    id = Column(Integer, primary_key=True)
    agent_order_no = Column(String(50))
    elapsed_time_ms = Column(Float)
    status = Column(String(10))  # success/failure
    response = Column(String(500))
    timestamp = Column(DateTime)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+pymysql://{Config.DB_CONFIG['user']}:{Config.DB_CONFIG['password']}"
            f"@{Config.DB_CONFIG['host']}:{Config.DB_CONFIG['port']}/{Config.DB_CONFIG['database']}?charset=utf8mb4"
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_result(self, result_dict: dict):
        session = self.Session()
        record = PerformanceResult(**result_dict)
        session.add(record)
        session.commit()
        session.close()
