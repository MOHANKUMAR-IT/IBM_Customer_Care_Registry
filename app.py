from TCEDesk_Engine import create_app


app = create_app()

if __name__ == '__main__':
    # from livereload import Server
    # server = Server(app.wsgi_app)
    # print(['%s' % rule for rule in app.url_map.iter_rules()])
    # app.run(debug=True)
    # app.run(use_reloader=True)
    # app.run()
    from waitress import serve    
    serve(app, host="0.0.0.0", port=8080)
    # server.serve(host = '0.0.0.0',port=5000)
    