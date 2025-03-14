from app import app
@app.route('/product')
def product():
    return "product"