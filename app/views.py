from app import app, models, forms
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
        if request.form['type'] == "filter":
            ellist =""
            with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:

                ellist = db.session.query(models.Income)
                filterPeriods = {'d': timedelta(days=1), 'y': timedelta(days=365), 'm': timedelta(days=30), 'w': timedelta(days=7)}
                requestedAcc = request.form['account']
                if requestedAcc != "":
                    ellist = ellist.filter_by(account = requestedAcc)
                requestedPer = request.form['period']
                if requestedPer != "":
                    ellist = ellist.filter(models.Income.date >= date.today() - filterPeriods[requestedPer])
                requestedSource = request.form['source']
                if requestedSource != "":
                    ellist = ellist.filter_by(source=requestedSource)

            print(ellist)
            return render_template("incomeSection.html", list=ellist)

        if request.form['type'] == "delete":
            with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                requested = request.form['id']
                db.session.query(models.Income).filter(models.Income.id == requested).delete()

            ellist = models.Income.query.all()
            print(ellist)
            return render_template("incomeSection.html", list=ellist, error=False)

        if request.form['type'] == "add":
            form = forms.AddIncome(request.form)
            if not (form['name'].data!='' and form['account'].data!='' and form['sum'].data!=''):
                ellist = models.Income.query.all()
                return render_template("incomeSection.html", list=ellist, error=True)

            else:
                with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                    newItem = models.Income(name=request.form['name'], tag=request.form['tag'],
                                            account=request.form['account'], sum=request.form['sum'],
                                            source = request.form['source'],
                                            date=date(*(int(i) for i in request.form['date'].split("-"))))
                    db.session.add(newItem)

                ellist = models.Income.query.all()
                return render_template("incomeSection.html", list=ellist)

        if request.form['type'] == "edit":
            form = forms.ChangeIncome(request.form)

            with SQLAlchemyDBConnection(SQLALCHEMY_DATABASE_URI) as db:
                requested = request.form['id']
                element = db.session.query(models.Income).filter(models.Income.id == requested).first()
                if request.form['name'] != "": element.name = request.form['name']
                if request.form['tag'] != "": element.tag = request.form['tag']
                if request.form['account'] != "": element.account = request.form['account']
                if request.form['date'] != "": element.date = date(*(int(i) for i in request.form['date'].split("-")))
                if request.form['sum'] != "": element.sum = (request.form['sum'])
                if request.form['source'] != "": element.category = request.form['source']

            ellist = models.Income.query.all()
            return render_template("incomeSection.html", list=ellist, error=False)

    print(request)
    ellist = models.Income.query.all()
    print(ellist)
    return render_template("index.html", title="home", list=ellist, form=forms.AddIncome(),
                           editForm = forms.ChangeIncome(), filterform=forms.FilterForm())
