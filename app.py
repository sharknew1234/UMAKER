from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    info = db.Column(db.Text, nullable = False)
    cat = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        return f"Product('{self.title}', '{self.price}', '{self.info}', '{self.cat}')"

class Sell(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    loc = db.Column(db.String)
    phone = db.Column(db.Integer, nullable = False)
    link = db.Column(db.String, nullable = False)
    unvan = db.Column(db.String, nullable = False)
    fio = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"Product('{self.loc}', '{self.phone}', '{self.link}', '{self.unvan}', '{self.fio}')"


class FeedBack(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    text = db.Column(db.Text, nullable = False)
    email = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"Feedback('{self.title}', '{self.text}', '{self.email}')"

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    t = db.Column(db.Text, nullable = False)

    def __repr__(self):
        return f"Forum('{self.name}', '{self.t}')"

app.app_context().push()
db.create_all()

@app.route('/')
@app.route('/home')
@app.route('/home1')
def index():
    q = request.args.get('q')

    if q:
        prs = Product.query.filter(Product.title.contains(q) | Product.cat.contains(q)).all()
    else:
        prs = Product.query.all()
    return render_template('index.html', prs=prs)

@app.route('/<int:n>', methods=['POST', 'GET'])
def index_more(n):
    pr = Product.query.get(n)
    return render_template('index_more.html', pr=pr)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/!TwxAQ*y!6', methods = ['POST', 'GET'])
def admin():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        info = request.form['info']
        cat = request.form['category']
        
        product = Product(title=title, price=price, info=info, cat=cat)
        try:
            db.session.add(product)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        fbs = FeedBack.query.all()
        sl = Sell.query.all()
        return render_template('admin.html', fbs=fbs, sl=sl)

@app.route('/!TwxAQ*y!6/<int:l>/delete')
def admin_del(l):
    pr = Product.query.get_or_404(l)

    try:
        db.session.delete(pr)
        db.session.commit()
        return redirect('/')
    except:
        return 'Error'

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        title = request.form['title']
        email = request.form['email']
        text = request.form['text']

        feedback = FeedBack(title=title, email=email, text=text)

        try:
            db.session.add(feedback)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error'
    else:
        return render_template('contact.html')

@app.route('/!TwxAQ*y!6/<int:t>')
def user_more(t):
    fb = FeedBack.query.get(t)
    return render_template('admin_det.html', fb=fb)

@app.route('/shello', methods = ['POST', 'GET'])
@app.route('/s', methods = ['POST', 'GET'])
def s_s():
    if request.method == 'POST':
        phone = request.form['Phone']
        link = request.form['Link']
        loc = request.form['Location']
        unvan = request.form['unvan']
        fio = request.form['fio']

        sell = Sell(fio=fio, unvan=unvan, phone=phone, link=link, loc=loc)

        try:
            db.session.add(sell)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error' 
    else:
        return render_template('sifaris.html')

@app.route('/forum', methods = ['POST', 'GET'])
def f_f():
    if request.method == 'POST':
        name = request.form['name']
        t = request.form['t']

        forum = Forum(name=name, t=t)

        try:
            db.session.add(forum)
            db.session.commit()
            return redirect('/forum')
        except:
            return 'Error'
    else:
        f = Forum.query.all()
        return render_template('forum.html', f=f)

@app.route('/book')
def book():
    book = Product.query.filter(Product.cat.contains("Book")).all()

    return render_template('book.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)