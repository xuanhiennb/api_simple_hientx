import json
import numpy as np
import math
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

file_pool_ids = 'poolIds.txt'

"""
@api {POST} /post-1 Create or Append a pool
@apiName Post-1
@apiGroup POINT 1
@apiDescription First POST endpoint receives a JSON in the form of a document with two fields: a pool-id (numeric) and a pool-values (array of values) and is meant to append (if pool already exists) or insert (new pool) the values to the appropriate pool (as per the id)

@apiHeader {key-value} [Content-Type=application/json] application/json

@apiBody {intNumber} poolId pool-id.
@apiBody {numbericArray} poolValues Array of values.

@apiSuccess {String} type "appended" or "inserted".
@apiSuccessExample {json} Success-Example
     HTTP/1.1 200 OK
     {
         "type": "inserted"
     }

@apiError (400 Invalid input) BadRequest Invalid input.
@apiErrorExample Response (example):
     HTTP/1.1 400 Bad Request
     {
       "message": "Invalid input"
     }

@apiError (500 Internal Server Error) InternalServerError The server encountered an internal error.
@apiErrorExample Response (example):
     HTTP/1.1 500 Internal Server Error
     {
       "Internal Server Error": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
     }

@apiSampleRequest off

"""

"""
@api {POST} /post-2 Query a pool
@apiName Post-2
@apiGroup POINT 2
@apiDescription Second POST is meant to query a pool, the two fields are pool-id (numeric) identifying the queried pool, and a quantile (in percentile form)

@apiHeader {key-value} [Content-Type=application/json] application/json

@apiBody {intNumber} poolId pool-id.
@apiBody {double} percentile percentile.

@apiSuccess {String} quantile The calculated quantile.
@apiSuccess {String} total_count The total count of elements in the pool.
@apiSuccessExample {json} Success-Example
     HTTP/1.1 200 OK
     {
         "quantile": -5, "total": 15
     }
     
@apiError (400 Invalid input) BadRequest Invalid input.
@apiErrorExample Response (example):
     HTTP/1.1 400 Bad Request
     {
       "message": "Invalid input"
     }

@apiError (500 Internal Server Error) InternalServerError The server encountered an internal error.
@apiErrorExample Response (example):
     HTTP/1.1 500 Internal Server Error
     {
       "Internal Server Error": "The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application."
     }

@apiSampleRequest off     
"""


@app.route("/post-1", methods=['POST'])
def post1():
    data = request.get_json()

    if not validate_input(data):
        return jsonify({
            'message': 'invalid input'
        })
    try:
        if not check_pool(data['poolId']):
            create(data)
            return jsonify({
                'type': 'inserted'
            })
        else:
            update(data['poolId'], data['poolValues'])
            return jsonify({
                'type': 'appended'
            })
    except:
        return jsonify({
            'message': 'error'
        })


@app.route("/post-2", methods=['POST'])
def post2():
    data = request.get_json()

    if not validate_input2(data):
        return jsonify({
            'message': 'invalid input'
        })
    try:
        if check_pool(data['poolId']):
            pool = get_pool(data['poolId'])
            quantile = calculate_quantile(pool['poolValues'], data['percentile'])
            return jsonify({
                    'quantile': quantile,
                    'total': len(pool['poolValues'])
                })
        else:
            return jsonify({
            'message': 'poolId not found'
        })
    except:
        return jsonify({
            'message': 'error'
        })

    


def get_pool(id):
    path = id_to_path(id)
    pools = load_data(path)
    return pools.get(str(id))



def load_data(path):
    if os.path.exists(path):
        with open(path, 'r') as file:
            data = file.read()
        if data == '':
            return None
        return json.loads(data)
    else:
        return None


def create(pool):
    path = id_to_path(pool['poolId'])
    data = load_data(path)
    add_pool_id(pool['poolId'])
    if data is None:
        data = {pool['poolId']: pool}
    else:
        data.update({pool['poolId']: pool})
    with open(path, "w+") as file:
        file.write(json.dumps(data))
    


def update(poolId, poolValues):
    path = id_to_path(poolId)
    data = load_data(path)
    pool = data.get(str(poolId))
    pool['poolValues'] += poolValues
    data[str(poolId)] = pool
    with open(path, "w") as file:
        json.dump(data, file)


def calculate_quantile(arr, percentile):
    size = len(arr)
    arr = sorted(arr)
    index = (size * percentile) / 100
    if percentile == 0:
        return arr[0]
    elif percentile == 100:
        return arr[-1]
    if index.is_integer():
        index = int(index)
        return (arr[index - 1] + arr[index]) / 2
    else:
        return arr[int(math.ceil(index)) - 1]


def check_pool(id):
    with open(file_pool_ids, 'r') as file:
        poolIds = file.read()
    if poolIds == '':
        return False
    else:
        ids = poolIds.strip().split('\n')
        if str(id) not in ids:
            return False
        else:
            return True


def add_pool_id(id):
    with open(file_pool_ids, "a+") as file:
        file.writelines(str(id) + '\n')


def id_to_path(id):
    name = 'data/' + str(id // 1000) + '.txt'
    return name


def validate_input(data):
    if 'poolId' not in data or 'poolValues' not in data:
        return False
    if any(isinstance(x, str) for x in data['poolValues']):
        return False
    if len(np.asarray(data['poolValues']).shape) != 1 or len(data['poolValues']) <1:
        return False
    if type(data['poolId']) is not int:
        return False
    if int(data['poolId']) < 0:
        return False
    return True

def validate_input2(data):
    if 'poolId' not in data or 'percentile' not in data:
        return False
    if data['percentile']<0 or data['percentile'] > 100:
        return False
    return True


if __name__ == '__main__':
    app.run(host='127.0.0.1', port = 5000)
