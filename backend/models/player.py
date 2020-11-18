from flask import current_app as app
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import validates

from .league import League
from .attributes import Attribute


class PlayerInfo(app.db.Model):
    __tablename__ = 'player_info'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    league_id = Column(
        'league_id', Integer, ForeignKey(League.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    name = Column(
        'name', String, nullable=False
    )


class PlayerAttribute(app.db.Model):
    __tablename__ = 'player_attribute'

    id = Column(
        'id', Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, index=True
    )

    player_id = Column(
        'player_id', Integer, ForeignKey(PlayerInfo.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    attribute_id = Column(
        'attribute_id', Integer, ForeignKey(Attribute.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    attribute_value = Column(
        'attribute_value', Float, nullable=False
    )

    @validates('attribute_id')
    def validate_unique_attribute_id(self, key, attribute_id):
        player = PlayerInfo.query.filter_by(id=self.player_id).first().name
        attribute = Attribute.query.filter_by(id=attribute_id).first().name
        if attribute_id in [attr_id for attr_id in PlayerAttribute.query.filter_by(player_id=self.player_id).attribute_id]:
            raise ValueError(
                f'Unable to add Attribute: {attribute} to Player: {player}. Attribute already exists')
        return attribute_id


class AttributeBoost(app.db.Model):
    __tablename__ = "attribute_boost"

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True,
        unique=True, index=True
    )

    player_id = Column(
        'player_id', ForeignKey(PlayerInfo.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    attribute_id = Column(
        'attribute_id', ForeignKey(Attribute.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False
    )

    ingame_boost = Column(
        'ingame_boost', Float, default=0
    )

    momentum_boost = Column(
        'momentum_boost', Float, default=0
    )

    @validates('attribute_id')
    def validate_attribute_id(self, key, attribute_id):
        attribute = Attribute.query.filter_by(
            id=attribute_id).first().boostable
        if not attribute.boostable:
            raise ValueError(f'Attribute: {attribute.name} is not boostable')
        return attribute_id

    def __repr__(self):
        return f'''
        <AttributeBoost(
            id={self.id},
            player_id={self.player_id},
            attribute_id={self.attribute_id},
            ingame_boost={self.ingame_boost},
            momentum_boost={self.momentum_boost}
        )>
        '''
