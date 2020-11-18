from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, Float, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from datetime import datetime
from dateutil.relativedelta import relativedelta

from .auth import User
from modules.errors import InactiveUserError, OverFreeLimitError

# Should technically be 1 single player and 1 multiplayer but I dont exactly have a way to handle that right now
FREE_LIMIT = 2


class League(app.db.Model):
    __tablename__ = 'league'
    '''
    id (Integer, indexed)
    player_owner (Integer, ForeignKey(User.id), indexed)
    '''
    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True
    )
    owner = Column(
        'owner', UUID(True), ForeignKey(User.id), nullable=False, index=True,
    )
    is_multiplayer = Column(
        'is_multiplayer', Boolean, default=False
    )

    def __repr__(self):
        return f'''
        <League(
            id={self.id},
            owner={self.player_owner},
            is_multiplayer={self.is_multiplayer}
        )>
        '''


class LeagueMember(app.db.Model):
    __tablename__ = 'league_member'
    '''
    id (Integer, indexed)
    league_id (Integer, ForeignKey(League.id), indexed)
    member_id (Integer, ForeignKey(User.id), indexed) -- This should be limited to 2 leagues (1 single player, 1 multiplayer) for free users. That is not something SQL can limit so we will have to limit it server side
    '''

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True
    )
    league_id = Column(
        'league_id', Integer, ForeignKey(League.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )
    member_id = Column(
        'member_id', UUID(True), ForeignKey(User.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    @validates('member_id')
    def validate_member_id(self, key, member_id):
        # Perform check to see if the user is
        # 1) A free member (no last_payment)
        # 2) has 2+ entries in member_id.
        db = app.db
        user = User.query.filter_by(id=member_id).first()
        if not user.is_active:
            raise InactiveUserError()
        league_matches = LeagueMember.query.filter_by(member_id=member_id)
        relativedelta()
        user_is_free_user = user.last_payment > (
            datetime.now() - relativedelta(months=1))
        if len(league_matches.all()) > FREE_LIMIT and user_is_free_user:
            raise OverFreeLimitError(member_id)


@event.listens_for(League, 'after_insert')
def auto_insert_league_member(mapper, connection, target):
    db = app.db
    try:
        league_member = LeagueMember(
            league_id=target.id, member_id=target.player_owner)
        db.session.add(league_member)
        db.session.attempt_commit()
    except Exception as exception:
        # TODO(Mike): Force bad league_member input so you can catch the appropriate exception here. Technically there are 2 possible exceptions you can get and we need to handle them differently
        print(exception)
