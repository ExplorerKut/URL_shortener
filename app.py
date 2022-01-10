from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3
from hashids import Hashids
app = Flask(__name__)
app.config['SECRET_KEY']='my secret key123'
hashids= Hashids(min_length=4, salt=app.config['SECRET_KEY'])

def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/',methods=('GET','POST'))
def index():
    conn=get_db_connection()

    if request.method=='POST':
        url=request.form['org_url']
        
        if not url:
            flash('Please enter URL of correct format')
            return redirect(url_for('index'))
        
        url_data=conn.execute('INSERT INTO urls(original_url) VALUES(?)',(url,))
        conn.commit()
        conn.close()

        url_id= url_data.lastrowid
        hashid=hashids.encode(url_id)
        short_url= request.host_url +hashid
        
        return render_template('index.html',short_url=short_url)
    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):
    conn=get_db_connection()
    original_id= hashids.decode(id)
    
    if original_id:
        original_id=original_id[0]
        url_data= conn.execute('SELECT original_url FROM urls WHERE id=(?)',(original_id,)).fetchone()
        original_url= url_data['original_url']
        
        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid Url')
        return redirect(url_for('index'))