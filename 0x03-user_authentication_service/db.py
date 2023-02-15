#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database.
        """
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ Document string for the checker  """
        dbm = self._session
        main = dbm.query(User)
        for key, value in kwargs.items():
            main = main.filter_by(**{key: value})
        if not main.first():
            dbm.commit()
            raise NoResultFound
        else:
            dbm.commit()
            return main.first()

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Document string for the checker  """
        try:
            check = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError
        dbm = self._session
        for key, value in kwargs.items():
            if not hasattr(check, key):
                raise ValueError
            setattr(check, key, value)
        dbm.commit()
