from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import aws_controller

class Quiz(Resource):

    def get(self):
        temp = jsonify(aws_controller.get_items())
        return jsonify(aws_controller.get_items())

    def post(self):
        data = request.json
        temp = jsonify(aws_controller.create_quiz_question())
        return temp.json


class Question(Resource):
    def get(self):

        temp = aws_controller.get_question('4c31b7744fd811ebb4b3acde48001122')
        print(temp['Items'][0]['questions'])
        return 


api.add_resource(Quiz, '/quiz')
api.add_resource(Question, '/question')

if __name__ == '__main__':
    app.run(port=8000, debug=True)