import datetime
from unittest.case import TestCase

from discord import user
from databridge import *
import unittest
import random
from datetime import datetime

userbridge = userBridge()
itembridge = itemBridge()

def generateRandomNumber():
    return int(random.uniform(1,10000000))

def create_test():
    return User(
        username = str(generateRandomNumber()),
        balance = generateRandomNumber(),
        last_dropdate = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    )

class TestUser(unittest.TestCase):
    def test_add(self):
        user = create_test()
        session = Session()
        session.add(user)
        session.commit()
        print(f"username: {user.username} || balance: {user.balance} || {user.last_dropdate}")
        self.assertEqual(user.username, (session.query(User).filter_by(username = user.username).first()).username)
        return(user, session)
    
    def test_update(self):
        user, session = self.test_add()
        newUserName = str(generateRandomNumber())
        user.username = newUserName
        session.commit()
        print(f"Updated the username: {user.username}")
        self.assertEqual(newUserName, (session.query(User).filter_by(username = newUserName).first()).username)

    def test_delete(self):
        user, session = self.test_add()
        username = user.username
        session.delete(user)
        session.commit()
        self.assertEqual(0, session.query(User).filter_by(username = username).count())
    
if __name__ == '__main__':
    unittest.main()