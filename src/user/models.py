from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship

from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    date_of_birth = Column(TIMESTAMP, nullable=False)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(TIMESTAMP)
    phone_number = Column(String)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role")
