import random,string
import json,requests
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify

#local Imports

from package import app,csrf
from package.models import db,User,Job,Sell,Cart, Adverts
from package.forms import *

#create after_request to clear cache
@app.after_request
def after_request(respone):
    #TO solve the problem of loggedout users's details being cached in the browser
    respone.headers['Cache-Control']="no-cache, no-store, must-revalidate"
    return respone

def generate_string(howmany):#call this function as renerate_string(10)
    x = random.sample(string.digits,howmany)
    return ''.join(x)


#create decorator to check for logins
def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('userloggedin')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied, Login To Gain Access")
            return redirect('/login')
    return login_check    

@app.route('/',methods=['POST','GET'])
def landing():
    config_items=app.config
    return render_template('/landing.html')

@app.route('/upload',methods=['POST','GET'])
def upload():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    upload=Uploadfile()
    if request.method=='GET':
        return render_template('/upload.html',upload=upload,userdeets=userdeets)
    else:
         if request.method =='GET':
            deets= db.session.query(Sell).all()
            return render_template('/upload.html',deets=deets,userdeets=userdeets)
         else:
            #retrieve the file
            allowed=['jpg','png']
            filesobj=request.files['frontimg']
            filesobj1=request.files['backimg']
            filename=filesobj.filename
            filename1=filesobj1.filename       
            newname='Default.png'
            newname1='Default.png'
            #validation
            if filename=='' or filename1=='':
                flash('Please upload both Images',category='error')
            else:                
                pieces=filename.split('.')
                pieces1=filename1.split('.')
                ext=pieces[-1].lower()
                ext1=pieces1[-1].lower()
                if ext and ext1 in allowed:
                    newname=str(int(random.random()*10000000))+filename
                    newname1=str(int(random.random()*10000000))+filename1
                    filesobj.save('package/static/uploads/'+ newname)
                    filesobj1.save('package/static/uploads/'+ newname1)
                else:
                    flash("Not Allowed, File Type Must Be ['jpg','png'], File was not uploades",category='error')
            newfile=newname
            newfile1=newname1
            desc=request.form.get('productdescription')
            price =request.form.get('productprice')
            delprice=request.form.get('delprice')
            quantity =request.form.get('quantity')
            uploader =Sell(price=price,delprice=delprice, description=desc ,front_img=newfile,back_img=newfile1,seller_user_id =id,quantity=quantity)
            db.session.add(uploader)
            db.session.commit()
            return redirect(url_for('shop'))


@app.route('/index',methods=['POST','GET'])
@login_required
def index():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    advert = db.session.query(Adverts).all()
    return render_template('/index.html',userdeets=userdeets, advert=advert)

@app.route('/cart',methods=['POST','GET'])
@login_required
def cart():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/cart.html',userdeets=userdeets)

@app.route('/copy',methods=['POST','GET'])
def copy():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/inni.html',userdeets=userdeets)

@app.route('/login',methods=['POST','GET'])
def login():
    log=LogForm()
    if request.method=="GET":
        return render_template('/login.html',log=log)
    else:
        email=request.form.get('email')
        pwd=request.form.get('pword')
        userdeets=db.session.query(User).filter(User.email==email).first()
        if userdeets != None:
            hashed_pwd=userdeets.password
            if check_password_hash(hashed_pwd,pwd) == True:
                session['userloggedin']=userdeets.user_id
                return redirect('/index')
            else:
                flash('Invalid Login Credentials,Try Again Or Reset Password')
                return redirect('/login')
        else:
            flash('Cant Connect Db')
            return redirect('/login')

@app.route('/reg',methods=['POST','GET'])
def reg():
    usereg=RegForm()   
    if request.method =="GET":
        return render_template('/reg.html',usereg=usereg)
    else:
        if usereg.validate_on_submit:
            fname=request.form.get('fname')
            lname=request.form.get('lname')
            address=request.form.get('address')
            email=request.form.get('email')
            phone=request.form.get('phone')
            username=request.form.get('username')
            pwd=request.form.get('pwd')
            status=request.form.get('status')
            hashed_pwd=generate_password_hash(pwd)
            user=User(firstname=fname,lastname=lname,email=email,password=hashed_pwd,phone=phone,address=address,username=username,status=status)
            db.session.add(user)
            db.session.commit()
            flash('Account Created Please Login')
            return redirect('/login')
        else:
            flash('Error With Database')
            return render_template('/reg.html',usereg=usereg)


@app.route('/jobs',methods=['GET','POST'])
def job():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    jb= db.session.query(Job).all()
    return render_template('/job_index.html',jb=jb,userdeets=userdeets)

@app.route('/accesories',methods=['GET','POST'])
def accesories():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/Accesories.html',userdeets=userdeets)

@app.route('/fragrance',methods=['GET','POST'])
def fragrance():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/fragrance.html',userdeets=userdeets)

@app.route('/handbags',methods=['GET','POST'])
def handbags():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/handbags.html',userdeets=userdeets)

@app.route('/men',methods=['GET','POST'])
def men():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/men.html',userdeets=userdeets)

@app.route('/suits',methods=['GET','POST'])
def suits():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/suits.html',userdeets=userdeets)

@app.route('/shoes',methods=['GET','POST'])
def shoes():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/shoes.html',userdeets=userdeets)

@app.route('/watches',methods=['GET','POST'])
def watches():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/watches.html',userdeets=userdeets)

@app.route('/women',methods=['GET','POST'])
def women():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    return render_template('/shop/women.html',userdeets=userdeets)





@app.route('/shop',methods=['GET','POST'])
def shop():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    shopdeets= db.session.query(Sell).all()
    return render_template('/shop/shop1.html',userdeets=userdeets,shopdeets=shopdeets)

@app.route('/logout')
def logout():
    if session.get("userloggedin")!= None:
        session.pop("userloggedin",None)
    return redirect('/') 

@app.route('/changepass',methods=["GET","POST"])
@login_required
def changepas():
    changep = ChangePass()
    id = session.get("userloggedin")
    userdeets = db.session.query(User).get_or_404(id)
    if request.method =="GET":
        return render_template('changepass.html',userdeets=userdeets,changep=changep)
    else:
        email= request.form.get('email')
        pwd = request.form.get('pwd')
        freshpwd = request.form.get('newpwd')
        chpwd=generate_password_hash(freshpwd)
        deets = db.session.query(User).filter(User.email==email).first()
        if deets != None:
            hashed_pwd =deets.password
            if check_password_hash(hashed_pwd,pwd)==True:
                deets.password = chpwd
                db.session.commit()
                flash('your password have been changed Successfully',category='changeperror')
                return redirect(url_for('changepas'))
            else:
                return render_template('changepass.html',userdeets=userdeets,changep=changep)
        else:
            flash('Check your email',category='changeperror')
            return render_template('changepass.html',userdeets=userdeets,changep=changep)
        

@app.route('/editprofiles',methods=["GET","POST"])
@login_required
def editp():
    edit = ProfileForm()
    id = session.get("userloggedin")
    userdeets = db.session.query(User).get_or_404(id)
    if request.method =="GET":
        return render_template('editprofile.html',userdeets=userdeets,edit=edit)
    else:
        if edit.validate_on_submit:
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname') 
            phone = request.form.get('phone')
            city = request.form.get('city')
            email=request.form.get('email')
            address = request.form.get('address')
            userdeets.firstname=firstname
            userdeets.lastname=lastname
            userdeets.phone=phone
            userdeets.address= address
            userdeets.city=city
            userdeets.email=email
            db.session.commit()
            flash('your profile has been updated',category='editprofile')
            return redirect(url_for('editp'))
        else:
            return render_template('editprofile.html',edit=edit,userdeets=userdeets)
        


@app.route('/add_cart',methods=['POST'])
@login_required
def catp():
    sell_id = request.form.get("sell_id")
    userid = session['userloggedin']
    img = request.form.get("img")
    price = request.form.get("price")
    quantity = request.form.get("quantity")
    description = request.form.get("description")
    query = Cart(price=price,goods_id=sell_id,img=img,quantity=quantity,description=description,seller_user_id=userid)
    db.session.add(query)
    db.session.commit()
    return ("sent to database")
    