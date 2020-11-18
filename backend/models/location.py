from flask import current_app as app
from sqlalchemy import Column, String, Integer

class Location(app.db.Model):
    __tablename__ = 'location'

    id = Column(
        'id', Integer, primary_key=True, nullable=False, autoincrement=True, unique=True, index=True
    )

    type = Column(
        'type', String(16), nullable=False
    )

    name = Column(
        'name', String, nullable=False
    )

    def __repr__(self) -> str:
        return f'''
        <Location(
            id={self.id},
            type={self.type},
            name={self.name}
        )>
        '''