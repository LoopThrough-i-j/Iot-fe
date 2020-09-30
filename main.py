import fe


app = fe.create_app()

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    # This will prevent the need for a custom gist
    # to run main.py locally. The hack is right here
    app.run(host='127.0.0.1', port=8080)
