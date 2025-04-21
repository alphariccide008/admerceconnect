from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import StringField,SubmitField,TextAreaField,PasswordField,SubmitField,DateField,IntegerField,FileField,RadioField
from wtforms.validators import Email,DataRequired,EqualTo,Length

class RegForm(FlaskForm):
    fname= StringField("FirstName",validators=[DataRequired()])
    lname= StringField("LastName",validators=[DataRequired(),Length(min=5)])
    email= StringField("Email",validators=[Email(),DataRequired(message='Please Input A Valid Email Address..')])
    pwd= PasswordField("Enter Password",validators=[DataRequired()])
    confpwd= PasswordField("Confirm Password",validators=[EqualTo('pwd'),DataRequired(message='Please Make Sure Password Corresponds With The One Stated Earlier')])
    username= StringField("Username",validators=[DataRequired(message='Please Input A Username')])
    phone= StringField("Phone Number",validators=[DataRequired(message='Please Input A Valid Phone Number'),Length(min=11)])
    address= StringField("Home Address",validators=[DataRequired(message='Please Input Home Address')])   
    btnsubmit=SubmitField("Register")

class Uploadfile(FlaskForm):
    frontimg = FileField("Front Image",validators=[FileAllowed(['jpg','png','jpeg'])])
    backimg = FileField("Back Image",validators=[FileAllowed(['jpg','png','jpeg'])])
    productdescription = TextAreaField("Description",validators=[DataRequired(message="Please Input A description")])
    productprice= StringField("Project Price",validators=[DataRequired(message="Price")])
    delprice= StringField("Old Price",validators=[DataRequired(message="Old Price")])
    quantity= StringField("Quantity",validators=[DataRequired(message="quantity")])
    btnsubmit = SubmitField("Upload Project")

class ChangePass(FlaskForm):
    email= StringField("Input Email",validators=[DataRequired(message="Enter email")])
    pwd = PasswordField("Enter Old Password",validators=[DataRequired(message="incorrect Password")])
    newpwd = PasswordField("New Password",validators=[DataRequired(message="Fill the field")])
    btnsubmit = SubmitField("Update Profile")


class LogForm(FlaskForm):
    email= StringField("Email Address",validators=[DataRequired(message='Enter A Registered Email Address..')])
    pword= PasswordField("Password",validators=[DataRequired(message='Enter A Valid Password')])
    btnlog=SubmitField("Log In")

class AdmLogForm(FlaskForm):
    email= StringField("Email Address",validators=[DataRequired(message='Enter A Registered Email Address..')])
    pword= PasswordField("Password",validators=[DataRequired(message='Enter A Valid Password')])
    btnlog=SubmitField("Log In")

class JobForm(FlaskForm):
    jobtitle =StringField('Job Title', validators=[DataRequired()])  #add more validation rules here if needed
    job_state=StringField('Job State',validators=[DataRequired()])
    job_country=StringField('Job Country',validators=[DataRequired()])
    job_salary=StringField('Salary Range',validators=[DataRequired()])
    job_employer=StringField('Employer',validators=[DataRequired()])
    working_hours=StringField('Working Hours',validators=[DataRequired()])
    job_link=StringField('Link',validators=[DataRequired()])
    submit = SubmitField('Add')

class ProfileForm(FlaskForm):
    firstname = StringField("First Name",validators=[DataRequired(message="Input your First Name")])
    lastname = StringField("Last Name",validators=[DataRequired(message="Input your First Name")])
    phone = StringField("Phone ",validators=[DataRequired(message="Input your First Name")])
    email = StringField("email",validators=[DataRequired(message="Input your First Name")])
    city = StringField("City",validators=[DataRequired(message="Input your First Name")])
    address = StringField("Address ",validators=[DataRequired(message="Input your First Name")])
    btnsubmit = SubmitField("Update Profile")

