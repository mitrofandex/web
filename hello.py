def app(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [bytes(x + '\n', 'ascii') for x in env['QUERY_STRING'].split('&')]
