def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    from run import app

    if __name__ == "__main__":
       return  app.run()