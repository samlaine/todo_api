""" Get todo route handler """

import logging
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import TodoModel

logger = logging.getLogger()


class GetTodos(Resource):
    """ Get todo related """

    parser = reqparse.RequestParser()

    parser.add_argument("title", type=str, required=True, help="missing field")
    parser.add_argument("desc", type=str, required=True, help="missing field")
    parser.add_argument("status", type=bool, required=True, help="missing field")

    @jwt_required
    def get(self):
        """get all todos linked to user"""

        try:
            user_id = get_jwt_identity()
            todos = [todo.to_json() for todo in TodoModel.find_by_user(user_id)] or []
        except Exception as exception:
            logger.debug(f"Exception fetching todos: {exception}")
            return {"success": False, "message": "internal_error"}, 500

        return {"success": True, "todos": todos}

