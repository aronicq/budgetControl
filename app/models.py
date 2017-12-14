from app import db


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    name = db.Column(db.String(120))
    tag = db.Column(db.String(120), db.ForeignKey('Tags.id').name)
    date = db.Column(db.Date)
    account = db.Column(db.String(100), db.ForeignKey('Accounts.id').name)
    source = db.Column(db.String(120), db.ForeignKey('Sources.id').name)
    currency = db.Column(db.String(10), db.ForeignKey('Currency.id').name)
    def __repr__(self):
        return self.name + ": " + str(self.sum) + " дата: " + str(self.date)


class Waste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Integer)
    name = db.Column(db.String(120))
    tag = db.Column(db.String(120), db.ForeignKey('WasteTags.id').name)
    date = db.Column(db.Date)
    account = db.Column(db.String(100), db.ForeignKey('Accounts.id').name)
    category = db.Column(db.String(120), db.ForeignKey('Category.id').name)
    currency = db.Column(db.String(10), db.ForeignKey('Currency.id').name)
    def __repr__(self):
        return self.name + ": " + str(self.sum) + " on " + str(self.date)


class WasteTags(db.Model):
    name = db.Column(db.String(120))
    id = db.Column(db.Integer, primary_key=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))


class Accounts(db.Model):
    name = db.Column(db.String(100))
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)

    def __repr__(self):
        return self.name + " " + str(self.balance)


class Tags(db.Model):
    name = db.Column(db.String(120))
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return "id: " + str(self.id) + ", name: " + self.name


class Sources(db.Model):
    name = db.Column(db.String(120))
    id = db.Column(db.Integer, primary_key=True)



class Currency(db.Model):
    name = db.Column(db.String(10))
    id = db.Column(db.Integer, primary_key=True)