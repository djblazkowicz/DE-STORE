import datetime
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import *
from sqlalchemy import text
from re import search

#Launch Flask application and database

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StoreModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Address = db.Column(db.String(100), nullable=False)
    manager = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Store(id = {self.id}, Address = {self.Address}, manager ={self.manager})"

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Points = db.Column(db.Integer)
    Email = db.Column(db.String(100), nullable=False)
    Mobile = db.Column(db.String(15), nullable=False)
    Active = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User(id = {self.id}, UserType = {self.UserType}, Name = {self.Name}, Points = {self.Points}, Email = {self.Email}, Mobile = {self.Mobile})"

class ArticleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(200), nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    Points = db.Column(db.Integer, nullable=True)
    Active = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Article(id = {self.id}, Name = {self.Name}, Description = {self.Description}, Price = {self.Price}, Points = {self.Points}, Active = {self.Active})"

class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Article = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.Integer, nullable=True)
    Store = db.Column(db.Integer, nullable=False)
    StockTransfer = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Item(id = {self.id}, Article= {self.Article}, Status = {self.Status}, Store = {self.Status}, WareHouseDelivery = {self.WareHouseDelivery})"

class ItemPurchaseModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PurchaseOrder = db.Column(db.Integer, nullable=False)
    Item = db.Column(db.Integer, nullable=False)

class PurchaseOrderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Integer, nullable=False)
    PaymentMethod = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.String(100), nullable=False)
    User = db.Column(db.Integer, nullable=False)

class DealModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Article = db.Column(db.Integer, nullable=False)
    Store = db.Column(db.Integer, nullable=True)
    DealType = db.Column(db.Integer, nullable=False)
    From = db.Column(db.DateTime, nullable=False)
    To = db.Column(db.DateTime, nullable=True)

class StockTransferModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    TransferReference = db.Column(db.Integer, nullable=False)
    Item = db.Column(db.Integer, nullable=False)
    StoreFrom = db.Column(db.Integer, nullable=True)
    StoreTo = db.Column(db.Integer, nullable=False)
    DeliveryDate = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"StockTransfer(id = {self.id}, TransferReference = {self.TransferReference}, Item = {self.Item}, StoreFrom = {self.StoreFrom}, StoreTo = {self.StoreTo}, DeliveryDate = {self.DeliveryDate})"

class BasketModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PurchaseOrder = db.Column(db.Integer, nullable=False)
    Item = db.Column(db.Integer, nullable=False)
    Price = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Basket(id = {self.id}, PurchaseOrder = {self.PurchaseOrder}, Item = {self.Item}, Price = {self.Price})"

db.create_all()

#ARGUMENT PARSERS for PUT REQUESTS

store_put_args = reqparse.RequestParser()
store_put_args.add_argument("id", type=int, help="Store ID number", required=True)
store_put_args.add_argument("Name", type=str, help="Store name", required=True)
store_put_args.add_argument("Address", type=str, help="Store Address", required=True)
store_put_args.add_argument("manager", type=int, help="Store Manager's User id", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("id", type=int, help="User's id number", required=True)
user_put_args.add_argument("UserType", type=int, help="User Type", required=True)
user_put_args.add_argument("Name", type=str, help="User Name", required=True)
user_put_args.add_argument("Points", type=int, help="The User's Loyalty Points balance", required=True)
user_put_args.add_argument("Email", type=str, help="The User's Email Address", required=True)
user_put_args.add_argument("Mobile", type=str, help="The User's Mobile Number", required=True)
user_put_args.add_argument("Active", type=int, help="is the account active or not", required=True)

item_put_args = reqparse.RequestParser()
item_put_args.add_argument("id", type=int, help="item id number", required=True)
item_put_args.add_argument("Article", type=int, help="item's article number", required=True)
item_put_args.add_argument("Status", type=int, help="Item's status", required=True)
item_put_args.add_argument("Store", type=int, help="Associated Store's id number", required=True)
item_put_args.add_argument("StockTransfer", type=int, help="Associated WareHouseDelivery id number", required=True)

article_put_args = reqparse.RequestParser()
article_put_args.add_argument("id", type=int, help="article id number", required=True)
article_put_args.add_argument("Name", type=str, help="article name", required=True)
article_put_args.add_argument("Description", type=str, help="Description", required=True)
article_put_args.add_argument("Price", type=int, help="price", required=True)
article_put_args.add_argument("Points", type=int, help="Points", required=True)
article_put_args.add_argument("Active", type=int, help="is the article active", required=True)

basket_put_args = reqparse.RequestParser()
#basket_put_args.add_argument("id", type=int, help="itempurchase id number", required=True)
basket_put_args.add_argument("PurchaseOrder", type=int, help="Associated PO id number", required=True)
basket_put_args.add_argument("Item", type=int, help="assopciated Item id number", required=True)
#basket_put_args.add_argument("Price", type=int, help="price of the item at time of checkout", required=True)

purchaseorder_put_args = reqparse.RequestParser()
#purchaseorder_put_args.add_argument("id", type=int, help="purchaseorder id number", required=True)
purchaseorder_put_args.add_argument("Status", type=int, help="purchaseorder Status", required=True)
purchaseorder_put_args.add_argument("PaymentMethod", type=int, help="purchaseorder PaymentMethod", required=True)
purchaseorder_put_args.add_argument("Date", type=str, help="purchaseorder date", required=True)
purchaseorder_put_args.add_argument("User", type=int, help="assoc user", required=True)

deal_put_args = reqparse.RequestParser()
deal_put_args.add_argument("id", type=int, help="Deal id number", required=True)
deal_put_args.add_argument("Article", type=int, help="Article id number", required=True)
deal_put_args.add_argument("Store", type=int, help="Store id number", required=True)
deal_put_args.add_argument("DealType", type=int, help="Deal type number", required=True)
deal_put_args.add_argument("From", type=datetime, help="deal start date", required=True)
deal_put_args.add_argument("To", type=datetime, help="deal end date", required=True)

stocktransfer_put_args = reqparse.RequestParser()
stocktransfer_put_args.add_argument("id", type=int, help="id number", required=True)
stocktransfer_put_args.add_argument("TransferReference", type=int, help="transfer reference number", required=True)
stocktransfer_put_args.add_argument("StoreFrom", type=int, help="Store id number", required=True)
stocktransfer_put_args.add_argument("StoreTo", type=int, help="Store id number", required=True)
stocktransfer_put_args.add_argument("DeliveryDate", type=datetime, help="warehousedelivery delivery date", required=True)


#ARGUMENT PARSERS FOR PATCH REQUESTS

store_patch_args = reqparse.RequestParser()
store_patch_args.add_argument("id", type=int, help="Deal id number", required=True)
store_patch_args.add_argument("Name", type=str, help="Store name")
store_patch_args.add_argument("Address", type=str, help="Store Address")
store_patch_args.add_argument("manager", type=int, help="Store Manager's User id")

user_patch_args = reqparse.RequestParser()
user_patch_args.add_argument("id", type=int, help="Deal id number", required=True)
user_patch_args.add_argument("UserType", type=int, help="User Type")
user_patch_args.add_argument("Name", type=str, help="User Name")
user_patch_args.add_argument("Points", type=int, help="The User's Loyalty Points balance")
user_patch_args.add_argument("Email", type=str, help="The User's Email Address")
user_patch_args.add_argument("Mobile", type=str, help="The User's Mobile Number")
user_patch_args.add_argument("Active", type=int, help="is the account active or not")

item_patch_args = reqparse.RequestParser()
item_patch_args.add_argument("Article", type=int, help="item's article number")
item_patch_args.add_argument("Status", type=int, help="Item's status")
item_patch_args.add_argument("Store", type=int, help="Associated Store's id number")
item_patch_args.add_argument("StockTransfer", type=int, help="Associated WareHouseDelivery id number")

article_patch_args = reqparse.RequestParser()
article_patch_args.add_argument("id", type=int, help="article id number", required=True)
article_patch_args.add_argument("Name", type=str, help="article name")
article_patch_args.add_argument("Description", type=str, help="Description")
article_patch_args.add_argument("Price", type=int, help="price")
article_patch_args.add_argument("Points", type=int, help="Points")
article_patch_args.add_argument("Active", type=int, help="is the article active")

basket_patch_args = reqparse.RequestParser()
basket_patch_args.add_argument("id", type=int, help="itempurchase id number", required=True)
basket_patch_args.add_argument("PurchaseOrder", type=int, help="Associated PO id number")
basket_patch_args.add_argument("Item", type=int, help="assopciated Item id number")
basket_patch_args.add_argument("Price", type=int, help="price of the item at time of checkout")

purchaseorder_patch_args = reqparse.RequestParser()
purchaseorder_patch_args.add_argument("Status", type=int, help="purchaseorder Status")
purchaseorder_patch_args.add_argument("PaymentMethod", type=int, help="purchaseorder PaymentMethod")
purchaseorder_patch_args.add_argument("Date", type=str, help="purchaseorder date")

deal_patch_args = reqparse.RequestParser()
deal_patch_args.add_argument("Article", type=int, help="Article id number")
deal_patch_args.add_argument("Store", type=int, help="Store id number")
deal_patch_args.add_argument("DealType", type=int, help="Deal type number")
deal_patch_args.add_argument("From", type=datetime, help="deal start date")
deal_patch_args.add_argument("To", type=datetime, help="deal end date")

stocktransfer_patch_args = reqparse.RequestParser()
stocktransfer_patch_args.add_argument("StoreFrom", type=int, help="Store id number")
stocktransfer_patch_args.add_argument("StoreTo", type=int, help="Store id number")
stocktransfer_patch_args.add_argument("DeliveryDate", type=datetime, help="warehousedelivery delivery date")


#SQLAPI ARGS
sqlapi_post_args = reqparse.RequestParser()
sqlapi_post_args.add_argument("SQL", type=str, help="SQL query", required=True)

#RESOURCE FIELDS FOR PARSING DATA

store_resource_fields = {
    'id' : fields.Integer,
    'Name' : fields.String,
    'Address' : fields.String,
    'manager' : fields.Integer
}

user_resource_fields = {
    'id' : fields.Integer,
    'UserType' : fields.Integer,
    'Name' : fields.String,
    'Points' : fields.Integer,
    'Email' : fields.String,
    'Mobile' : fields.String,
    'Active' : fields.Integer
}

item_resource_fields = {
    'id' : fields.Integer,
    'Article' : fields.Integer,
    'Status' : fields.String,
    'Store' : fields.Integer,
    'StockTransfer' : fields.Integer
}

article_resource_fields = {
    'id' : fields.Integer,
    'Name' : fields.String,
    'Description' : fields.String,
    'Price' : fields.Integer,
    'Points' : fields.Integer,
    'Active' : fields.Integer
}

basket_resource_fields = {
    'id' : fields.Integer,
    'PurchaseOrder' : fields.Integer,
    'Item' : fields.Integer
}

purchaseorder_resource_fields = {
    'id' : fields.Integer,
    'Status' : fields.Integer,
    'PaymentMethod' : fields.Integer,
    'Date' : fields.String,
    'User' : fields.Integer
}

deal_resource_fields = {
    'id' : fields.Integer,
    'Article' : fields.Integer,
    'Store' : fields.Integer,
    'DealType' : fields.Integer,
    'From' : fields.DateTime,
    'To' : fields.DateTime
}

stocktransfer_resource_fields = {
    'id' : fields.Integer,
    'TransferReference' : fields.Integer,
    'StoreFrom' : fields.Integer,
    'StoreTo' : fields.Integer,
    'DeliveryDate' : fields.DateTime
}

sqliteapi_resource_fields = {
    'SQL' : fields.String
}

#API CALLS

#STORE API
class StoreAPI(Resource):
    #ADD A STORE
    @marshal_with(store_resource_fields)
    def put(self):
        args = store_put_args.parse_args()
        id = int(args['id'])
        result = StoreModel.query.get(id)
        if result:
            abort(409)
        
        Store = StoreModel(id = args['id'], Name = args['Name'], Address = args['Address'], manager = args['manager'])
        db.session.add(Store)
        db.session.commit()
        return Store, 201
    #UPDATE A STORE
    @marshal_with(store_resource_fields)
    def patch(self):
        args = store_patch_args.parse_args()
        store_id = int(args['id'])
        Store = StoreModel.query.get(store_id)
        if not Store:
            abort(404)
        if args['Name']:
            Store.Name = args['Name']
        if args['Address']:
            Store.Address = args['Address']
        if args['manager']:
            Store.manager = args['manager']
        #db.session.add(Store)
        db.session.commit()
        return Store, 201

#USER API
class UserAPI(Resource):
    #ADD A User
    @marshal_with(user_resource_fields)
    def put(self):
        args = user_put_args.parse_args()
        id = int(args['id'])
        result = UserModel.query.get(id)
        if result:
            abort(409)
        
        User = UserModel(
            id = args['id'],
            UserType = args['UserType'],
            Name = args['Name'],
            Points = args['Points'],
            Email = args['Email'],
            Mobile = args['Mobile'],
            Active = args['Active']
        )
        db.session.add(User)
        db.session.commit()
        return User, 201

    #UPDATE A User
    @marshal_with(user_resource_fields)
    def patch(self):
        args = user_patch_args.parse_args()
        id = int(args['id'])
        User = UserModel.query.get(id)
        if not User:
            abort(404)
        for arg in args:
            if args['UserType']:
                User.UserType = args['UserType']
            if args['Name']:
                User.Name = args['Name']
            if args['Points']:
              User.Points = args['Points']
            if args['Email']:
                User.Email = args['Email']
            if args['Mobile']:
                User.Mobile = args['Mobile']
            if args['Active'] or args['Active'] == 0:
                User.Active = args['Active']
        
        db.session.commit()
        return User, 201


#ITEM API
class ItemAPI(Resource):
    #ADD
    @marshal_with(item_resource_fields)
    def put(self):
        args = item_put_args.parse_args()
        id = int(args['id'])
        result = ItemModel.query.get(id)
        if result:
            abort(409)
        
        Item = ItemModel(
                            id = args['id'],
                            Article = args['Article'],
                            Status = args['Status'],
                            Store = args['Store'],
                            StockTransfer = args['StockTransfer']
                            )

        db.session.add(Item)
        db.session.commit()

        return Item, 201

    #UPDATE
    @marshal_with(item_resource_fields)
    def patch(self):
        args = item_patch_args.parse_args()
        id = int(args['id'])
        Item = ItemModel.query.get(id)
        if not Item:
            abort(404)
        
        if args['Article']:
            Item.Article = args['Article']
        if args['Status']:
            Item.Status = args['Status']
        if args['Store']:
            Item.Store = args['Store']
        if args['WareHouseDelivery']:
            Item.WareHouseDelivery = args['WareHouseDelivery']

        db.session.commit()
        return Item, 201

#ARTICLE API
class ArticleAPI(Resource):
    #ADD A STORE
    @marshal_with(article_resource_fields)
    def put(self):
        args = article_put_args.parse_args()
        id = int(args['id'])
        result = ArticleModel.query.get(id)
        if result:
            abort(409)
        
        Article = ArticleModel(
                            id = args['id'],
                            Name = args['Name'],
                            Description = args['Description'],
                            Price = args['Price'],
                            Points = args['Points'],
                            Active = args['Active']
                            )

        db.session.add(Article)
        db.session.commit()

        return Article, 201

    #UPDATE AN ARTICLE
    @marshal_with(article_resource_fields)
    def patch(self):
        args = article_patch_args.parse_args()
        id = int(args['id'])
        Article = ArticleModel.query.get(id)
        if not Article:
            abort(404)
        
        if args['Name']:
            Article.Name = args['Name']
        if args['Description']:
            Article.Description = args['Description']
        if args['Price'] or args['Price'] == 0:
            Article.Price = args['Price']
        if args['Points'] or args['Price'] == 0:
            Article.Points = args['Points']
        if args['Active'] or args['Active'] == 0:
            Article.Active = args['Active']

        db.session.commit()
        return Article, 201

#BASKET API
class BasketAPI(Resource):
    #CREATE
    @marshal_with(basket_resource_fields)
    def put(self):
        args = basket_put_args.parse_args()
        #id = args['id']
        result = ItemPurchaseModel.query.order_by(ItemPurchaseModel.id).all()
        print(len(result))
        Id = len(result) + 1
        print("ID is: ", Id)
        Basket = ItemPurchaseModel(
            id = Id,
            PurchaseOrder = args['PurchaseOrder'],
            Item = args['Item']
        )

        db.session.add(Basket)
        db.session.commit()
        return Basket, 201

#PURCHASE ORDER API
class PurchaseOrderAPI(Resource):
    #CREATE
    @marshal_with(purchaseorder_resource_fields)
    def put(self):
        args = purchaseorder_put_args.parse_args()
        result = PurchaseOrderModel.query.order_by(PurchaseOrderModel.id).all()
        Id = len(result) + 1

        PO = PurchaseOrderModel(
            id = Id,
            Status = args['Status'],
            PaymentMethod = args['PaymentMethod'],
            Date = args['Date'],
            User = args['User']
        )

        db.session.add(PO)
        db.session.commit()
        return PO, 201
    #UPDATE
    @marshal_with(purchaseorder_resource_fields)
    def patch(self):
        args = purchaseorder_patch_args.parse_args()
        id = args['id']
        PO = PurchaseOrderModel.query.get(id)
        if not PO:
            abort(404)
        
        if args['Status']:
            PO.Status = args['Status']
        if args['PaymentMethod']:
            PO.PaymentMethod = args['PaymentMethod']

        db.session.commit()
        return PO, 201


#WAREHOUSE RESTOCK API
class StockTransferAPI(Resource):
    #CREATE
    @marshal_with(stocktransfer_resource_fields)
    def put(self):
        args = stocktransfer_put_args.parse_args()
        id = args['id']
        result = StockTransferModel.query.get(id)
        if result:
            abort(409)
        Delivery = StockTransferModel(
            id = args['id'],
            TransferReference = args['TransferReference'],
            StoreFrom = args['StoreFrom'],
            StoreTo = args['StoreTo'],
            DeliveryDate = args['DeliveryDate']
        )

        db.session.add(Delivery)
        db.session.commit()
        return Delivery, 201

#GET API CALLS
class GetStore(Resource):
    #GET A STORE - OR RETURN LIST OF STORES IF INPUT IS 0
    @marshal_with(store_resource_fields)
    def get(self, store_id):
        if store_id == 0:
           result = StoreModel.query.order_by(StoreModel.Address).all()
           return result
        else:
            result = StoreModel.query.get(store_id)
            result = [result]
            return result

class GetUser(Resource):
    #GET A USER - OR RETURN LIST OF USERS IF INPUT IS 0
    @marshal_with(user_resource_fields)
    def get(self, user_id):
        if user_id == 0:
            result = UserModel.query.order_by(UserModel.Name).all()
            return result
        else:
            result = UserModel.query.get(user_id)
            result = [result]
            return result

class GetArticle(Resource):
    #GET AN ARTICLE - OR RETURN LIST OF ARTICLES IF INPUT IS 0
    @marshal_with(article_resource_fields)
    def get(self, article_id):
        if article_id == 0:
            result = ArticleModel.query.order_by(ArticleModel.Name).all()
            return result
        else:
            result = UserModel.query.get(article_id)
            result = [result]
            return result

class GetItem(Resource):
    @marshal_with(item_resource_fields)
    def get(self, item_id):
        if item_id == 0:
            result = ItemModel.query.order_by(ItemModel.id).all()
            return result
        else:
            result = ItemModel.query.get(item_id)
            result = [result]
            return result

class GetPurchaseOrder(Resource):
    @marshal_with(purchaseorder_resource_fields)
    def get(self, item_id):
        if item_id == 0:
            result = PurchaseOrderModel.query.order_by(PurchaseOrderModel.id).all()
            return result
        else:
            result = PurchaseOrderModel.query.get(item_id)
            result = [result]
            return result

#SQLITE API
class SQLiteAPI(Resource):
    def post(self):
        args = sqlapi_post_args.parse_args()
        sql = text(args['SQL'])
        print(args['SQL'])
        result = db.engine.execute(sql)
        searching = "select" in args['SQL']
        print(searching)
        if searching:
            out = jsonify([dict(row) for row in result])
            return out
        if searching == False:
            return 200

#GET ENDPOINTs
api.add_resource(GetStore, "/GetStore/<int:store_id>")
api.add_resource(GetUser, "/GetUser/<int:user_id>")
api.add_resource(GetArticle, "/GetArticle/<int:article_id>")
api.add_resource(GetItem, "/GetItem/<int:item_id>")
api.add_resource(GetPurchaseOrder, "/GetPurchaseOrder/<int:item_id>")

#OTHER ENDPOINTS
api.add_resource(StoreAPI, "/StoreAPI")
api.add_resource(UserAPI, "/UserAPI")
api.add_resource(ArticleAPI, "/ArticleAPI")
api.add_resource(ItemAPI, "/ItemAPI")
api.add_resource(StockTransferAPI, "/StockTransferAPI")
api.add_resource(BasketAPI, "/BasketAPI")
api.add_resource(PurchaseOrderAPI, "/PurchaseOrderAPI")

api.add_resource(SQLiteAPI, "/SQLiteAPI")

if __name__ == "__main__":
    app.run(debug=True)