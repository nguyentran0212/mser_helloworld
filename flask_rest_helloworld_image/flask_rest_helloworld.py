#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 11:10:15 2017

@author: nguyentran

This is a sample of a RESTful API developed with flask_restful library
"""

from flask import Flask
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

# Internal data. This can be replaced with a database
TODOS = {"todo1" : {"task" : "learn Python"},
         "todo2" : {"task" : "learn RESTful API in Python"},
         "todo3" : {"task" : "learn to build RESTful microservice in Python"}
        }

# Check if data exists. Otherwise, respond with 404
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message = "Todo %s doesn't exist" % todo_id)

# Create a parser for form data submitted by clients via POST or PUT
parser = reqparse.RequestParser()
# Configure the parser to look for certain argument in the submitted data
# Submitted data can be considered a dictionary with argument : value pairs
# This is an argument
augument_task = "task"
# Indicate that this API expects an argument named task in the submitted data
# After parsing, we can be sure the given argument exists and the data is safe
parser.add_argument(augument_task)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}
    
# Todo resource
# Interaction with individual todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]
    
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        # Status 204 means the request is processed. No further content to return
        return '', 204
    
    def put(self, todo_id):
        # invoke the created parser on the request object
        # the return is a dictionary
        args = parser.parse_args()
        task = {augument_task : args[augument_task]}
        TODOS[todo_id] = task
        # Status 201 means the request is fulfiled, and a new resource has been created
        return task, 201
    
# Todos resource (i.e., represent a list of todo items)
# Interaction with a list of todo items
class Todos(Resource):
    def get(self):
        return TODOS
    
    def post(self):
        # parse the request object to get "task" data
        args = parser.parse_args()
        # Find the largest ID number in the existing list of todos
        # This can be replaced by invoking database
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = "todo%i" % todo_id
        TODOS[todo_id] = {'task' : args['task']}
        return TODOS[todo_id], 201
    
# Connect resources to URL endpoints
api.add_resource(HelloWorld, '/')
api.add_resource(Todo, "/todos/<todo_id>")
api.add_resource(Todos, "/todos")

if __name__ == "__main__":
    # It is CRITICAL to attach the server to the address 0.0.0.0 instead of the localhost. Otherwise, it cannot be accessed from the outside of a container
    app.run(debug=True, host="0.0.0.0")