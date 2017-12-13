import datetime
import BudgetControl


class Income(BudgetControl.db.Model):
    db = BudgetControl.db
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    name = db.Column(db.String(120))
#     tag = db.Column(db.String(120), db.ForeignKey('Tags.id').name)
#     date = db.Column(db.Date)
    account = db.Column(db.String(100), db.ForeignKey('Accounts.id').name)
#     source = db.Column(db.String(120), db.ForeignKey('Sources.id').name)
#     def __repr__(self):
#         return self.name + ": " + str(self.sum) + "from " + str(self.source)
#
#
class Accounts(BudgetControl.db.Model):
    db = BudgetControl.db
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
#
#
# class Tags(BudgetControl.db.Model):
#     db = BudgetControl.db
#     name = db.Column(db.String(120))
#     id = db.Column(db.Integer, primary_key=True)
#     def __repr__(self):
#         return "id: " + str(self.id) + ", name: " + self.name
#
#
# class Sources(BudgetControl.db.Model):
#     db = BudgetControl.db
#     name = db.Column(db.String(120))
#     id = db.Column(db.Integer, primary_key=True)