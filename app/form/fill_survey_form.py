from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from ..models import session, Poll
from wtforms.validators import DataRequired


class FillSurveyForm(FlaskForm):
  #this method is not very reliable
    with open('survey_id.txt', 'r') as s_id:
        id = s_id.read()
        t_id = id[3:]
    poll = session.query(Poll).filter_by(id=t_id).first()
    first_answer_options = RadioField(poll.question, choices=[poll.answer_one, poll.answer_two, poll.answer_tree,
                                      poll.answer_four, poll.answer_five], validators=[DataRequired()])
    submit = SubmitField('Submit')
