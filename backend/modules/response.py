import json
import logging

from flask import Response as _response

from modules.server_response_statuses import SUCCESS
_JSON_CONTENT_TYPE = 'application/json'

def Response(data={}, status_code=SUCCESS, status_text=''):
    logger = logging.getLogger('server')
    response = _response()
    response.content_type = _JSON_CONTENT_TYPE
    try:
        if status_text:
            data['status_text'] = status_text
    except TypeError as error:
        logger.log(logging.INFO, 'Unable to insert status_text into data')
        logger.log(logging.INFO, f'Error: {error} || Status: {status_text}')
    try:
        data['status_code'] = status_code
    except TypeError as error:
        logger.log(logging.INFO, 'Unable to insert status_text into data')
        logger.log(logging.INFO, f'Error: {error} || Status: {status_text}')
    try:
        response.data = json.dumps(data)
    except:
        response.data = data
    response.status_code = status_code


    return response
