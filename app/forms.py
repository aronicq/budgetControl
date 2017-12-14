from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length
from wtforms.fields.html5 import DateField
from app.models import Tags, Accounts, Sources, WasteTags, Category, Currency


class AddIncome(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(max=120)])
    tag = SelectField('tag', choices=[(i.id, i.name) for i in Tags.query.all()])
    date = DateField('entrydate', format='%Y-%m-%d')
    account = SelectField('account', validators=[InputRequired()], choices=[(i.id, i.name) for i in Accounts.query.all()])
    sum = StringField('sum', validators=[InputRequired()])
    source = SelectField('source', choices=[(i.id, i.name) for i in Sources.query.all()])
    currency = SelectField('currency', choices=[(i.id, i.name) for i in Currency.query.all()])


class ChangeIncome(FlaskForm):
    name = StringField('name', validators=[Length(max=120)])
    tag = SelectField('tag', choices=[(i.id, i.name) for i in Tags.query.all()])
    date = DateField('entrydate', format='%Y-%m-%d')
    account = SelectField('account', choices=[(i.id, i.name) for i in Accounts.query.all()])
    sum = StringField('sum')
    source = SelectField('source', choices=[(i.id, i.name) for i in Sources.query.all()])
    currency = SelectField('currency', choices=[(i.id, i.name) for i in Currency.query.all()])


class FilterForm(FlaskForm):
    period = SelectField('period', choices=[("", ""), ('d', 'day'), ('w', 'week'), ('m','month'), ('y','year')])
    account = SelectField('account', choices=[("", "")] + [(i.id, i.name) for i in Accounts.query.all()])
    source = SelectField('source', choices=[(i.id, i.name) for i in Sources.query.all()])


class AddWaste(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(max=120)])
    tag = SelectField('tag', choices=[(i.id, i.name) for i in WasteTags.query.all()])
    date = DateField('entrydate', format='%Y-%m-%d')
    account = SelectField('account', validators=[InputRequired()],
                          choices=[(i.id, i.name) for i in Accounts.query.all()])
    sum = StringField('sum', validators=[InputRequired()])
    category = SelectField('category', choices=[(i.id, i.category) for i in Category.query.all()])
    currency = SelectField('currency', choices=[(i.id, i.name) for i in Currency.query.all()])


class ChangeWaste(FlaskForm):
    name = StringField('name', validators=[Length(max=120)])
    tag = SelectField('tag', choices=[(i.id, i.name) for i in WasteTags.query.all()])
    date = DateField('entrydate', format='%Y-%m-%d')
    account = SelectField('account', choices=[(i.id, i.name) for i in Accounts.query.all()])
    sum = StringField('sum')
    category = SelectField('category', choices=[(i.id, i.category) for i in Category.query.all()])


class WasteFilterForm(FlaskForm):
    period = SelectField('period', choices=[("", ""), ('d', 'day'), ('w', 'week'), ('m','month'), ('y','year')])
    account = SelectField('account', choices=[("", "")] + [(i.id, i.name) for i in Accounts.query.all()])
    category = SelectField('category', choices=[(i.id, i.category) for i in Category.query.all()])


class ChangeAccount(FlaskForm):
    name = StringField('name')
    balance = StringField('balance')
    currency = SelectField('currency', choices=[(i.id, i.name) for i in Accounts.query.all()])


class AddAccount(FlaskForm):
    name = StringField('name')
    balance = StringField('balance')
    choices = [("", "")] + [(i.id, i.name) for i in Accounts.query.all()]