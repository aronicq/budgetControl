# from flask_wtf import FlaskForm
# from wtforms import StringField, SelectField
# from wtforms.validators import InputRequired, Length
# from models import Tags, Accounts
# from wtforms.fields.html5 import DateField
#
#
# class AddIncome(FlaskForm):
#     name = StringField('name', validators=[InputRequired(), Length(max=120)])
#     tag = SelectField('tag', choices=[(i.id, i.name) for i in Tags.query.all()])
#     date = DateField('entrydate', format='%Y-%m-%d')
#     account = SelectField('account', validators=[InputRequired()], choices=[(i.id, i.name) for i in Accounts.query.all()])
#     sum = StringField('sum', validators=[InputRequired()])
#     source = StringField('source')
#
#
# class ChangeIncome(FlaskForm):
#     name = StringField('name', validators=[Length(max=120)])
#     tag = SelectField('tag', choices=[(i.id, i.name) for i in Tags.query.all()])
#     date = DateField('entrydate', format='%Y-%m-%d')
#     account = SelectField('account', choices=[(i.id, i.name) for i in Accounts.query.all()])
#     sum = StringField('sum')
#     source = StringField('source')
#
#
# class FilterForm(FlaskForm):
#     period = SelectField('period', choices=[("", ""), ('d', 'day'), ('w', 'week'), ('m','month'), ('y','year')])
#     account = SelectField('account', choices= [("", "")] + [(i.id, i.name) for i in Accounts.query.all()])
#     source = StringField('source')