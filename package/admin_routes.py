import random,string,os
import json,requests
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask import render_template,request,abort,redirect,flash,make_response,session,url_for,jsonify

from package import app,csrf
from package.models import db,User,Admin,Job,Adverts, Transaction
from package.forms import *


def login_required(f):
    @wraps(f)
    def login_check(*args,**kwargs):
        if session.get('adminloggedin')!=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied, Login To Gain Access")
            return redirect('/logadmin')
    return login_check

@app.route('/logadmin',methods=['POST','GET'])
def adminlog():
    adm=AdmLogForm()
    if request.method=="GET":
        return render_template('/admin/adminlog.html',adm=adm)
    else:
        email=request.form.get('email')
        pwd=request.form.get('pword')
        admindeets=db.session.query(Admin).filter(Admin.email==email).first()
        if admindeets != None:
            hashed_pwd=admindeets.pwd
            if check_password_hash(hashed_pwd,pwd) == True:
                session['adminloggedin']=admindeets.admin_id
                return redirect('/admin/alluser/')
            else:
                flash('Invalid Login Credentials,Try Again Or Reset Password')
                return redirect('/logadmin')
        else:
            flash('Cant Connect Db')
            return redirect('/logadmin')
       

@app.route('/admin/alluser/')
@login_required
def all_user():
    use= db.session.query(User).all()
    return render_template('admin/alluser.html',use=use)

@app.route('/admin/user_delete/<id>/')
@login_required
def user_delete(id):
    use=db.session.query(User).get_or_404(id)
    db.session.delete(use)
    db.session.commit()
    flash('User Data Deleted')
    return redirect(url_for('all_user'))

@app.route('/admin/addjob/',methods=['POST','GET'])
@login_required
def add_job():
    job=JobForm()
    if request.method=="GET":
        return render_template('admin/addjobs.html',job=job)
    else:
        if job.validate_on_submit:
            title=request.form.get('jobtitle')
            state=request.form.get('job_state')
            country=request.form.get('job_country')
            employer=request.form.get('job_employer')
            salary=request.form.get('job_salary')
            hours=request.form.get('working_hours')
            lnk=request.form.get('job_link')
            jo=Job(job_title=title,job_state=state,job_country=country,employer=employer,salary_range=salary,job_link=lnk,working_hours=hours)
            db.session.add(jo)
            db.session.commit()
            flash('Job Added')
            return redirect('/admin/addjob/')
        else:
            flash('All Field Must Be Filled Out')
            render_template('/admin/addjob/',job=job)


@app.route('/admin/addads/',methods=['POST','GET'])
@login_required
def add_ads():
    if request.method=="GET":
        return render_template('admin/addads.html')
    else:
          #retrieve the file
            allowed=['jpg','png']
            filesobj=request.files['cover']
            filename=filesobj.filename
            newname='Default.png'
            #validation
            if filename=='':
                flash('Please Choose a book cover',category='error')
            else:                
                pieces=filename.split('.')
                ext=pieces[-1].lower()
                if ext in allowed:
                    newname=str(int(random.random()*10000000))+filename
                    filesobj.save('package/static/uploads/'+ newname)
                else:
                    flash("Not Allowed, File Type Must Be ['jpg','png'], File was not uploades",category='error') 

            company=request.form.get('company')
            cover=newname
            ad=Adverts(ads_company=company,ads_cover=cover)
            db.session.add(ad)
            db.session.commit()
            if ad.ads_id:
                flash("Ads Added",category='info')
            else:
                flash("Problem Occured,Please Try Again",category='danger')
            return redirect(url_for('add_ads'))
    




@app.route('/admin/alltransactions/')
@login_required
def all_transaction():
    userdeets = db.session.query(Transaction).all()
    return render_template('admin/transaction.html',userdeets=userdeets)




@app.route('/orders')
@login_required
def orders():
    admin_id = session.get('admin')
    # Only fetch confirmed transactions
    confirmed_transactions = db.session.query(Transaction).filter(Transaction.status == 'confirmed').all()

    return render_template('admin/order.html', transaction=confirmed_transactions)


@app.route("/Product/<int:di>/")
def product_confirm(di):
    # Query the transaction by ID
    transaction = db.session.query(Transaction).filter_by(id=di).first()  # Use .first() to get the transaction

    if transaction:  # Check if the transaction exists
        transaction.status = 'confirmed'  # Update transaction status to 'confirmed'
        db.session.commit()
        flash('Payment confirmed', category='paymentmsg')
    else:
        flash('Transaction not found', category='danger')

    return redirect(url_for('orders'))  # Redirect to the orders page


@app.route("/shipment_confirmation/<int:di>/")
def payment_confirm(di):
    # Query the transaction by ID
    transaction = db.session.query(Transaction).filter_by(id=di).first()  # Use .first() to get the transaction

    if transaction:  # Check if the transaction exists
        transaction.shipment_status = 'shipped'  # Update shipment status to 'shipped'
        db.session.commit()
        flash('Product shipped', category='paymentmsg')
    else:
        flash('Transaction not found', category='danger')

    return redirect(url_for('orders'))  # Redirect to the orders page



@app.route("/notifications")
@login_required
def notifications():
    # Query for all transactions that are in 'pending' status
    new_orders = Transaction.query.filter_by(status='pending').all()

    # Prepare the data to return to the front end
    notifications = []
    for order in new_orders:
        notifications.append({
            'id': order.id,
            'name': order.name,
            'email': order.email,
            'amount': order.amount,
            'timestamp': order.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'product_names': order.product_description,
        })

    return jsonify(notifications)