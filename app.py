from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def H_index(citations): 
      
    # sorting in ascending order 
    citations.sort() 
      
    # iterating over the list 
    for i, cited in enumerate(citations): 
          
        # finding current result 
        result = len(citations) - i 
          
        # if result is less than or equal 
        # to cited then return result 
        if result <= cited: 
            return result 
           
    return 0



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tindex = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.name


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = User(name=name)
        
        import subprocess
        subprocess.run(["twint" , "-u", name, "-o", name, "--json"])
        
        tweets = []
        likes_per_tweet = []
        for line in open('twint/' + name + '/tweets.json', 'r'):
            tweets.append(json.loads(line))
            likes_per_tweet.append(json.loads(line)['likes_count'])
        new_stuff.tindex = H_index(likes_per_tweet)

        
        
        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        users = User.query.order_by(User.created_at).all()
        return render_template('index.html', users=users)


@app.route('/delete/<int:id>')
def delete(id):
    User = User.query.get_or_404(id)

    try:
        db.session.delete(User)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    User = User.query.get_or_404(id)

    if request.method == 'POST':
        User.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, User=User)


if __name__ == '__main__':
    app.run(debug=True)
