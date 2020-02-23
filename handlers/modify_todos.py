""" Delete / Put handler resource """
import logging

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import TodoModel

logger = logging.getLogger()


class ModifyTodos(Resource):
    """ Modify Todo item """

    parser = reqparse.RequestParser()
    parser.add_argument("title", type=str, required=True, help="Field is required")
    parser.add_argument("desc", type=str, required=False, help="Field is required")
    parser.add_argument("status", type=bool, required=True, help="Field is required")

    @jwt_required
    def delete(self, todo_id: str):
        """ Create new todo item"""

        try:
            todo = TodoModel.find_by_id(todo_id)
            if not todo:
                return {"success": True, "message": "deleted_succesfully"}, 200

            todo.delete_from_db()
        except Exception as exception:
            logger.debug(
                f"Exception occured when deleting a todo with id: {todo_id}, {exception}",
            )
            return {"success": False, "message": "internal_error"}, 500

        return {"success": True, "message": "deleted_succesfully"}, 200

    @jwt_required
    def put(self, todo_id: str):
        """ modify existing todo item"""
        req_data = self.parser.parse_args()
        try:
            todo = TodoModel.find_by_id(todo_id)
            if not todo:
                todo = TodoModel(**req_data, owner=get_jwt_identity())
            else:
                todo.desc = req_data["desc"]
                todo.title = req_data["title"]
                todo.status = req_data["status"]

            todo.save_to_db()
            return {"success": True, "todo": todo.to_json()}, 200
        except Exception as exception:
            logger.error(
                f"Exception occured when modifying a todo with params: {req_data}, {exception}",
            )
            return {"sucess": False, "message": "internal_error"}, 500


##
##
## TODO1: ADD MODIFY ENDPOINT, ADD DELETE ALL (FOR USER) ENDPOINT
## TODO2: MOBILE CLIENT TO CONSUME THE API
## TODO3: PUSH ALL TO GIT
##
##
