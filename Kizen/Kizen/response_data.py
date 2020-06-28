def json_data(data=None, status='success', message=''):
    return {
        'results': data,
        'status': status,
        'message': message,
    }
