# Imports necessary modules
# You will need to install pywebview https://pywebview.flowrl.com/guide/installation.html
# For Video Reference and Testing see main directory
# Since trying to avoid a cumbersome download I have since decided to attempt to host on heroku so pywebview is no longer needed

# Features:
# Links to switch between the two pages
# Standalone application
#
# Login Page
#   Uses Pixellation to reference how strong your password is
#   Checks whether the username, password and email address is in database
#   Redirects user to login page if non of the above is provided
#
# Sign Up Page
#   Uses Pixellation to reference how strong your password isUses Pixellation to reference how strong your password is
#   Tells user how strong their password is: bad, weak, okay, good, strong
#   If the email address already exists in database it redirects them to the login page
#   All fields must be filled out for the credentials.txt file to be updated
#
# General Robust Error handling, ie. checks whether port is already open and then closes it
#
# Skills Used:
# Threading - no longer used after ommiting pywebview
# Functions
# File handling

#import sys
import os
from bottle import Bottle, get, static_file, run, route, template, request, redirect
#import time


# Not Built-in modules, use local pacakge and append(insert) new system path variable
# e.g. (pytjon3 -m) pip install <package> -t <directory>


'''
import os
import signal
import subprocess
from subprocess import Popen, PIPE
'''

        
# FlowChart:
'''

Login - Enter Credentials
Check: Email Exists
    if Exists:
        Return you have already got an account
    else:
        create account

'''
# Create a function to run the main code so that it can be threaded later



def countCredentials():
    fname = "Credentials.txt"
    global count
    count = 0
    with open(fname, 'r') as f:
        for line in f:
            count += 1
    print("Total number of lines is:", count)
                           
            
# Defines location of all static files
@get("/static/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="static/css")

@get("/static/font/<filepath:re:.*\.(eot|otf|svg|ttf|woff|woff2?)>")
def font(filepath):
    return static_file(filepath, root="static/font")

@get("/static/img/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="static/img")

@get("/static/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="static/js")


# Defining Routes
@route('/')
def index():
    # Looks inside view folder for .tpl
    return template('index') # I can pass variables to template like, name = "Aiyush"

@route('/login')
def login():
    return template('login') 



# Implementing forms
@route('/loginCheck', method='POST')
def passwordCheck():

    name = request.forms.get('name')
    email = request.forms.get('email')
    password = request.forms.get('password')
    print (" [SUCCESSFULL] - Credentials: ")
    print (name)
    print (email)
    print (password)

    def checkCredentials(name, email, password):
        countCredentials()
        file = open("Credentials.txt", "r")

        line = file.readline()
        counter = 0
        content = file.read()
        contentList = content.split("\n")

        nameFound = False
        emailFound = False
        passwordFound = False
        
        for x in range(0, count -1):
            namePos = 0
            emailPos = 1
            passwordPos = 2
            positionOfPassword = 1
            positionOfEmail = 2

            # Check Whether Email is present
            nameOnly = ((str(contentList[x]).split(sep = ",")[namePos]).strip())
            emailOnly = ((str(contentList[x]).split(sep = ",")[emailPos]).strip())
            passwordOnly = ((str(contentList[x]).split(sep = ",")[passwordPos]).strip())

            # Check if the name is in database

            if positionOfPassword != positionOfEmail:
                print ("[EMAIL]",email)
                if email == emailOnly:
                    emailFound = True
                    positionOfEmail = x

                    print ("[PASSWORD]",password)
                    if password == passwordOnly:
                        passwordFound = True
                        positionOfPassword = x
                        break

        if emailFound:
            if passwordFound:
                print ("Both found")

                if positionOfPassword == positionOfEmail:
                    redirect('https://www.agsb.co.uk')

        else:
            print ("Credentials not found, awwww :(")
            redirect('/')

    checkCredentials(name, email, password)
    
@route('/passwordCheck', method='POST')
def passwordCheck():

    def checkExists(email):
        # This function checks if the email address is already in the database
        global emailDetected
        emailDetected = False
        countCredentials()
        file = open("Credentials.txt", "r")

        line = file.readline()
        counter = 0
        content = file.read()
        contentList = content.split("\n")

        # Prints emails in range
        for x in range(0,count-1):
            emailPos = 1
            emailOnly =  ((str(contentList[x]).split(sep = ",")[emailPos]).strip())
            print (emailOnly)

            if emailOnly == email:
                emailDetected = True

        if emailDetected == True:
            print ("[Email Exists Already]")
            redirect('/')
            

            
        file.close()
                    
    name = request.forms.get('name')
    email = request.forms.get('email')
    password = request.forms.get('password')
    print (" [SUCCESSFULL] - Credentials: ")
    print (name)
    print (email)
    print (password)

    checkExists(email)
        
    def allAttributes(name, email, password):
        # Check if all the form is filled in (email, username and password)
        allExist = False

        if 'name' in locals() and 'email' in locals() and 'password' in locals():
            allExist = True
            print ("allExist =",allExist)
            # Next call function to add to database

        else:
            allExist = False
            print ("allExist =",allExist)
            redirect('/')
            
    allAttributes(name, email, password)


    def addDatabase(name, email, password):
        newCredentials = []
        newCredentials.append(name)
        newCredentials.append(email)
        newCredentials.append(password)
        
        file = open("Credentials.txt", "a+")
        for item in newCredentials:
            file.write(item + ",")
        file.write("\n")
        file.read()
        print("Added new credentials",str(newCredentials))
        
    print('Finished Checking Existing Database [COMPLETE] ')
    # Do something with variables here

    addDatabase(name, email, password)
    return template('login')




    
# Method to run the bottle server
# If local run on port 8080 else run on heroku 
if os.environ.get('APP_LOCATION') == 'heroku':
    run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    run(host='localhost', port=8080, debug=True)



