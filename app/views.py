from app import app, models, forms
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.forms import AddAccount, ChangeAccount
from config import SQLALCHEMY_DATABASE_URI
from datetime import date, timedelta
from flask import Flask, request, render_template


class SQLAlchemyDBConnection(object):
    """SQLAlchemy database connection"""

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.session = None

    def __enter__(self):
        engine = create_engine(self.connection_string)
        Session = sessionmaker()
        self.session = Session(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.commit()
        self.session.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        tableName = {"income" : models.Income, "waste": models.Waste}

        if request.form['table'] == "acc":
            ellist=""
            if request.form['type'] == "add":
                form = forms.AddAccount(request.form)
                if not (form['name'].data != '' and form['balance'].data != ''):
                    ellist = models.Accounts.query.all()
                    return render_template("accountsSection.html", op=request.form['table'][:3], list=ellist,
                                           error=True)

                else:
                    with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                        newItem = ""
                        if request.form['table'] == 'acc':
                            newItem = models.Accounts(name=request.form['name'], balance=request.form['balance'])
                        db.session.add(newItem)

                    ellist = models.Accounts.query.all()
                    return render_template("accountsSection.html", list=ellist, op=request.form['table'][:3],
                                           error=False)

            if request.form['type'] == "edit":
                form = forms.ChangeAccount(request.form)

                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    requested = request.form['id']
                    element = db.session.query(models.Accounts).filter(models.Accounts.id == requested).first()
                    if request.form['name'] != "": element.name = request.form['name']
                    if request.form['balance'] != "": element.balance = request.form['balance']

                ellist = models.Accounts.query.all()
                return render_template("accountsSection.html", list=ellist, op=request.form['table'][:3], error=False)

            if request.form['type'] == "delete":
                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    requested = request.form['id']
                    db.session.query(models.Accounts).filter(models.Accounts.id == requested).delete()

                ellist = models.Accounts.query.all()
                print(ellist)
                return render_template("accountsSection.html", op=request.form['table'][:3], list=ellist)

        else:
            if request.form['type'] == "filter":
                ellist =""
                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    ellist = db.session.query(tableName[request.form['table']])
                    filterPeriods = {'d': timedelta(days=1), 'y': timedelta(days=365), 'm': timedelta(days=30), 'w': timedelta(days=7)}
                    requestedAcc = request.form['account']
                    if requestedAcc != "":
                        ellist = ellist.filter_by(account = requestedAcc)
                    requestedPer = request.form['period']
                    if requestedPer != "":
                        ellist = ellist.filter(tableName[request.form['table']].date >= date.today() - filterPeriods[requestedPer])

                    if request.form['table'] == 'income':
                        requestedSource = request.form['source']
                        if requestedSource != "":
                            ellist = ellist.filter_by(source=requestedSource)
                    if request.form['table'] == 'waste':
                        requestedCategory = request.form['category']
                        if requestedCategory != "":
                            ellist = ellist.filter_by(category=requestedCategory)

                print(ellist)
                return render_template("incomeSection.html", op=request.form['table'][:3], list=ellist)

            if request.form['type'] == "delete":
                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    requested = request.form['id']
                    value = db.session.query(tableName[request.form['table']]).filter(tableName[request.form['table']].id == requested).first()
                    db.session.query(tableName[request.form['table']]).filter(tableName[request.form['table']].id == requested).delete()
                    if request.form['table'] == "waste":
                        element = db.session.query(models.Accounts).filter(
                            models.Accounts.id == request.form['account']).first()
                        element.balance += int(value.sum)
                    if request.form['table'] == "income":
                        element = db.session.query(models.Accounts).filter(
                            models.Accounts.id == request.form['account']).first()
                        element.balance -= int(value.sum)

                ellist = tableName[request.form['table']].query.all()
                print(ellist)
                return render_template("incomeSection.html", op=request.form['table'][:3], list=ellist)

            if request.form['type'] == "add":
                form = forms.AddIncome(request.form)
                if not (form['name'].data!='' and form['account'].data!='' and form['sum'].data!=''):
                    ellist = tableName[request.form['table']].query.all()
                    return render_template("incomeSection.html", op=request.form['table'][:3], list=ellist, error=True)

                else:
                    with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                        newItem=""
                        if request.form['table'] == 'income':
                            newItem = models.Income(name=request.form['name'], tag=request.form['tag'],
                                                    account=request.form['account'], sum=request.form['sum'],
                                                    source=request.form['source'], currency=request.form['currency'],
                                                    date=date(*(int(i) for i in request.form['date'].split("-"))))
                            element = db.session.query(models.Accounts).filter(
                                models.Accounts.id == request.form['account']).first()
                            element.balance += int(request.form['sum'])

                        if request.form['table'] == 'waste':
                            newItem = models.Waste(name=request.form['name'], tag=request.form['tag'],
                                                    account=request.form['account'], sum=request.form['sum'],
                                                    category=request.form['category'], currency=request.form['currency'],
                                                    date=date(*(int(i) for i in request.form['date'].split("-"))))
                            element = db.session.query(models.Accounts).filter(
                                models.Accounts.id == request.form['account']).first()
                            element.balance -= int(request.form['sum'])

                        db.session.add(newItem)

                    ellist = tableName[request.form['table']].query.all()
                    return render_template("incomeSection.html", list=ellist, op=request.form['table'][:3], error=False)


            if request.form['type'] == "edit":
                form = forms.ChangeIncome(request.form)

                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    requested = request.form['id']
                    element = db.session.query(tableName[request.form['table']]).filter(tableName[request.form['table']].id == requested).first()
                    if request.form['name'] != "": element.name = request.form['name']
                    if request.form['tag'] != "": element.tag = request.form['tag']
                    if request.form['account'] != "": element.account = request.form['account']
                    if request.form['date'] != "": element.date = date(*(int(i) for i in request.form['date'].split("-")))
                    if request.form['sum'] != "": element.sum = (request.form['sum'])
                    if request.form['currency'] != "": element.currency = request.form['currency']
                    if request.form['table'] == 'income':
                        if request.form['source'] != "": element.source = request.form['source']
                        if request.form['sum'] != "":
                            requested = request.form['id']
                            value = db.session.query(tableName[request.form['table']]).filter(
                                tableName[request.form['table']].id == requested).first()

                            element = db.session.query(models.Accounts).filter(
                                models.Accounts.id == request.form['account']).first()
                            element.balance = -(request.form['sum']) + int(value.sum)

                    if request.form['table'] == 'waste':
                        if request.form['category'] != "": element.category = request.form['category']
                        if request.form['sum'] != "":
                            requested = request.form['id']
                            value = db.session.query(tableName[request.form['table']]).filter(
                                tableName[request.form['table']].id == requested).first()

                            element = db.session.query(models.Accounts).filter(
                                models.Accounts.id == request.form['account']).first()
                            element.balance = int(request.form['sum']) - int(value.sum)




                ellist = tableName[request.form['table']].query.all()
                return render_template("incomeSection.html", list=ellist, op=request.form['table'][:3], error=False)

    print(request)
    ellistI = models.Income.query.all()
    ellistW = models.Waste.query.all()
    accList = models.Accounts.query.all()
    return render_template("index.html", title="home", addAccForm=AddAccount(), editAccForm=ChangeAccount(), acc=accList, listWas=ellistW, listInc=ellistI, addIncForm=forms.AddIncome(),
                           editIncForm=forms.ChangeIncome(), filterIncForm=forms.FilterForm(),
                           addWasForm=forms.AddWaste(), editWasForm=forms.ChangeWaste(), filterWasForm=forms.WasteFilterForm())
