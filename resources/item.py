from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id."
    )
    @jwt_required()
    def get(self, name):
        #return {'item': next(filter(lambda x: x['name'] == name, items), None)}
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {"message": "item not found"}, 404


    def post(self, name):
        #if next(filter(lambda x: x['name'] == name, items), None) is not None:
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        #items.append(item)
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "INSERT INTO items VALUES (?,?)"
        #cursor.execute(query,(item['name'],item['price']))
        #connection.commit()
        #connection.close()
        try:
            item.save_to_db()
        except:
            return {"message":"an error occurred inserting an item."}, 500 #internal server error

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item has been deleted!'}

    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        #return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'item': [item.json() for item in ItemModel.query.all()]}
