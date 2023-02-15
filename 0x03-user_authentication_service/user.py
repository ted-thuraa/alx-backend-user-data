#!/usr/bin/env python3
"""The `user` model's module
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import desclarative_base

Base = desclarative_base()

class User(Base):
    """Represents a record from the `user` table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)

    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=True)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)