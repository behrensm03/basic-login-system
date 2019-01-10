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
        
    
    # def toDictionary(self):
    #     #password_hash = bcrypt.hashpw(self.password, bcrypt.gensalt())
    #     d = {
    #         'username': self.username.encode('utf8'),
    #         'password': self.password,
    #         'firstName': self.firstName,
    #         'lastName': self.lastName,
    #         'email': self.email,
    #         'gradYear': self.gradYear,
    #         'academy': self.academy,
    #         'jobTitle': self.jobTitle,
    #         'company': self.company
    #     }
    #     return d


def getUsername(i):
    u = str(i)
    ind = u.find('username')
    u = u[ind+13:]
    end = u.find(',')
    u = u[:end-1]
    return u

def getProperty(i, p):
    s = str(i)
    ind = s.find(p)
    s=s[ind+len(p)+4:]
    end=s.find(',')
    s=s[:end-1]
    if p == "academy":
        s = s.upper()
    return s




