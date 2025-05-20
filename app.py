from flask import Flask, render_template, request, url_for, flash, redirect
from config import Config
from models import db, Contact
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Create tables manually inside an app context, no need for @app.before_first_request
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        flash('Your message has been sent!', 'success')
        
        # Redirect to 'thank_you' page with name as a parameter
        return redirect(url_for('thank_you', name=form.name.data, email=form.email.data, message=form.message.data))
    
    return render_template('contact.html', form=form)

@app.route('/thank-you/<name>')
def thank_you(name):
    name = request.args.get('name')
    email = request.args.get('email')
    message = request.args.get('message')
    
    return render_template('thank_you.html', name=name, email=email, message=message)

if __name__ == '__main__':
    app.run(debug=True)
