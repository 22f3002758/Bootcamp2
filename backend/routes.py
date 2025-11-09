from flask import current_app as app, render_template, request, redirect
from backend.models import *
from flask_login import login_user, login_required,current_user,logout_user
from sqlalchemy import or_

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/register',methods=["GET","POST"])
def register():
     if request.method=="GET":
        return render_template("customer/cust_register.html")
     elif request.method=="POST":
        fname=request.form.get("cname")
        femail=request.form.get("cemail")
        fpwd=request.form.get("cpwd")
        fcity=request.form.get("ccity")
        fphone=request.form.get("cphone")
        cust_obj=db.session.query(Customer).filter_by(email=femail).first()
        if not cust_obj:
            custdata=Customer(name=fname,email=femail,password=fpwd,city=fcity,phone=fphone,status='Active')
            db.session.add(custdata)
            db.session.commit()
            return redirect("/login")
        else:
            return "User already exist"
        
     

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


        


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
        serv=db.session.query(Services).all()
        sp=db.session.query(ServiceProvider).all()
        cust=db.session.query(Customer).all()
        return render_template("admin/ad_dashboard.html",services=serv, serviceproviders=sp, customers=cust) 
    else:
        return "Unauthorized access"
    

@app.route("/search/admin", methods=["GET","POST"]) 
def ad_search():
    if request.method=="GET":
        return render_template("admin/search.html")
    elif request.method=="POST":
        qtype=request.form.get("querytype")
        qry=request.form.get("query")
        if qtype=="service" and qry:
            obj=db.session.query(Services).filter(or_(Services.name.ilike(f"%{qry}%"),Services.description.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html",services=obj, qtype=qtype)
        if qtype=="sp" and qry:
            obj=db.session.query(ServiceProvider).filter(or_(ServiceProvider.name.ilike(f"%{qry}%"),ServiceProvider.email.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html",serviceproviders=obj, qtype=qtype)
        if qtype=="cust" and qry:
            obj=db.session.query(Customer).filter(or_(Customer.name.ilike(f"%{qry}%"),Customer.email.ilike(f"%{qry}%"))).all()
            return render_template("admin/search.html",customers=obj, qtype=qtype)




@app.route("/createservices", methods=["GET","POST"])
def services():
    if request.method=="GET" and request.args.get("action")=="create":
        return render_template("admin/create_services.html")    
    elif request.method=="POST" and request.args.get("action")=="create":
        fname=request.form.get("name")
        fbp=request.form.get("bp")
        fdesc=request.form.get("desc")
        servobj=db.session.query(Services).filter_by(name=fname).first()
        if not servobj:
            dbserv=Services(name=fname, baseprice=fbp, description=fdesc)
            db.session.add(dbserv)
            db.session.commit()
            return redirect("/dashboard/ad")
        else:
            return redirect("/createservices")
    elif request.method=="GET" and request.args.get("action")=="edit":
        id=request.args.get("id")
        servobj=db.session.query(Services).filter_by(id=id).first()  
        
        return render_template("admin/create_services.html",servobj=servobj)
        
    elif request.method=="POST" and request.args.get("action")=="edit":  
        id=request.args.get("id") 
        fname=request.form.get("name")
        fbp=request.form.get("bp")
        fdesc=request.form.get("desc")
        obj=db.session.query(Services).filter_by(id=id).first() 
        if fname:
            obj.name=fname
        if fbp:
            obj.baseprice=fbp
        if fdesc:
            obj.description=fdesc
        db.session.commit()
        return redirect("/dashboard/ad")   

    elif request.method=="GET" and request.args.get("action")=="delete":
        id=request.args.get("id")
        delobj=db.session.query(Services).filter_by(id=id).first() 
        db.session.delete(delobj)
        db.session.commit()
        return redirect("dashboard/ad")
        


@app.route("/manageproviders", methods=["GET","POST"])
def manageproviders():
    if request.method=="GET" and request.args.get("action")=="create" :
        services=db.session.query(Services).all()
        return render_template("admin/create_sp.html", services=services)  
    elif request.method=="POST" and request.args.get("action")=="create":
        fname= request.form.get("name")
        femail=request.form.get("email")
        fpwd=request.form.get("pwd")
        fcity=request.form.get("city")
        fphone=request.form.get("phone")
        fcat=request.form.get("cat")
        spobj=db.session.query(ServiceProvider).filter_by(email=femail).first()
        if not spobj:
            dbobj=ServiceProvider(name=fname,email=femail,password=fpwd,city=fcity,phone=fphone,servicename=fcat)
            db.session.add(dbobj)
            db.session.commit()
            return redirect("/dashboard/ad")
        
    elif request.method=="GET" and request.args.get("action")=="edit":  
        id=request.args.get("id")
        spobj=db.session.query(ServiceProvider).filter_by(id=id).first()
        services=db.session.query(Services).all()
        return render_template("admin/create_sp.html",spobj=spobj, services=services)
    
    elif request.method=="POST" and request.args.get("action")=="edit":
        print("Hello world")
        id=request.args.get("id")
        fname= request.form.get("name")
        femail=request.form.get("email")
        fpwd=request.form.get("pwd")
        fcity=request.form.get("city")
        fphone=request.form.get("phone")
        fcat=request.form.get("cat")
        spobj=db.session.query(ServiceProvider).filter_by(id=id).first()
        if fname:
            spobj.name=fname
        if femail:
            spobj.email=femail
        if fpwd:
            spobj.password=fpwd
        if fcity:
            spobj.city=fcity  
        if fphone:
            spobj.phone=fphone   
        if fcat:
            spobj.servicename=fcat 
        db.session.commit()
        return redirect("dashboard/ad")    

    elif request.method=="GET" and request.args.get("action")=="delete":
        id=request.args.get("id")
        delobj=db.session.query(ServiceProvider).filter_by(id=id).first() 
        db.session.delete(delobj)
        db.session.commit()
        return redirect("dashboard/ad")
      

@app.route("/managecust", methods=["GET", "POST"])
def managecust():
    id=request.args.get("id")
    custobj=db.session.query(Customer).filter_by(id=id).first()
    if request.args.get("action")=='Flag':
        custobj.status="Flagged"
        db.session.commit()
        return redirect("dashboard/ad")
    elif request.args.get("action")=="Unflag":
        custobj.status="Active"
        db.session.commit()
        return redirect("dashboard/ad")



