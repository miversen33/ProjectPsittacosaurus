from models.player import PlayerInfo
from models.team import Game, Team
from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, Float
from sqlalchemy.orm import validates

from datetime import datetime


class Stats(app.db.Model):
    __tablename__ = 'stats'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    name = Column(
        'name', String, nullable=False, unique=True
    )

    def __repr__(self) -> str:
        return f'''
        <Stats(
            id={self.id},
            name={self.name}
        )
        '''
    pass


class PlayerGameStats(app.db.Model):
    __tablename__ = 'player_game_stat'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    game_id = Column(
        'game_id', Integer, ForeignKey(Game.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    stat_id = Column(
        'stat_id', Integer, ForeignKey(Stats.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerGameStats(
            id={self.id},
            player_id={self.player_id},
            game_id={self.game_id},
            stat_id={self.stat_id},
            value={self.value}
        )>
        '''


class PlayerSeasonStats(app.db.Model):
    __tablename__ = 'player_season_stat'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    year = Column(
        'year', Integer, nullable=False
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    stat_id = Column(
        'stat_id', Integer, ForeignKey(Stats.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerSeasonStats(
            id={self.id},
            player_id={self.player_id},
            year={self.year},
            team_id={self.team_id},
            stat_id={self.stat_id},
            value={self.value}
        )>
        '''


class PlayerCareerStats(app.db.Model):
    __tablename__ = 'player_career_stat'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    stat_id = Column(
        'stat_id', Integer, ForeignKey(Stats.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerCareerStats(
            id={self.id},
            player_id={self.player_id},
            stat_id={self.stat_id},
            value={self.value}
        )>
        '''


class Records(app.db.Model):
    __tablename__ = 'record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    name = Column(
        'name', String, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <Records(
            id={self.id},
            name={self.name}
        )>
        '''


class PlayerGameRecord(app.db.Model):
    __tablename__ = 'player_game_record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    game_id = Column(
        'game_id', Integer, ForeignKey(Game.id), nullable=False
    )

    record_id = Column(
        'record_id', Integer, ForeignKey(Records.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerGameRecord(
            id={self.id},
            player_id={self.player_id},
            game_id={self.game_id},
            record_id={self.record_id},
            value={self.value}
        )>
        '''


class TeamGameRecord(app.db.Model):
    __tablename__ = 'team_game_record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    game_id = Column(
        'game_id', Integer, ForeignKey(Game.id), nullable=False
    )

    record_id = Column(
        'record_id', Integer, ForeignKey(Records.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <TeamGameRecord(
            id={self.id},
            team_id={self.team_id},
            game_id={self.game_id},
            record_id={self.record_id},
            value={self.value}
        )>
        '''


class PlayerSeasonRecord(app.db.Model):
    __tablename__ = 'player_season_record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    year = Column(
        'year', Integer, nullable=False
    )

    record_id = Column(
        'record_id', Integer, ForeignKey(Records.id), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerSeasonRecord(
            id={self.id},
            player_id={self.player_id},
            team_id={self.team_id},
            year={self.year},
            record_id={self.record_id},
            value={self.value}
        )>
        '''


class TeamSeasonRecord(app.db.Model):
    __tablename__ = 'team_season_record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    year = Column(
        'year', Integer, nullable=False
    )

    record_id = Column(
        'record_id', Integer, ForeignKey(Records.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <TeamSeasonRecord(
            id={self.id},
            team_id={self.team_id},
            year={self.year},
            record_id={self.record_id},
            value={self.value}
        )>
        '''


class PlayerCareerRecord(app.db.Model):
    __tablename__ = 'player_career_record'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id), nullable=False
    )

    record_id = Column(
        'record_id', Integer, ForeignKey(Records.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    value = Column(
        'value', Float, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <PlayerCareerRecord(
            id={self.id},
            player_id={self.player_id},
            record_id={self.record_id},
            value={self.value}
        )>
        '''
