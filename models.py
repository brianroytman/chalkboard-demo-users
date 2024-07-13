from sqlalchemy import Column, String, DateTime, Integer
from datetime import datetime, timezone
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    
    # Dynamic default and onupdate in UTC timezone
    date_created = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    date_updated = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.username} at {self.date_created}>"
