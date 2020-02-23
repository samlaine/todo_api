""" User model """

from settings import DB


class UserModel(DB.Model):
    """ User model has user related functionality such as saving and retrieving from db"""

    __tablename__ = "user"

    id = DB.Column(DB.Integer, primary_key=True)
    email = DB.Column(DB.String(80))
    password = DB.Column(DB.String(80))

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def save_to_db(self):
        """ Saves (UserModel) object to database"""
        DB.session.add(self)
        DB.session.commit()

    def to_json(self) -> dict:
        """ returns dict representation of (UserModel)"""
        return {"id": self.id, "email": self.email, "password": self.password}

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        """Gets user with given email from database
        :param email(String) email of the user
        """
        return cls.query.filter_by(email=email).first() or None

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        """Gets user with given id from database
        :param _id(int) id of the user
        """
        return cls.query.filter_by(id=_id).first() or None
