from uuid import uuid4 as uuid

from flask import current_app as app
from flask.globals import session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, Float, event
from sqlalchemy.orm import validates

from datetime import datetime

class User(app.db.Model):
    _PASSWORD_LENGTH = 60
    '''
    Columns
        id UUID unique indexed,
        username String unique indexed,
        password (Hash) String,
        email_address String unique,
        creation_date DateTime,
        last_login DateTime,
        2fa_secret String/Null,
        last_payment_date DateTime,
        is_active Boolean,
        consecutive_failed_logins Integer (should be 0 once a succesful login happens. May not be the best place to put this?)
    '''

    editable_fields = [
        'user_name',
        'password',
        'email_address',
        'secret',
        'is_active'
    ]

    __tablename__ = 'user'
    
    id = Column(
        'id', UUID(True), primary_key=True, nullable=False, unique=True, default=uuid
    )
    user_name = Column(
        'user_name', String, unique=True, index=True, nullable=False
    )
    password = Column(
        'password', String(_PASSWORD_LENGTH), nullable=False
    )
    email_address = Column(
        'email_address', String, nullable=False, unique=True
    )
    creation_date = Column(
        'creation_date', DateTime, nullable=False, default=datetime.now()
    )
    last_login = Column(
        'last_login', DateTime, nullable=False, default=datetime.now()
    )
    secret = Column(
        'secret', String , nullable=True
    )
    last_payment = Column(
        'last_payment_date', DateTime, nullable=True
    )
    is_active = Column(
        # TODO(Mike): Change default to be False, and make "is_active" be triggered via email activation link
        'is_active', Boolean, default=True
    )
    consecutive_failed_logins = Column(
        'consecutive_failed_logins', Integer, default=0
    )

    def __repr__(self):
        return f'''
        <User(
            id={self.id}, 
            user_name='{self.user_name}', 
            password= , 
            email_address='{self.email_address}', 
            creation_date='{self.creation_date}', 
            last_login='{self.last_login}', 
            secret={" " if self.secret != None else "None"}, 
            last_payment={self.last_payment}, 
            is_active={self.is_active}, 
            consecutive_failed_logins={self.consecutive_failed_logins}
        )>'''

class UserSession(app.db.Model):
    # This needs a backend job that clears out any item that is older than whatever the users set timeout is. As we dont
    # Have that defined yet, we will assume 1 hour
    '''
    Columns
        id Integer unique indexed,
        session_key unique String (UUID probably),
        session_type String (Should be 'w', 'm', 'd' for 'website', 'mobile', or 'desktop')
        user_id (either linked to user.id or user.user_id) Integer unique indexed ForeignKey(user.whateverLink),
        last_hit DateTime,
        last_ip_hit_from String (Im not fond of keeping this, but it will help us reduce bad attempts on a user)
    '''

    __tablename__ = 'session'

    _valid_session_types = ['web', 'desktop', 'mobile']

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True
    )
    session_key = Column(
        'session_key', String(36), unique=True, default=lambda: str(uuid())
    )
    session_type = Column(
        'session_type', String(8), nullable=False
    )
    user_id = Column(
        'user_id', UUID(True), ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'), unique=True, index=True
    )
    last_hit = Column(
        'last_hit', DateTime, default=datetime.now()
    )

    @validates('session_type')
    def validate_session_type(self, key, session_type):
        if session_type not in self._valid_session_types:
            raise ValueError()
        return session_type

    def __repr__(self) -> str:
        return f'''
        <UserSession(
            id={self.id},
            session_key= ,
            session_type={self.session_type},
            user_id={self.user_id},
            last_hit={self.last_hit}
        )>
        '''
