from app import create_app

app, redis_client = create_app()

if __name__ == '__main__':
    app.run(debug=True)