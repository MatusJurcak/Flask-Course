from flask import Flask, request, redirect, url_for, render_template, flash
from forms import SignupForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

@app.route('/signup', methods=['GET','POST'])
def signup():
    # request.form will be empty on a GET request, but populated on a POST request since it will contain values that a user has entered
    form = SignupForm(request.form)
    # let's first see if it is a post request
    if request.method == 'POST':
        # now we can use the WTForms validate method to see if we have passed our validations for the form we created in forms.py. This method returns True or False
        if form.validate():
          # we will cover flash messages more, but they are a one time message that is displayed to the user of our application
          flash("You have succesfully signed up!")
          return redirect(url_for('welcome'))
    # if the method is a GET - or if form.validate() returns False, our form will contain a dictionary called errors which contain the error messages to display to the user
    return render_template('signup.html', form=form)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
