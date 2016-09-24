from store_app import create_app

app = create_app(config=ProductionConfig)

if __name__ == '__main__':
    app.run(port=8080)
