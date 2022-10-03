'''
    This is API program
    It will dynamically generate responce of given argument
'''
import json
from flask import Flask, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class Home(Resource):
    '''This class is used as a home page'''

    def get(self):
        '''This method print welcome'''
        return "welcome to our API"

    def post(self):
        '''This method print post request data'''
        data = request.get_json()
        return {'you sent': data}


class Multi(Resource):
    '''This class give responce of given request'''

    def get(self, key_name):
        '''this function find data of given argument'''
        with open("./server_data/insecure.json", "r") as file:
            data = json.load(file)
        self.flag = 0
        for items in data:
            if items == key_name:
                self.flag = 1
                self.new_version = ((data[items])[0])["advisory"]
        if self.flag == 1:
            return key_name + " -- " + self.new_version
        else:
            str = "No vulnerability in " + key_name + " module"
            return str


api.add_resource(Home, "/", methods=['GET', 'POST'])
api.add_resource(Multi, '/<string:key_name>')


if __name__ == "__main__":
    app.run(debug=True)
