from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, Float
from sqlalchemy.orm import validates

from datetime import datetime

from .league import League
from .player import PlayerInfo
from .attributes import Attribute
from .position import Position, Subposition


class Team(app.db.Model):
    __tablename__ = 'team_info'

    def generate_random_teamname():
        return 'Random Team Name'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    league_id = Column(
        'league_id', Integer, ForeignKey(League.id, ondelete='CASCADE', onupdate='CASCADE'), index=True, nullable=False
    )

    name = Column(
        'name', String(128), nullable=False, default=generate_random_teamname
    )

    def __repr__(self) -> str:
        return f'''
        <Team(
            id={self.id},
            league_id={self.league_id},
            name={self.name}
        )>
        '''


class TeamRoster(app.db.Model):
    __tablename__ = 'team_roster'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    position_id = Column(
        'position_id', Integer, ForeignKey(Position.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    subposition_id = Column(
        'subposition_id', Integer, ForeignKey(Subposition.id, ondelete='CASCADE', onupdate='CASCADE'), default=None
    )

    depth_chart_position = Column(
        'depth_chart_position', Integer, default=None
    )

    def __repr__(self) -> str:
        return f'''
        <TeamRoster(
            id={self.id},
            team_id={self.team_id},
            player_id={self.player_id},
            position_id={self.position_id},
            subposition_id={self.subposition_id},
            depth_chart_position={self.depth_chart_position}
        )>
    '''

#     @validates('player_id')
#     def verify_player_is_on_one_team(self, key, player_id):
#         print("TODO(Mike): Implement validator for making sure a player is on one team only")
#         print(repr(self))
#         # if len(
#         #     TeamRoster.query.filter(
#         #         TeamRoster.player_id=player_id,
#         #         TeamRoster.team_id!=self.team_id
#         #     ).all()) > 1:


class TeamAttributes(app.db.Model):
    __tablename__ = 'team_attribute'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id, ondelete='CASCADE', onupdate='CASCADE'), index=True, nullable=False
    )

    attribute_id = Column(
        'attribute_id', Integer, ForeignKey(Attribute.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    attribute_value = Column(
        'attribute_value', String(128), nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <TeamAttributes(
            id={self.id},
            team_id={self.team_id},
            attribute_id={self.attribute_id},
            attribute_value={self.attribute_value}
        )>
        '''


class Stadium(app.db.Model):
    __tablename__ = 'stadium'

    def init_capacity_generator(context):
        team = Team.query.filter_by(
            context.get_current_parameters()['team_id'])
        return 0

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id), index=True, nullable=False
    )

    name = Column(
        'name', String(256), default=None
    )

    max_capacity = Column(
        'max_capacity', Integer, nullable=False, default=init_capacity_generator
    )

    level = Column(
        'level', Integer, nullable=False, default=1
    )

    @validates('level')
    def check_level(self, key, level):
        team = Team.query.filter_by(self.team_id).name
        if level <= 0 or level > 10:
            raise ValueError(
                f'Stadium: {self.name} level for Team: {team} cannot be greater than 10 or less than 1')
        return level

    def __repr__(self) -> str:
        return f'''
        <Stadium(
            id={self.id},
            team_id={self.team_id},
            name={self.name},
            max_capacity={self.max_capacity},
            level={self.level}
        )>
        '''


class Game(app.db.Model):
    __tablename__ = 'game'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    home_team_id = Column(
        'home_team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    away_team_id = Column(
        'away_team_id', Integer, ForeignKey(Team.id), nullable=False
    )

    played_in = Column(
        'played_in', Integer, ForeignKey(Stadium.id), nullable=False
    )

    who_won = Column(
        'who_won', Integer, ForeignKey(Team.id), nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <Game(
            id={self.id},
            home_team_id={self.home_team_id},
            away_team_id={self.away_team_id},
            played_in={self.played_in},
            who_won={self.who_won}
        )>
        '''


class Contract(app.db.Model):
    __tablename__ = 'contract'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    team_id = Column(
        'team_id', Integer, ForeignKey(Team.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    start_year = Column(
        'start_year', Integer, nullable=False
    )

    length = Column(
        'length', Integer, nullable=False
    )

    end_year = Column(
        'end_year', Integer, nullable=False
    )

    was_fired = Column(
        'was_fired', Boolean, default=False
    )

    def __repr__(self) -> str:
        return f'''
        <Contract(
            id={self.id},
            player_id={self.player_id},
            team_id={self.team_id},
            start_year={self.start_year},
            length={self.length},
            end_year={self.end_year},
            was_fired={self.was_fired}
        )>
        '''


class ContractGoals(app.db.Model):
    __tablename__ = 'contract_goals'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    goal = Column(
        'goal', String, nullable=False
    )

    league_level_bind = Column(
        'league_level_bind', Integer, default=None
    )

    def __repr__(self) -> str:
        return f'''
        <ContractGoals(
            id={self.id},
            goal={self.goal},
            league_level_bind={self.league_level_bind}
        )>
        '''


class ContractGoalMap(app.db.Model):
    __tablename__ = 'contract_goal_map'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    contract_id = Column(
        'contract_id', Integer, ForeignKey(Contract.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    goal_id = Column(
        'goal_id', Integer, ForeignKey(ContractGoals.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    x_definition = Column(
        'x_definition', Integer, nullable=False
    )

    validator_method = Column(
        'validator_method', String, nullable=False
    )


"""
# class Team(TeamModel):
#     pass
    '''
    id (Integer, indexed),
    name (varchar),
    country (Location ForeignKey)
    province (Location ForeignKey)
    city (Location ForeignKey)
    mascot (Mascot ForeignKey)
    stadium (Stadium ForeignKey)
    player_owner (Integer. If not null, consider it a foreign key to User)
    '''

# class Location(TeamModel):
#     pass

# class Mascot(TeamModel):
#     pass

# class Stadium(TeamModel):
#     pass
"""

# class Player(app.db.Model):
#     '''
#     id (Integer, indexed),
#     league_id (Integer, ForeignKey(league.id), indexed)
#     name (varchar)
#     '''
#     __tablename__ = 'player'

#     id = Column(
#         'id', Integer, autoincrement=True, primary_key=True, nullable=False, unique=True
#     )
#     league_id = Column(
#         'league_id', Integer, ForeignKey(League.id), index=True, nullable=False
#     )
#     name = Column(
#         'name', String, nullable=False
#     )

#     def __repr__(self):
#         return f'''
#         <Player(
#             id={self.id},
#             league_id={self.league_id},
#             name={self.name}
#         )>
#         '''
