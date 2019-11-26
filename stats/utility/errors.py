import functools

from flask import jsonify, request

'''
Constant value representing the endpoint. This has to be written with two
uppercase letter, eg. API Gateway -> AG)
'''
EP_CODE = 'SS'

'''
Dictionary with all errors related to this service and the
corresponding error messages and status_code
'''
EP_DICT = {
    '001': (404, 'User not found'),
}


def response(code):
    '''
    Standard for the error response.

    The code must be written as a three number code, call it xyz, as follows:
        x -> the number of the current blueprint
        y -> the number of the route of the current blueprint
        z -> the number of the error within the current route

    Returns:
        A json response ready to be sent via a Flask view
    '''
    status_code, message = EP_DICT[code]
    return jsonify({
        'code': f'E{EP_CODE}{code}',
        'message': message
    }), status_code
