from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import aws_controller

class Quiz(Resource):

    def get(self):
        category = request.args.get('category')
        temp = jsonify(aws_controller.get_items())
        return jsonify(aws_controller.get_items())

    def post(self):
        data = request.json
        question = data.get('question')
        incorrect_answers = data.get('incorrect_answers')
        correct_answer = data.get('correct_answer')
        category = data.get('category')

        # just ensure fields are present
        if not all([bool(question), bool(incorrect_answers), bool(correct_answer), bool(category)]):
            raise ValueError()

        temp = jsonify(aws_controller.create_quiz_question(
                question, incorrect_answers, correct_answer, category
            )
        )
        return temp.json


class Questions(Resource):

    def post(self):
        data = request.json
        questions = data.get('questions')
        if not type(questions) is list: 
            raise ValueError("questions not provided")

        # TODO add more validation
        return aws_controller.batch_create_questions(questions)


api.add_resource(Quiz, '/quiz')
api.add_resource(Questions, '/questions')

if __name__ == '__main__':
    app.run(port=8000, debug=True)