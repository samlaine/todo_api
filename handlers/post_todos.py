""" Post todo handler resource """
import logging
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import TodoModel

logger = logging.getLogger()


class PostTodos(Resource):
    """ Create new Todo item """

    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True, help="Field is required")
    parser.add_argument("desc", type=str, required=False, help="Field is required")
    parser.add_argument("status", type=bool, required=True, help="Field is required")

    @jwt_required
    def post(self):
        """ Create new todo item"""

        req_data = self.parser.parse_args()
        user_id = get_jwt_identity()
        new_todo = TodoModel(**req_data, owner=user_id)

        try:
            new_todo.save_to_db()
        except Exception as exception:
            logger.debug(
                f"Exception occured when creating a todo with params: {new_todo}, {exception}",
            )
            return {"success": False, "message": "internal_error"}, 500

        return {
            "success": True,
            "message": "todo created succesfully",
            "todo": new_todo.to_json(),
        }

