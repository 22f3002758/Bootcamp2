from flask import current_app as app, render_template, request, redirect
from backend.models import *
from flask_login import login_user, login_required,current_user

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        femail=request.form.get("email")
        fpwd=request.form.get("pwd")
        sp_obj=db.session.query(ServiceProvider).filter_by(email=femail).first()
        cust_obj=db.session.query(Customer).filter_by(email=femail).first()
        ad_obj=db.session.query(Admin).filter_by(email=femail).first()
        if sp_obj and sp_obj.password==fpwd:
            login_user(sp_obj)
            return redirect("/dashboard/sp")
        elif cust_obj and cust_obj.password==fpwd:
            login_user(cust_obj)
            return redirect("/dashboard/cust")
        elif ad_obj and ad_obj.password==fpwd:
            login_user(ad_obj)
            return redirect("/dashboard/ad")
        else:
            return " check your credentials"

        


@app.route("/dashboard/sp", methods=['GET','POST'])
@login_required
def sp_dasboard():
    if isinstance(current_user,ServiceProvider):
        return f"Welcome to sp dashboard{current_user.email}"      
    else:
        return "Unauthorized access"

@app.route("/dashboard/cust", methods=['GET','POST'])
@login_required
def cust_dasboard():
    if isinstance(current_user,Customer):
        return f"Welcome to customer dashboard{current_user.email}"  
    else:
        return "Unauthorized access"

@app.route("/dashboard/ad", methods=['GET','POST'])
@login_required
def ad_dasboard():
    if isinstance(current_user,Admin):
        return f"Welcome to Admin dashboard{current_user.email}" 
    else:
        return "Unauthorized access"