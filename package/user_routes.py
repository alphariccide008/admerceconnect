import random,string
import json,requests
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask_mail import Message
from package import mail 
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify

#local Imports

from package import app,csrf
from package.models import db,User,Job,Product,Cart, Adverts, Transaction
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
            deets= db.session.query(Product).all()
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
            product_name = request.form.get('product_name')
            seller = request.form.get('seller')
            seller_phone =request.form.get('seller_number')
            desc=request.form.get('productdescription')
            price =request.form.get('productprice')
            delprice=request.form.get('delprice')
            quantity =request.form.get('quantity')
            category = request.form.get('category')
            uploader =Product(price=price,delprice=delprice,seller_name=seller ,category=category,product_name=product_name, seller_number=seller_phone, description=desc ,front_img=newfile,back_img=newfile1,seller_user_id =id,quantity=quantity)
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
    products = db.session.query(Product).filter(Product.category =='fragrance').all()
    return render_template('/shop/fragrance.html',userdeets=userdeets, products=products)

@app.route('/handbags',methods=['GET','POST'])
def handbags():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='handbag').all()
    return render_template('/shop/handbags.html',userdeets=userdeets, products=products)

@app.route('/men',methods=['GET','POST'])
def men():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='men').all()
    return render_template('/shop/men.html',userdeets=userdeets, products=products )

@app.route('/suits',methods=['GET','POST'])
def suits():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='suits').all()
    return render_template('/shop/suits.html',userdeets=userdeets, products=products)

@app.route('/shoes',methods=['GET','POST'])
def shoes():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='shoes').all()
    return render_template('/shop/shoes.html',userdeets=userdeets, products=products)

@app.route('/watches',methods=['GET','POST'])
def watches():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='watches').all()
    return render_template('/shop/watches.html',userdeets=userdeets, products=products)

@app.route('/women',methods=['GET','POST'])
def women():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    products = db.session.query(Product).filter(Product.category =='women').all()
    return render_template('/shop/women.html',userdeets=userdeets, products=products)





@app.route('/shop',methods=['GET','POST'])
def shop():
    id= session.get('userloggedin')
    userdeets =db.session.query(User).get_or_404(id)
    shopdeets= db.session.query(Product).all()
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
        


# All cart route 
@app.route("/add-to-cart/<int:item_id>")
def add_to_cart(item_id):
    user_id = session.get('userloggedin')  # Assuming your session key is 'userloggedin'
    if not user_id:
        return redirect(url_for('login'))  # Redirect if user is not logged in

    # Fetch the product from DB
    product = Product.query.get_or_404(item_id)

    # Check if the product already exists in the cart
    existing_item = Cart.query.filter_by(user_id=user_id, goods_id=item_id).first()

    if existing_item:
        # If it exists, increment the quantity
        existing_item.quantity += 1
    else:
        # Otherwise, add it as a new item
        new_item = Cart(
            user_id=user_id,
            goods_id=product.product_id,
            img=product.front_img,  # Assuming your product model has an 'img' field
            price=product.price,
            quantity=1,
            product_name=product.product_name,
            seller_name=product.seller_name,
            seller_number=product.seller_number,
            seller_id = product.seller_user_id,
            description=product.description
        )
        db.session.add(new_item)

    db.session.commit()
    return redirect(url_for('shop'))
    


@app.context_processor
def inject_cart_count():
    user_id = session.get('userloggedin')
    count = Cart.query.filter_by(user_id=user_id).count() if user_id else 0
    return dict(cart_count=count)


@app.route("/cart")
@login_required
def cart():
    user_id = session.get('userloggedin')  # Get user ID from session
    if not user_id:
        return redirect(url_for('login'))  # Redirect if not logged in

    # Retrieve the logged-in user and their cart items
    userdeets = db.session.query(User).get_or_404(user_id)

    # Get items in the cart along with associated product details
    cart_items = Cart.query.filter_by(user_id=userdeets.user_id).all()

    # Calculate total price for all items in cart
    total = sum(item.price * item.quantity for item in cart_items)

    return render_template('/cart.html', items=cart_items, total=total, userdeets=userdeets)



@app.route("/remove-from-cart/<int:item_id>")
def remove_from_cart(item_id):
    user_id = session.get('userloggedin')
    if not user_id:
        return redirect(url_for('login'))  # Redirect if user is not logged in
    
    # Fetch the cart item to be removed
    cart_item = Cart.query.filter_by(goods_id=item_id, user_id=user_id).first()
    
    if cart_item:
        db.session.delete(cart_item)  # Delete the item from the database
        db.session.commit() # Commit the changes to the database
    
    return redirect(url_for('cart')) 



# Payment Gatewayfrom flask_mail import Message
@app.route("/checkout", methods=["POST", "GET"])
def checkout():
    user_id = session.get('userloggedin')
    if not user_id:
        return redirect(url_for('login'))

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        flash("Your cart is empty.", "danger")
        return redirect(url_for('cart'))

    total_amount = sum(item.price * item.quantity for item in cart_items) * 100

    product_names = [item.product_name for item in cart_items]

    product_quantities = [str(item.quantity) for item in cart_items]
    product_images = [item.img for item in cart_items]
   

    product_name = ", ".join(product_names)
    quantities_str = ", ".join(product_quantities)
    images_str = ", ".join(product_images)
    seller_names = ', '.join([item.seller_name for item in cart_items])
    seller_numbers = ', '.join([item.seller_number for item in cart_items])

    name = request.form["name"]
    email = request.form["email"]
    address = request.form["address"]

    transaction = Transaction(
        user_id=user_id,
        amount=total_amount,
        status="pending",
        reference="",
        name=name,
        email=email,
        address=address,
        seller_name=seller_names,
        seller_number=seller_numbers,
        product_name=product_name,
        quantities=quantities_str,
        img=images_str,
        shipment_status="pending"
    )
    db.session.add(transaction)
    db.session.commit()

    # ✅ Send order summary email
    try:
        msg = Message("Your Order Summary", recipients=[email])
        msg.body = f"""Hi {name},Thank you for shopping with AdcomerceConnect! Here is a summary of your order:

        Products: {product_name}
        Quantities: {quantities_str}
        Shipping Address: {address}
        Total Amount: ₦{total_amount / 100:.2f}

        We will notify you once the payment is complete and your order is on its way.

        Best regards,
        AdmerceConnect Team
                """
        mail.send(msg)
    except Exception as e:
        flash(f"Could not send email: {str(e)}", "warning")

    # Initialize Paystack
    headers = {
        "Authorization": "Bearer sk_test_f3f650ddd241d9c89f13c3d9468162052fcc8152",
        "Content-Type": "application/json"
    }

    data = {
        "email": email,
        "amount": total_amount,
        "callback_url": url_for("shop", _external=True),
        "metadata": {"product_description": product_name}
    }

    try:
        res = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
        response_data = res.json()

        if res.status_code == 200 and response_data["status"]:
            transaction.reference = response_data["data"]["reference"]
            db.session.commit()

            # Clear cart
            Cart.query.filter_by(user_id=user_id).delete()
            db.session.commit()

            return redirect(response_data["data"]["authorization_url"])
        else:
            flash("Payment initialization failed: " + response_data.get("message", "Unknown error"), "danger")
            return redirect(url_for('cart'))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('cart'))
