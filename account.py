import security
import bcrypt
from security import *

class Account:
    """
    An instance represents a user's account. Contains fields:
        First Name
        Last Name
        Name (first name + last name)
        Username
        Password
        email
        Graduation year
        Academy
        Job Title (optional)
        Company (optional)
    """
    
    
    def __init__(self, fname, lname, un, pw, em, gy, a, job, comp):
        """
        Initialize account with first and last name, username, hashed password, email, grad year, academy, job title, and company.
        """
        
        self.firstName = fname
        self.lastName = lname
        self.username = un
        self.password = pw
        self.email = em
        self.gradYear = gy
        self.academy = a
        self.jobTitle = job
        self.company = comp
        
mutableProperties = ['firstName', 'lastName', 'email', 'gradYear', 'academy', 'jobTitle', 'company']
    



def getUsername(i):
    """
    Given user i, return the username
    """
    
    u = str(i)
    ind = u.find('username')
    u = u[ind+13:]
    end = u.find(',')
    u = u[:end-1]
    return u




def getProperty(i, p):
    """
    Given user i and property p, return the desired property.
    For example, getProperty(user1, 'firstName') will return the value of property firstName for user1.
    """
    
    s = str(i)
    ind = s.find(p)
    s=s[ind+len(p)+4:]
    end=s.find(',')
    s=s[:end-1]
    if p == "academy":
        s = s.upper()
    return s



def equalProperties(uname, prop, val):
    """
    Return true if property prop is already equal to val.
    Uname, prop, and val are all strings.
    """
    
    old = getProperty(security.getUser(uname), prop)
    if prop == "academy":
        old = old.lower()
    return old == val.lower()






def updateAccount(uname, fname, lname, em, gy, acad, job, com):
    security.updateProperty(uname, 'firstName', fname)
    security.updateProperty(uname, 'lastName', lname)
    security.updateProperty(uname, 'email', em)
    security.updateProperty(uname, 'gradYear', gy)
    security.updateProperty(uname, 'academy', acad)
    security.updateProperty(uname, 'jobTitle', job)
    security.updateProperty(uname, 'company', com)






    



