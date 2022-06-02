from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate, migrate



app = Flask(__name__)
app.secret_key = 'mysecret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True




db = SQLAlchemy(app)
# migrate = Migrate(app, db)

class Tattoinv(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
 
    def __repr__(self):
        return f"name {self.name} lastname {self.price} age {self.amount}"
    

@app.route('/')
def index():
    tatt = Tattoinv.query.all()
    if "A" in session.values():
        session.pop("A", None)
        return render_template('index.htm', tatt = tatt, message = "Item added Successfully")
    elif "U" in session.values():
        session.pop("U", None)
        return render_template('index.htm', tatt = tatt, message = "Item updated Successfully")
    elif "D" in session.values():
        session.pop("D", None)
        return render_template('index.htm', tatt = tatt, message = "Item deleted Successfully")
    return render_template('index.htm', tatt=tatt)

@app.route('/add-inventory')
def add_data():
    return render_template('add_inv.htm')

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    price = request.form.get('price')
    amount = request.form.get('amount')
    if name != '' and price.isdigit() and amount.isdigit():
        tatt = Tattoinv(name=name, price=price, amount=amount)
        db.session.add(tatt)
        session["message"] = "A"
        return redirect('/')
    else:
        return render_template('add_inv.htm', error='Please enter valid data')


@app.route('/delete/<int:id>')
def clear_inventory(id):
    inv = Tattoinv.query.get(id)
    db.session.delete(inv)
    session["message"] = "D"
    return redirect('/')

@app.route('/update-inv')
def update_inv():
    return render_template('update_inv.htm')

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    if request.method == 'POST':
        tatto = Tattoinv.query.get(id)
        tatto.name = request.form.get('name')
        tatto.price = request.form.get('price')
        tatto.amount = request.form.get('amount')
        session["message"] = "U"
        return redirect('/')
    info = Tattoinv.query.get(id)
    name = info.name
    price = info.price
    amount = info.amount
    
    return render_template('update_inv.htm',id=id, name=name, price=price, amount=amount)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
 