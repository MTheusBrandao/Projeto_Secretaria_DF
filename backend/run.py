from app import criar_aplicacao

app = criar_aplicacao

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5000)