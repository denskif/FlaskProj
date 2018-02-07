from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')


class TagForm(Form):
    name = StringField('Name')
