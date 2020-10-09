from model import * 

"""
Classes to connect the user data and item data to the discord application from a MySQL server
"""

class userBridge():
    def Add(self, obj):
        session = Session()
        try:
            user = User(
                username = obj['username'],
                balance = obj['balance'],
                last_dropdate = obj['dropDate']
            )
            session.add(user)
            session.commit()
        finally:
            session.close()

    def Update(self, obj):
        session = Session()
        try:
            user = session.query(User).filter(User.username == obj['username']).first()
            user.balance = obj['balance'],
            user.last_dropdate = obj['dropDate']
            session.commit()
        finally:
            session.close()

    def Get(self, username):
        session = Session()
        try:
            return(session.query(User).filter(User.username == username).first())
        finally:
            session.close()

class itemBridge():
    def Add(self, obj):
        session = Session()
        try:
            item = Item(
                name = obj['name'],
                quantity = obj['quantity'],
                price = obj['price'],
                owner = obj['owner']
            )
            session.add(item)
            session.commit()
        finally:
            session.close()

    def Update(self, name, quantity, price, username):
        session = Session()
        try:
            item = session.query(Item).filter(Item.name == name and Item.price == price and Item.owner == username).first()
            if(quantity == 0):
                session.delete(item)
            else:
                item.quantity = quantity
            session.commit()
        finally:
            session.close()

    def GetByUser(self,username):
        session = Session()
        try:
            return(session.query(Item).filter(Item.owner == username).all())
        finally:
            session.close()

    def GetByItemName(self,name):
        session = Session()
        try:
            return(session.query(Item).filter(Item.name.contains(name)).limit(20).all())
        finally:
            session.close()
    def GetByID(self, id):
        session = Session
        try: 
            return(session.query(Item).filter(Item.iid == id))
        finally:
            session.close()

