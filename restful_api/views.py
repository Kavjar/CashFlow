from flask import request, jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from restful_api import flask_app, session
from restful_api.models import User, Finances, Account, Family, Transaction

auth = HTTPBasicAuth()
with flask_app.app_context():
    Users = session.query(User).all()
    res = dict()
    for i in range(len(Users)):
        res[Users[i].username] = generate_password_hash(Users[i].password)
    users = jsonify(res)


@auth.verify_password
def verify_password(username, password):
    print(password)
    if username in res and check_password_hash(res.get(username), password):
        return username


# @flask_app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         if request.form["username"] == "" or request.form["password"] == "":
#             return jsonify({"message": "Invalid data"})
#         try:
#             temp = session.query(User).filter(User.username == request.form["username"]).first()
#             if temp.password == request.form["password"]:
#                 ss["username"] = request.form["username"]
#                 ss["password"] = request.form["password"]
#                 ss["id"] = temp.id
#                 return jsonify({"message": "Success"})
#         except Exception as e:
#             return jsonify({"message": "User not found"})
#         return jsonify({"message": "Access denied"})
#     return render_template("login_page.html")


@flask_app.route("/user/", methods=["POST"])
def create_user():
    username = request.json.get("username")
    firstname = request.json.get("firstname")
    lastname = request.json.get("lastname")
    email = request.json.get("email")
    password = request.json.get("password")
    phone = request.json.get("phone")

    user = session.query(User).filter_by(username=username).first()
    users = session.query(User).all()
    accounts = session.query(Account).all()

    if user and user.username == username:
        return jsonify(status="Current user is already exists"), 400
    if username and password and firstname and lastname and email and phone:
        created_acc = Account(id_account=len(accounts) + 1, sum=0)
        created_user = User(id_user=len(users) + 1, username=username, firstname=firstname, lastname=lastname,
                            email=email, password=password, phone=phone,
                            account_id=created_acc.id_account, family_id=None)
        session.add(created_acc)
        session.add(created_user)
        session.commit()
        result = {
            "data": {
                "id": created_user.id_user,
                "username": created_user.username,
                "firstname": created_user.firstname,
                "lastname": created_user.lastname,
                "email": created_user.email,
                "password": generate_password_hash(created_user.password),
                "phone": created_user.phone,
                "Account": {
                    "id": created_acc.id_account,
                    "sum": created_acc.sum
                }
            },
            "status": "Created"
        }
        res[username] = generate_password_hash(password)
        return jsonify(result), 201
    else:
        return jsonify(status="Bad data"), 400


@flask_app.route("/user/<id_>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def user_management(id_):
    user = session.query(User).filter_by(id_user=id_).first()
    if user is None:
        return jsonify(status="User not found"), 404
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status="Access denied"), 403
    account = session.query(Account).filter_by(id_account=user.account_id).first()
    if request.method == "GET":
        if user.family_id == -1:
            result = {
                "data": {
                    "id": user.id_user,
                    "username": user.username,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "password": generate_password_hash(user.password),
                    "phone": user.phone,
                    "Account": {
                        "id": account.id_account,
                        "sum": account.sum
                    }
                },
                "status": "current user"
            }
        else:
            result = {
                "data": {
                    "id": user.id_user,
                    "username": user.username,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "password": generate_password_hash(user.password),
                    "phone": user.phone,
                    "Account": {
                        "id": account.id_account,
                        "sum": account.sum
                    },
                    "family id": user.family_id
                },
                "status": "current user"
            }
        return jsonify(result), 200

    if request.method == "PUT":
        username = request.json.get("username")
        firstname = request.json.get("firstname")
        lastname = request.json.get("lastname")
        email = request.json.get("email")
        password = request.json.get("password")
        phone = request.json.get("phone")

        if username or password or firstname or lastname or email or phone:
            if username:
                user.username = username
            if lastname:
                user.lastname = lastname
            if firstname:
                user.firstname = firstname
            if email:
                user.email = email
            if password:
                user.password = password
                res[logged_user] = generate_password_hash(password)
            if phone:
                user.phone = phone

            session.query(User).filter_by(id_user=user.id_user).update(
                dict(username=user.username, firstname=user.firstname, lastname=user.lastname,
                     email=user.email, password=user.password, phone=user.phone))
            session.commit()
            if user.family_id == -1:
                result = {
                    "data": {
                        "id": user.id_user,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname,
                        "email": user.email,
                        "password": generate_password_hash(user.password),
                        "phone": user.phone
                    },
                    "status": "Updated"
                }
            else:
                result = {
                    "data": {
                        "id": user.id_user,
                        "username": user.username,
                        "firstname": user.firstname,
                        "lastname": user.lastname,
                        "email": user.email,
                        "password": generate_password_hash(user.password),
                        "phone": user.phone,
                        "family id": user.family_id
                    },
                    "status": "Updated"
                }

            return jsonify(result), 201
        else:
            return jsonify(status="Bad request"), 400

    if request.method == "DELETE":
        finances = session.query(Finances).all()
        for i in range(len(finances)):
            if finances[i].account_id == user.account_id:
                db_session1 = session.object_session(finances[i])
                db_session1.delete(finances[i])
                db_session1.commit()
        db_session1 = session.object_session(user)
        db_session1.delete(user)
        db_session1.commit()

        db_session2 = session.object_session(account)
        db_session2.delete(account)
        db_session2.commit()
        return jsonify(status="deleted"), 200


@flask_app.route("/family/", methods=["POST"])
def create_fam():
    surname = request.json.get("surname")

    families = session.query(Family).all()
    if surname:
        created_fam = Family(id_family=len(families) + 1, surname=surname, budget=0)
        session.add(created_fam)
        session.commit()
        result = {
            "data": {
                "id": created_fam.id_family,
                "surname": created_fam.surname,
                "budget": created_fam.budget,
            }
        }
        return jsonify(result), 201
    else:
        return jsonify(status="Bad data"), 400


@flask_app.route("/family/<id_>", methods=["GET", "PUT", "DELETE"])
@auth.login_required
def family__id(id_):
    logged_user = auth.current_user()

    family = session.query(Family).filter_by(id_family=id_).first()
    if family is None:
        return jsonify(status="Family not found"), 404

    users = session.query(User).filter(User.family_id == id_).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
    if k == len(users):
        return jsonify(status="Access denied"), 403
    result = {
        "data": {
            "id": family.id_family,
            "surname": family.surname,
            "budget": family.budget,
        }
    }
    if request.method == "GET":

        return jsonify(result), 200

    if request.method == "PUT":
        surname = request.json.get("surname")

        if surname:
            family.surname = surname
            session.query(Family).filter_by(id_family=family.id_family).update(
                dict(surname=family.surname))
            session.commit()
            return jsonify(status="Updated", id=family.id_family, surname=family.surname, budget=family.budget), 200
        else:
            return jsonify(status="Bad request"), 400

    if request.method == "DELETE":
        users = User.query.all()
        for i in range(len(users)):
            if users[i].family_id == int(id_):
                session.query(User).filter_by(id_user=users[i].id_user).update(
                    dict(family_id=-1))
                session.commit()
        transactions = Transaction.query.all()
        for i in range(len(transactions)):
            if transactions[i].family_id == int(id_):
                db_session1 = session.object_session(transactions[i])
                db_session1.delete(transactions[i])
                db_session1.commit()
        db_session2 = session.object_session(family)
        db_session2.delete(family)
        db_session2.commit()
        return jsonify(status="deleted"), 200


@flask_app.route("/family/<id_>/members/", methods=["GET"])
@auth.login_required
def get_family_members(id_):
    logged_user = auth.current_user()

    family = session.query(Family).filter_by(id_family=id_).first()
    if family is None:
        return jsonify(status="Family not found"), 404

    users = session.query(User).filter(User.family_id == id_).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
    if k == len(users):
        return jsonify(status="Access denied"), 403

    courses_list = []
    for cor in users:
        courses_list.append(User.get_users2(cor))
    if len(courses_list) == 0:
        return jsonify(status="There are no users in this family"), 404
    else:
        return jsonify(courses_list), 200


@flask_app.route("/transaction/<familyId>/<accountId>", methods=["POST"])
@auth.login_required
def make_transaction(familyId, accountId):
    family = session.query(Family).filter_by(id_family=familyId).first()
    account = session.query(Account).filter_by(id_account=accountId).first()
    if family is None:
        return jsonify(status="Family not found"), 404
    if account is None:
        return jsonify(status="User with this account id not found"), 404

    logged_user = auth.current_user()
    users = session.query(User).filter(User.family_id == familyId).all()
    cur_user, k = None, 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status="You are not a family member"), 403
    if cur_user.account_id != int(accountId):
        return jsonify(status="It is not your account"), 403

    transactions = session.query(Transaction).all()
    direction = request.json.get("direction")
    money = request.json.get("money")

    if direction != 1 and direction != 0:
        return jsonify(status="You can have only f->p or p->f direction"), 400
    if money > 0:
        if direction == 1 and family.budget > money:
            family.budget -= money
            account.sum += money
            session.query(Family).filter_by(id_family=family.id_family).update(
                dict(budget=family.budget))
            session.commit()
            session.query(Account).filter_by(id_account=account.id_account).update(
                dict(sum=account.sum))
            session.commit()
        elif direction == 0 and account.sum > money:
            family.budget += money
            account.sum -= money
            session.query(Family).filter_by(id_family=family.id_family).update(
                dict(budget=family.budget))
            session.query(Account).filter_by(id_account=account.id_account).update(
                dict(sum=account.sum))
            session.commit()
        else:
            return jsonify(status="Not enough money to make a transaction"), 400

        create_trans = Transaction(id_transaction=len(transactions) + 1, money=money,
                                   direction=direction, family_id=familyId, account_id=accountId)

        session.add(create_trans)
        session.commit()
        return jsonify(status="Transaction completed", id=create_trans.account_id, money=create_trans.money,
                direction=create_trans.direction, family_id=create_trans.family_id, account_id=create_trans.account_id), 200
    else:
        return jsonify(status="Bad request"), 400


@flask_app.route("/family/<familyId>/member/<userId>", methods=["PUT", "DELETE"])
@auth.login_required
def add_or_delete_member(familyId, userId):
    family = session.query(Family).filter_by(id_family=familyId).first()
    user = session.query(User).filter_by(id_user=userId).first()
    if family is None:
        return jsonify(status="Family not found"), 404
    if user is None:
        return jsonify(status="User not found"), 404

    logged_user = auth.current_user()
    users = session.query(User).filter(User.family_id == familyId).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status="You are not a family member"), 403

    if request.method == "PUT":
        if user.family_id == int(familyId):
            return jsonify(status="This user is already in the family"), 400
        else:
            session.query(User).filter_by(id_user=userId).update(
                dict(family_id=familyId))
            session.commit()
            return jsonify(status="User was added to the family"), 200
    else:
        if not user.family_id:
            return jsonify(status="This user does not belong to any family"), 400
        else:
            session.query(User).filter_by(id_user=userId).update(
                dict(family_id=None))
            session.commit()
            return jsonify(status="User was deleted from family")


@flask_app.route("/family/<familyId>/transactions", methods=["GET"])
@auth.login_required
def get_trans(familyId):
    family = session.query(Family).filter_by(id_family=familyId).first()
    if family is None:
        return jsonify(status="Family not found"), 404

    logged_user = auth.current_user()
    users = session.query(User).filter(User.family_id == familyId).all()
    k = 0
    for u in users:
        if u.username != logged_user:
            k += 1
        else:
            cur_user = u
    if k == len(users):
        return jsonify(status="You are not a family member"), 403

    fam_transactions = session.query(Transaction).filter(Transaction.family_id == familyId).all()
    transaction_list = []
    if not len(fam_transactions):
        return jsonify(status="This family has no transactions"), 404
    else:
        for trans in fam_transactions:
            transaction_list.append(Transaction.get_transaction(trans))
        return jsonify(transaction_list), 200


@flask_app.route("/user/account/<accountId>/transactions", methods=["GET"])
@auth.login_required
def getacc_trans(accountId):
    account = session.query(Account).filter_by(id_account=accountId).first()
    if account is None:
        return jsonify(status="Account not found"), 404

    user = session.query(User).filter_by(account_id=accountId).first()
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status="Access denied"), 403


    acc_transactions = session.query(Transaction).filter(Transaction.account_id == accountId).all()
    acc_finances = session.query(Finances).filter(Finances.account_id == accountId).all()
    transaction_list = []
    if not len(acc_transactions) and not len(acc_finances):
        return jsonify(status="This account have no transactions and finances"), 404
    else:
        for trans in acc_transactions:
            transaction_list.append(Transaction.get_transaction(trans))
        for trans in acc_finances:
            transaction_list.append(Finances.get_finances(trans))
        return jsonify(transaction_list), 200


@flask_app.route("/user/account/<accountId>/purchase", methods=["POST"])
@auth.login_required
def finan(accountId):
    account = session.query(Account).filter_by(id_account=accountId).first()
    if account is None:
        return jsonify(status="Account not found"), 404

    user = session.query(User).filter_by(account_id=accountId).first()
    logged_user = auth.current_user()
    if logged_user != user.username:
        return jsonify(status="Access denied"), 403

    finances = session.query(Finances).all()
    item = request.json.get("item")
    price = request.json.get("price")
    date = request.json.get("date")
    status = request.json.get("status")
    if status != "expenses" and status != "incomes":
        return jsonify(status="You can have only expenses or incomes status"), 400
    if item and price and date and status:
        if price < 0:
            return jsonify(status="Bad data"), 400
        created_fin = Finances(id_fin=len(finances) + 1, item=item, price=price, date=date, account_id=accountId, status=status)
        if status == "expenses":
            if price > account.sum:
                return jsonify(status="Not enough money"), 400
            account.sum -= price
        else:
            account.sum += price
        session.query(Account).filter_by(id_account=accountId).update(
            dict(sum=account.sum))
        session.add(created_fin)
        session.commit()
        result = {
            "Account": {
                "id": account.id_account,
                "sum": account.sum
            },
            "status": "OK"
        }
        return jsonify(result), 200
    else:
        return jsonify(status="Bad data"), 400


@flask_app.route("/users/", methods=["GET"])
# @auth.login_required(role="teacher")
def create_all_users():
    users = session.query(User).all()
    courses_list = []
    for cor in users:
        courses_list.append(User.get_users(cor))
    if len(courses_list) == 0:
        return jsonify(status="Users not found"), 404
    else:
        return jsonify(courses_list), 200
