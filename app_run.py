from flask import Flask, render_template, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very hard to guess string'
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    session['number'] = random.randint(0, 1000)
    session['times'] = 10
    return render_template('index.html')


@app.route('/guess', methods=['GET', 'POST'])
def guess():
    times = session['times']
    result = session.get('number')
    form = Guess_number_from()
    if form.validate_on_submit():
        times -= 1
        session['times'] = times
        if times == 0:
            flash('你输了')
            return redirect(url_for('index'))
        answer = form.number.data
        if answer > result:
            flash('你猜的数字太大了！你还有{}次机会'.format(times))
        if answer < result:
            flash('你猜的数字太小啦！你还有{}次机会'.format(times))
        if answer == result:
            flash('恭喜你赢了')
            return redirect(url_for('index'))
        return redirect(url_for('guess'))
    return render_template('guess.html', form=form)


class Guess_number_from(FlaskForm):
    number = IntegerField('输入数字（0到1000): ', validators=[DataRequired('输入一个有效数字！'),
                                                        NumberRange(0, 1000, '请输入0到1000以内的数字！')])
    submit = SubmitField('提交')


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
