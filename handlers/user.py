""" User route handler """

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models import UserModel


class RegisterUser(Resource):
    """ User registration handler"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "email", type=str, required=True, help="email field is required"
    )
    parser.add_argument(
        "password", type=str, required=True, help="password is required"
    )

    def generate_response(self, success: bool, message: str) -> dict:
        """return error message dict"""
        return {"success": success, "message": message}

    def post(self):
        """create user by email and password"""
        req_data = self.parser.parse_args()

        if UserModel.find_by_email(req_data["email"]):
            return self.generate_response(False, "user_exists"), 400

        user = UserModel(**req_data)
        user.save_to_db()

        return self.generate_response(True, "user_created"), 201


class LoginUser(Resource):
    """ User login resource"""

    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, help="field missing")
    parser.add_argument("password", type=str, required=True, help="field missing")

    def post(self):
        """Returns access_token for in exchange to valid user credentials"""
        req_data = self.parser.parse_args()
        user = UserModel.find_by_email(req_data["email"])
        if not user or user.password != req_data["password"]:
            return {"success": False, "message": "invalid_credentials"}, 400

        access_token = create_access_token(identity=user.id)
        return {"success": True, "access_token": access_token}

