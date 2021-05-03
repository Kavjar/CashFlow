from restful_api.models import *
from restful_api import session
from datetime import datetime

account1 = Account(id_account=1, sum=3000)
family1 = Family(id_family=11, surname="Karabin", budget="40000")
user1 = User(id_user=1, username="yarko", firstname="Yaroslav", lastname="Karabin", email="karabin.yar@gmail.com",
             password="yarkoliv", phone="+380678891189",
             Account=account1, Family=family1)
account2 = Account(id_account=2, sum=500)
family2 = Family(id_family=12, surname="Panto", budget="35000")
user2 = User(id_user=2, username="panto", firstname="Rostik", lastname="Panto", email="panto.ros@gmail.com",
             password="111", phone="+380998891189",
             Account=account2, Family=family2)
account3 = Account(id_account=3, sum=10000)
family3 = Family(id_family=13, surname="Leheza", budget="100000")
user3 = User(id_user=3, username="liz", firstname="Liza", lastname="Leheza", email="lizzzz@gmail.com",
             password="1526", phone="+380950915524",
             Account=account3, Family=family3)

account4 = Account(id_account=4, sum=2566)
user4 = User(id_user=4, username="bodya", firstname="Bogdan", lastname="Kostiv", email="bohdan@gmail.com",
             password="9999", phone="+380954565524",
             Account=account4, family_id=None)
account5 = Account(id_account=5, sum=1324)
user5 = User(id_user=5, username="sasha", firstname="Oleksandr", lastname="Vlasuk", email="sanya@gmail.com",
             password="0000", phone="+380891525524",
             Account=account5, family_id=None)
account6 = Account(id_account=6, sum=7815)
user6 = User(id_user=6, username="romashka", firstname="Roman", lastname="Zoro", email="romamama@gmail.com",
             password="1010", phone="+380688891144",
             Account=account6, family_id=None)
#
# session.add(account1)
# session.add(family1)
# session.add(user1)
#
# session.add(account2)
# session.add(family2)
# session.add(user2)
#
# session.add(account3)
# session.add(family3)
# session.add(user3)
#
# session.add(account4)
# session.add(user4)
#
# session.add(account5)
# session.add(user5)
#
# session.add(account6)
# session.add(user6)


finances1 = Finances(id_fin=1, item="scholarship", price=1000, date=datetime(year=2021, month=4, day=28),
                     account_id=1, status="income")
finances2 = Finances(id_fin=2, item="food", price=100, date=datetime(year=2021, month=4, day=28),
                     account_id=2, status="outcome")
finances3 = Finances(id_fin=3, item="scholarship", price=200, date=datetime(year=2021, month=4, day=28),
                     account_id=2, status="income")
finances4 = Finances(id_fin=4, item="food", price=200, date=datetime(year=2021, month=4, day=28),
                     account_id=2, status="outcome")
finances5 = Finances(id_fin=5, item="candies", price=1354, date=datetime(year=2021, month=4, day=28),
                     account_id=3, status="outcome")
finances6 = Finances(id_fin=6, item="entertainments", price=1354, date=datetime(year=2021, month=4, day=28),
                     account_id=4, status="outcome")
finances7 = Finances(id_fin=7, item="scholarship", price=1354, date=datetime(year=2021, month=4, day=28),
                     account_id=4, status="income")
finances8 = Finances(id_fin=8, item="salary", price=1354, date=datetime(year=2021, month =4, day=28),
                     account_id=5, status="income")
finances9 = Finances(id_fin=9, item="salary", price=1354, date=datetime(year=2021, month=4, day=28),
                     account_id=5, status="income")
finances10 = Finances(id_fin=10, item="utilities", price=1354, date=datetime(year=2021, month=4, day=28),
                      account_id=6, status="outcome")
finances11 = Finances(id_fin=11, item="utilities", price=1354, date=datetime(year=2021, month=4, day=28),
                      account_id=6, status="outcome")
finances12 = Finances(id_fin=12, item="utilities", price=1354, date=datetime(year=2021, month=4, day=28),
                      account_id=6, status="outcome")

session.add(finances1)
session.add(finances2)
session.add(finances3)
session.add(finances4)
session.add(finances5)
session.add(finances6)
session.add(finances7)
session.add(finances8)
session.add(finances9)
session.add(finances10)
session.add(finances11)
session.add(finances12)
session.commit()
