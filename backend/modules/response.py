import json

from flask import Response as _response

from modules.server_response_statuses import SUCCESS
_JSON_CONTENT_TYPE = 'application/json'

def Response(data={}, status_code=SUCCESS, status_text=''):
    response = _response()
    response.content_type = _JSON_CONTENT_TYPE
    try:
        if status_text:
            data['status_text'] = status_text
    except TypeError as error:
        # TODO(Mike): Log out that this doesn't work because data does not support item assignment. Maybe figure out another
        # way to massage the error in, in these events?
        print('Unable to insert status_text into data')
        print(error, status_text)
    try:
        data['status_code'] = status_code
    except TypeError as error:
        print('Unable to insert status_code into data')
        print(error, status_code)
    try:
        response.data = json.dumps(data)
    except Exception as exception:
        response.data = data
    response.status_code = status_code


    return response
