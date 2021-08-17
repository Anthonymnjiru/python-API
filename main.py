from flask import Flask,request, jsonify, session, json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///mydb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Products(db.Model) :
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,unique=True)
    description=db.Column(db.String(400))
    price=db.Column(db.Float)
    quantity=db.Column(db.Integer)

    def __init__(self,name,description,price,quantity):
        self.name=name
        self.description=description
        self.price=price
        self.quantity=quantity

class ProductsSchema(ma.Schema):
    class Meta:
        fields=('id','name','description','price')
        
product_schema=ProductsSchema()
products_schema=ProductsSchema(many=True)

#this line creates a database with all tables, you can comment after first run
db.create_all()

@app.route('/')
def home():

    return {'status':'running'}

@app.route("/addproduct",methods=['POST'])
def  addproduct():
    try:
        name=request.json['name']
        price=request.json['price']
        qty=request.json['qty']
        desc=request.json['description']
        
        newproduct=Products(name,desc,price,qty)
        db.session.add(newproduct)
        db.session.commit()

        return {"feedback": "success"}

    except:
         return {"feedback": "failed"}

@app.route('/alldata')
def alldata():
    products=Products.query.all()
    products=products_schema.dump(products)

    return products_schema.jsonify(products)

@app.route('/getitem/<name>')
def getitem(name):
    try:
        item=Products.query.filter_by(name=name).first()
        
        item=product_schema.dump(item)

        return product_schema.jsonify(item)
    
    except:
        return {"feedback":"error searching "}

#get all names and return them in a array
@app.route('/names',methods=['POST','GET'])
def names():
    names=[product.name for product in Products.query.all()]
    
    return {'names':names}

@app.route('/specifics')
def specifics():
    items=Products.query.filter_by(name='rice').all()
        
    items=products_schema.dump(items)

    return products_schema.jsonify(items)

#this route queries for all products in the table and manipulates data by doing arithimetic operations
@app.route('/operations')
def operations():
    items=Products.query.filter_by(quantity=30).all() 
    id=[i.id for i in items] 
    names=[i.name for i in items]
    descriptions=[i.description for i in items]
    prices=[i.price for i in items]
    quantities=[i.quantity for i in items]
    for i in range(len(id)):
        update=Products.query.filter_by(id=id[i]).first() #gets each row by id
        
        update.price=prices[i]/2 #updates the price value  by dividing by 2
       
        db.session.commit() #make changes to the database

    return {'id':id,"names":names,"prices":prices}


@app.errorhandler(404)
def not_found(error):
    return {"feedback":"404"}

if __name__=="__main__":
    app.run(debug=True)