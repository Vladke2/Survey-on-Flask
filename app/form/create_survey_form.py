from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateSurveyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    question = TextAreaField('Question', validators=[DataRequired()])
    answer_one = StringField('Перший варіант відповіді', validators=[DataRequired()])
    answer_two = StringField('Другий варіант відповіді', validators=[DataRequired()])
    answer_tree = StringField("Третій варіант відповіді(Це поле не обов'язкове)", validators=[Length(min=0, max=140)])
    answer_four = StringField("Четвертий варіант відповіді(Це поле не обов'язкове)", validators=[Length(min=0, max=140)])
    answer_five = StringField("П'ятий варіант відповіді(Це поле не обов'язкове)", validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
