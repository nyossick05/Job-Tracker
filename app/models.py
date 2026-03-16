from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from datetime import datetime, timezone
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    applications = relationship("Application", back_populates="owner")

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    position = Column(String, index=True)
    status = Column(String, index=True)
    applied_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    owner_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    owner = relationship("User", back_populates="applications")