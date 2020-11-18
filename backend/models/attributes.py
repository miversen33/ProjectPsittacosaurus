from flask import current_app as app
from sqlalchemy import Column, ForeignKey, String, Integer, Boolean, DateTime, event, Float
from sqlalchemy.orm import validates

class Attribute(app.db.Model):

    __tablename__ = 'attribute'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True,
        unique=True, index=True
    )

    name = Column(
        'name', String, unique=True, index=True, nullable=False
    )

    boostable = Column(
        'boostable', Boolean, default=True, nullable=False
    )

    def __repr__(self):
        return f'''
        <Attribute(
            id={self.id},
            name={self.name},
            boostable={self.boostable}
        )>
        '''

# @event.listens_for(Attribute, 'after_insert')
# def auto_insert_attribute_subtables(mapper, connection, attribute):
#     db = app.db
#     try:
#         for player in Player.query.all():
#             db.session.add(PlayerAttribute(
#                 player_id=player.id,
#                 attribute_id=attribute.id,
#             ))
#             db.session.add(AttributeBoost(
#                 player_id=player.id,
#                 attribute_id=attribute.id
#             ))
#     except Exception as exception:
#         print(repr(exception), exception)
#     try:
#         for subposition in Subposition.query.all():
#             db.session.add(BaseAttribute(
#                 position_id=subposition.parent_position_id,
#                 subposition_id=subposition.id,
#                 attribute_id=attribute.id
#             ))
#     except Exception as exception:
#         print(repr(exception), exception)