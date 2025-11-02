import dummy1

########

print("Hello1")
print(__name__)

if __name__=="__main__": ###false
    print("From Hello1")
###########################    
    print("Hello2")
print(__name__)

if __name__=="__main__": ##true
    print("From Hello2")