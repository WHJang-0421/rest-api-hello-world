from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

# instance of flask
app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate.init_app(app, db)

api = Api(app)

# model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.Float)

    def __repr__(self):
        return f"{self.first_name} - {self.last_name} - {self.gender} - {self.salary}"

# GET REQUEST: /
class GetEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {
                'ID': emp.id,
                'First Name': emp.first_name,
                'Last Name': emp.last_name,
                'Gender': emp.gender,
                'Salary': emp.salary
            }
            emp_list.append(emp_data)
        return {"Employees": emp_list}, 200

# POST REQUEST: /add
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(first_name=request.json['First Name'], last_name=request.json['Last Name'], gender=request.json['Gender'], salary=request.json['Salary'])
            db.session.add(emp)
            db.session.commit()
            # return a json response
            return make_response(jsonify({
                'ID': emp.id,
                'First Name': emp.first_name,
                'Last Name': emp.last_name,
                'Gender': emp.gender,
                'Salary': emp.salary
            }), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# UPDATE REQUEST: /update/?
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error': 'not found'}, 404
            else:
                emp.first_name = request.json['First Name']
                emp.last_name = request.json['Last Name']
                emp.gender = request.json['Gender']
                emp.salary = request.json['Salary']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# DELETE REQUEST: /delete/?
class DeleteEmployee(Resource):
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200

api.add_resource(GetEmployee, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

if __name__ == "__main__":
    app.run(debug=True)