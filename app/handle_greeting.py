# test function for handling /test uri with request and response
def handle_greeting(request):
    # grab values from request object
    name = request['name']

    # initialize a response object
    response = {}
    
    # logic for sending response
    response['greeting'] = 'Hello, ' + name

    # return response object
    return response