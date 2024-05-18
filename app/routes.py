from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from .models import session, User, Poll, SurveyResponses
from datetime import datetime
from app import app
from .form import EditProfileForm, CreateSurveyForm


@app.route('/')
def home():
    current_user_username = current_user.username
    surveys = session.query(Poll).all()
    return render_template('home.html', username=current_user_username, surveys=surveys)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        session.commit()


@app.route('/user/<username>')
@login_required
def user_profile(username):
    user = session.query(User).filter_by(username=username).first()
    if user is None:
        flash('No such user found', 'error')
        print('error')
        return redirect(url_for('home'))
    if not user == current_user:
        print('user is not current_user')
    name = user.username
    about_me = user.about_me
    last_seen = user.last_seen
    return render_template('profile.html', name=name, about_me=about_me, last_seen=last_seen, user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user_profile', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.route('/create_survey', methods=['GET', 'POST'])
@login_required
def create_survey():
    if not current_user.is_authenticated:
        flash("To get started, please register.")
        return redirect(url_for('home'))
    form = CreateSurveyForm()
    if form.validate_on_submit():
        new_survey = Poll(
            author=current_user.username,
            title=form.title.data,
            description=form.description.data,
            question=form.question.data,
            answer_one=form.answer_one.data,
            answer_two=form.answer_two.data,
            answer_tree=form.answer_tree.data,
            answer_four=form.answer_four.data,
            answer_five=form.answer_five.data,
        )
        try:
            session.add(new_survey)
            session.commit()
            flash('your survey has been saved', "success")
            return redirect(url_for("home"))
        except Exception as exc:
            return exc
        finally:
            session.close()
    return render_template('create_survey.html', form=form)


@app.route('/fill_survey/<id>', methods=['GET', 'POST'])
@login_required
def fill_survey(id):
    poll = session.query(Poll).filter_by(id=id).first()
    user = session.query(User).filter_by(id=current_user.id).first()
    
    class FillSurveyForm(FlaskForm):
        poll = session.query(Poll).filter_by(id=id).first()
        first_answer_options = RadioField(poll.question, choices=[poll.answer_one, poll.answer_two, poll.answer_tree,
                                                                  poll.answer_four, poll.answer_five],
                                          validators=[DataRequired()])
        submit = SubmitField('Submit')

    form = FillSurveyForm()

    if form.validate_on_submit():
        new_survey = SurveyResponses(
            survey_title=poll.title,
            question=poll.question,
            answer_options=f"First:{poll.answer_one}, Second:{poll.answer_two}, Third:{poll.answer_tree},\
                           Fourth:{poll.answer_four}, Fifth:{poll.answer_five}",
            user_response=form.first_answer_options.data,
            username=user.username,
            user_age=user.age
        )
        try:
            session.add(new_survey)
            session.commit()
            flash('your answer has been saved', "success")
            return redirect(url_for("home"))
        except Exception as exc:
            return exc
        finally:
            session.close()
    question = session.query(Poll).filter_by(id=id).first()
    return render_template('fill_survey.html', form=form, question=question.question)
