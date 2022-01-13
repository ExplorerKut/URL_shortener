from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3
from hashids import Hashids
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__)
os.environ.get('DATABASE_URL')
app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
hashids= Hashids(min_length=4, salt=app.config['SECRET_KEY'])

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)


db=SQLAlchemy(app)
class Urls(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    original_url=db.Column(db.String(500),nullable=False)

    def __init__(self,id, original_url):
        self.id=id
        self.original_url=original_url

@app.route('/',methods=('GET','POST'))
def index():
    if request.method=='POST':
        url=request.form['org_url']
        
        if not url:
            flash('Please enter URL of correct format')
            return redirect(url_for('index'))
        
        is_present=Urls.query.filter_by(original_url=url).first()
        if is_present is None:
            db.session.execute("INSERT INTO urls(original_url) values('"+url+"')")
            db.session.commit()
        url_data_id=Urls.query.filter_by(original_url=url).first()
        db.session.commit()
        url_id=url_data_id.id
        hashid=hashids.encode(url_id)
        short_url= request.host_url +hashid
        
        return render_template('index.html',short_url=short_url)
    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    original_id= hashids.decode(id)

    if original_id:
        original_id=original_id[0]
        url_data=Urls.query.filter_by(id=original_id).first()
        db.session.commit()
        original_url=url_data.original_url
        return redirect(original_url)
    else:
        flash('Invalid Url')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)