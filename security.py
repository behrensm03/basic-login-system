import sqlite3
from passlib.hash import pbkdf2_sha256
import bcrypt, account
from account import *

from pymongo import MongoClient
client = MongoClient()

db = client.pymongo_test

users = db.users





def login(input_username, input_password):
    """
    Given username and password, attempts to log in. If credentials are correct, returns True. If login fails, returns False.
    """
    
    if (not (userExists(input_username))):
        return False
    else:
        user_info = str(getUser(input_username))
        ind = user_info.find('password')
        password = user_info[ind+13:]
        end = password.find(',')
        p2 = password[:end-1]
        check_hash = bcrypt.hashpw(input_password.encode('utf8'), p2.encode('utf8')).decode('utf8')
        if (check_hash == p2):
            return True
        else:
            return False
    



def register(un, pw, c):
    """
    Checks criteria with validRegister() first and returns if invalid.
    If valid, adds username un and hashed version of password pw to database.
    """
    
    if (not validRegister(un, pw, c)):
        return
    password_hash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    new_user = {
        'username': un.encode('utf8'),
        'password': password_hash
    }
    users.insert_one(new_user)
    return
        


def registerV2(a, pw, c):
    """
    Checks criteria with validRegister() and returns if invalid.
    Adds a.username and hashed password to database.
    """
    
    if ((not isinstance(a, account.Account)) or (not validRegister(a.username, pw, c))):
        return
    password_hash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    users.insert_one(userToDict(a, pw))
    return
    



def userToDict(a, pw):
    """
    Returns dictionary representation of Account a using hashed version of password pw.
    """
    
    if (not isinstance(a, account.Account)):
        return
    password_hash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    new_user = {
        'username': a.username.encode('utf8'),
        'password': password_hash,
        'firstName': a.firstName,
        'lastName': a.lastName,
        'email': a.email,
        'gradYear': a.gradYear,
        'academy': a.academy,
        'jobTitle': a.jobTitle,
        'company': a.company
    }
    return new_user



def userExists(u):
    """
    Returns True if username exists in database, False otherwise.
    """
    
    find = users.find_one({'username': u.encode('utf8')})
    if (find == None):
        return False
    else:
        return True



def getUser(u):
    """
    Return the user given a username u.
    """
    find = users.find_one({'username': u.encode('utf8')})
    return find



def passwordsMatch(p1, p2):
    """
    Returns true if passwords p1 and p2 are equal, false otherwise.
    """
    
    return (p1 == p2)





def validUsername(u):
    """
    Returns True if username u is valid, false otherwise.
    Criteria for valid username: Must be at least 4 characters long.
    """
    
    if (len(u) < 4):
        return False
    else:
        return True





def hasNumber(p):
    """
    Returns true if p contains a number, false if contains no numbers (digits).
    """
    
    return any(char.isdigit() for char in p)




def validPassword(p):
    """
    Return true if p contains a number and is at least 8 characters long.
    """
    
    if ((len(p) >= 8) and hasNumber(p)):
        return True
    else:
        return False



    
    

def validRegister(un, pw, c):
    """
    Returns True if all criteria for registering a new account are met, False otherwise.
    Criteria: Username does not exist, Username is valid, Password is valid, Passwords match.
    """
    
    if (userExists(un) or validUsername(un)==False or validPassword(pw)==False or passwordsMatch(pw, c)==False):
        return False
    else:
        return True





def registerError(un, pw, c):
    """
    For use when it is known that validRegister() returns False.
    Determines which criteria are not met and adds the correct error messages together and returns the full error message.
    """
    
    error=""
    if (userExists(un)):
        error=error+"Username is taken. Please choose another."
    if (validUsername(un)==False):
        error=error+" Username must contain at least 4 characters."
    if (validPassword(pw)==False):
        error=error+" Password must contain at least 8 characters and at least 1 number."
    if (passwordsMatch(pw, c)==False):
        error=error+" Passwords do not match."
    return error



def updatePassword(u, new, c):
    """
    If this combination is valid for the change, hashes the new password and updates the password field in db.
    Returns true if successful, false otherwise.
    """
    
    if validChange(u, new, c):
        new_hash = bcrypt.hashpw(new.encode('utf8'), bcrypt.gensalt())
        users.update({'username': u.encode('utf8')}, {'$set':{'password': new_hash}})
        return True
    else:
        return False



def validChange(u, pw, c):
    """
    Returns true if this combination of username, password, and password confirmation is a valid combination to change the password.
    Checks for username existing, valid password, passwords matching, and that the new password is different from the old.
    """
    
    if (not userExists(u)) or (not passwordsMatch(pw, c)) or (not validPassword(pw)) or (login(u, pw)):
        return False
    else:
        return True


def updateProperty(uname, prop, val):
    """
    Updates property prop to val for user uname.
    """
    if (prop == 'academy' and val == 'NONE'):
        return
    elif (not account.equalProperties(uname, prop, val)) and (prop in account.mutableProperties) and (not val == "") and (userExists(uname)):
        users.update({'username': uname.encode('utf8')}, {'$set':{prop: val}})










# users.delete_many({})