from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, Float, event
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import insert, select

from .attributes import Attribute
class Position(app.db.Model):
    __tablename__ = 'position'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    name = Column(
        'name', String(128), nullable=False
    )

    side = Column(
        'side', String(32), default=''
    )

    def __repr__(self):
        return f'''
        <Position(
            id={self.id},
            name={self.name},
            side={self.side}
        )>
        '''


class Subposition(app.db.Model):
    __tablename__ = 'subposition'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    parent_position_id = Column(
        'parent_position_id', Integer, ForeignKey(Position.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    name = Column(
        'name', String(128), nullable=False
    )

    parent_position__relationship = relationship(
        'Position', cascade='all, delete-orphan', single_parent=True
    )

    def __repr__(self):
        return f'''
        <Subposition(
            id={self.id},
            parent_position_id={self.parent_position_id},
            name={self.name}
        )>
        '''


class BaseAttribute(app.db.Model):
    __tablename__ = 'base_attribute'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    position_id = Column(
        'position_id', Integer, ForeignKey(Position.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True
    )

    subposition_id = Column(
        'subposition_id', Integer, ForeignKey(Subposition.id, ondelete='CASCADE', onupdate='CASCADE'), nullable=True, default=None
    )

    attribute_id = Column(
        'attribute_id', Integer, ForeignKey(Attribute.id, ondelete='CASCADE', onupdate='CASCADE'), index=True, nullable=False
    )

    attribute_value = Column(
        'attribute_value', Integer, nullable=False, default=40
    )

    attribute_deviation = Column(
        'attribute_deviation', Float, nullable=False, default=0.0
    )

    attribute_mean = Column(
        'attribute_mean', Float, nullable=False, default=40
    )

    attribute_generation_cap = Column(
        'attribute_generation_cap', Float, nullable=False, default=5
    )

    attribute_importance = Column(
        'attribute_importance', Float, nullable=False, default=.25
    )

    # parent_position_relationship = relationship(
    #     'Position', cascade='all'
    # )

    # subposition_relationship = relationship(
    #     'Subposition', cascade='all'
    # )

    # attribute_relationship = relationship(
    #     'Attribute', cascade='all'
    # )

    def __repr__(self):
        return f'''
        <BaseAttribute(
            id={self.id},
            position_id={self.position_id},
            subposition_id={self.subposition_id},
            attribute_id={self.attribute_id},
            attribute_value={self.attribute_value},
            attribute_deviation={self.attribute_deviation},
            attribute_mean={self.attribute_mean},
            attribute_generation_cap={self.attribute_generation_cap},
            attribute_importance={self.attribute_importance}
        )>
        '''

# @event.listens_for(Position, 'after_insert')
# def auto_insert_neutral_subposition_for_position(mapper, connection, position):
#     db = app.db
#     try:
#         db.session.add(Subposition(name='Neutral', parent_position_id=position.id))
#         db.session.attempt_commit()
#     except Exception as exception:
#         print(repr(exception), exception)

# @event.listens_for(Subposition, 'after_insert')
# def auto_insert_attribute_for_players(mapper, connection, subposition):
#     from .attributes import Attribute, BaseAttribute
#     db = app.db
#     try:
#         position = Position.query.filter_by(id=subposition.parent_position_id).first()
#         for attribute in Attribute.query.all():
#             db.session.add(BaseAttribute(
#                 position_id=position.id,
#                 subposition_id=subposition.id,
#                 attribute_id=attribute.id
#             ))

#         db.session.attempt_commit()
#     except Exception as exception:
#         print(repr(exception), exception)
