from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.notes import Note

note_bp = Blueprint("note", __name__)
note_api = Api(note_bp)


class NoteAPI(Resource):
    def get(self, id):
        note = db.session.query(note).get(id)
        if note:
            return note.to_dict()
        return {"message": "note not found"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True, type=str)
        args = parser.parse_args()

        note = Note(args["text"])
        try:
            db.session.add(note)
            db.session.commit()
            return note.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            note = db.session.query(Note).get(args["id"])
            if note:
                note.completed = True
                db.session.commit()
            else:
                return {"message": "note not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            note = db.session.query(Note).get(args["id"])
            if note:
                db.session.delete(note)
                db.session.commit()
                return note.to_dict()
            else:
                return {"message": "note not found"}, 404
        except Exception as e:
            db.session.rollback()
            return {"message": f"server error: {e}"}, 500


class TodoListAPI(Resource):
    def get(self):
        todos = db.session.query(Note).all()
        return [todo.to_dict() for note in note]


note_api.add_resource(noteAPI, "/note")
note_api.add_resource(noteListAPI, "/noteList")