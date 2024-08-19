from flask import Flask, render_template, request, jsonify
import os, re, datetime
import database as db
from models import Food 


app = Flask(__name__)

# create the database and table. Insert 10 test foods into db
# Do this only once to avoid inserting the test foods into 
# the db multiple times
if not os.path.isfile('foods.db'):
    db.connect()

# route for landing page
# check out the template folder for the index.html file
# check out the static folder for css and js files
@app.route("/")
def index():
    return render_template("index.html")

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    name = req_data['name']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['name'] == name:
            return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Food with name {name} is already in kitchen!',
                'status': '404'
            })

    bk = Food(db.getNewId(), True, name, datetime.datetime.now())
    print('new food: ', bk.serialize())
    db.insert(bk)
    new_bks = [b.serialize() for b in db.view()]
    print('foods in lib: ', new_bks)
    
    return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': 'Success creating a new food!👍😀'
            })


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    bks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in bks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all foods in kitchen!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Food with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting all foods in kitchen!👍😀',
                    'no_of_foods': len(bks)
                })


@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    bks = [b.serialize() for b in db.view()]
    if req_args:
        for b in bks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting food by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! Food with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': bks,
                    'status': '200',
                    'msg': 'Success getting food by ID!👍😀',
                    'no_of_foods': len(bks)
                })

@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    name = req_data['name']
    the_id = req_data['id']
    bks = [b.serialize() for b in db.view()]
    for b in bks:
        if b['id'] == the_id:
            bk = Food(
                the_id, 
                name, 
                datetime.datetime.now()
            )
            print('new food: ', bk.serialize())
            db.update(bk)
            new_bks = [b.serialize() for b in db.view()]
            print('foods in lib: ', new_bks)
            return jsonify({
                # 'error': '',
                'res': bk.serialize(),
                'status': '200',
                'msg': f'Success updating the food named {name}!👍😀'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Failed to update Food with name: {name}!',
                'status': '404'
            })
    
    


@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    fds = [f.serialize() for f in db.view()]
    if req_args:
        for f in fds:
            if f['id'] == int(req_args['id']):
                db.delete(f['id'])
                updated_fds = [f.serialize() for f in db.view()]
                print('updated_fds: ', updated_fds)
                return jsonify({
                    'res': updated_fds,
                    'status': '200',
                    'msg': 'Success deleting food by ID!👍😀',
                    'no_of_foods': len(updated_fds)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No Food ID sent!",
            'res': '',
            'status': '404'
        })

if __name__ == '__main__':
    app.run()
