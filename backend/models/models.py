from typing import Any
from flask import current_app as app
# Model imports
from .auth import User, UserSession
from .attributes import Attribute
from .position import Position, Subposition, BaseAttribute
from .league import League, LeagueMember
from .location import Location
from .log import APILog
from .player import PlayerInfo, PlayerAttribute, AttributeBoost
from .stat import Stats, PlayerGameStats, PlayerCareerStats, TeamGameRecord, TeamSeasonRecord, PlayerGameRecord, PlayerSeasonRecord, PlayerCareerRecord

_models = [
    User, 
    UserSession,
    Attribute,
    Position,
    Subposition,
    BaseAttribute,
    League, 
    LeagueMember,
    Location,
    APILog,
    PlayerInfo,
    PlayerAttribute, 
    AttributeBoost,
    Stats, 
    PlayerGameStats, 
    PlayerCareerStats, 
    TeamGameRecord,
    TeamSeasonRecord, 
    PlayerGameRecord, 
    PlayerSeasonRecord, 
    PlayerCareerRecord
]

def init_tables(db, ignore_table_failure=False):
    '''
    If ignore_table_failure is true, we will print out that creating a table failed, and then carry on. This should only be used
    for debugging purposes. It will be removed after basic setup is done
    '''
    # from .auth import User
    engine = db.engine
    # User.metadata.create_all(engine)
    for model in _models:
        try:
            model.metadata.create_all(engine)
        except Exception as exception:
            if(ignore_table_failure):
                print(f'{model} creation failed')
                print(exception)
            else:
                raise exception