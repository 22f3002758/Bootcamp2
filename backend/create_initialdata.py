from flask import current_app as app
from .models import *

with app.app_context():
    db.create_all()
    if db.session.query(Services).count()==0:
        srv1=Services(name="Home Cleaning", baseprice=500, description="Home Cleaning category")
        srv2=Services(name="Home Decor", baseprice=700, description="Home Decor category")
        db.session.add_all([srv1,srv2])
        db.session.commit()

    if  db.session.query(ServiceProvider).count()==0:
        sp1=ServiceProvider(email="sp1@gmail.com",password="asdf",servicename='Home Cleaning', status='Active')
        sp2=ServiceProvider(email="sp2@gmail.com",password="asdf",servicename='Home Cleaning', status='Active')
        sp3=ServiceProvider(email="sp3@gmail.com",password="asdf",servicename='Home Decor', status='Active')
        sp4=ServiceProvider(email="sp4@gmail.com",password="asdf",servicename='Home Decor', status='Active')   
        db.session.add_all([sp1,sp2,sp3,sp4])
        db.session.commit()

    if db.session.query(Admin).count==0:
        ad=Admin(email="admin@gmail.com", password="asdf")    
        db.session.add(ad)
        db.session.commit()

    if  db.session.query(Customer).count()==0:
        cust=Customer(name='Rahul',email="Rahul@gmail.com",password="asdf", status='Active')
        
        db.session.add(cust)
        db.session.commit()

    #Extract all sp of Home Cleaning

    serv_obj=db.session.query(Services).filter_by(name="Home Cleaning").first()
    print(serv_obj.Sproviders[0].email)   

    spobj=db.session.query(ServiceProvider).filter_by(email='sp1@gmail.com').first()
    bp=spobj.service.baseprice
    print(bp)
