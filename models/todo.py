""" TODO model """

from datetime import datetime
from settings import DB


class TodoModel(DB.Model):
    """Todo model has all todo related functionality such as saving and retrieving from db"""

    __tablename__ = "todo"

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(256), nullable=False)
    desc = DB.Column(DB.String(256), nullable=True)
    status = DB.Column(DB.Boolean, nullable=False)
    created_at = DB.Column(DB.DateTime, default=datetime.utcnow())
    updated_at = DB.Column(DB.DateTime)
    owner = DB.Column(DB.Integer, DB.ForeignKey("user.id"))
    user = DB.relationship("UserModel")

    def __init__(self, title: str, desc: str, status: bool, owner: int):
        self.title = title
        self.desc = desc
        self.status = status
        self.owner = owner

    def to_json(self) -> dict:
        """ returns dict representation of the object"""
        return {
            "id": self.id,
            "title": self.title,
            "desc": self.desc,
            "status": self.status,
            "owner": self.owner,
        }

    def save_to_db(self):
        """Save (TodoModel) into db"""
        DB.session.add(self)
        DB.session.commit()

    def delete_from_db(self):
        """Delete (TodoModel) from db"""
        DB.session.delete(self)
        DB.session.commit()

    @classmethod
    def find_by_user(cls, user_id: str) -> "TodoModel":
        """return all todo items where owner is user_id"""
        return cls.query.filter_by(owner=user_id).all()

    @classmethod
    def find_by_id(cls, _id: int) -> "TodoModel":
        """returns one todo by id"""
        return cls.query.filter_by(id=_id).first()
