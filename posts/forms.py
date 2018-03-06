from wtforms import Form, StringField, TextAreaField, SelectField


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
    tags = SelectField('Tag', choices=[])


class TagForm(Form):
    name = StringField('Name')


