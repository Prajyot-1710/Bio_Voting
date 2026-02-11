from flask import Flask
from flask import Flask, jsonify, request, render_template
from flask_session import Session

import json
import sys

from flask import Flask, flash, redirect, render_template, \
     request, url_for ,session

from datetime import datetime

import sqlite3 as sql

from tkinter import * 
from tkinter import messagebox 
import tkinter as tk

node = Flask(__name__)
node.config['SESSION_TYPE'] = 'vote'
node.config['SECRET_KEY'] = 'india'

sess = Session()


@node.route('/')
def  first():
    return  render_template('index.html')

@node.route('/elogin', methods=['POST'])
def  elogin():
    error = None
    if  request.method  ==  'POST':
        username=request.form['username']
        password=request.form['password']
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from eofficer where username='"+username+"' and password='"+password+"'"
        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
            
            error  =  'Invalid  username  or  password.  Please  try  again  !'
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", error) 
            root.destroy()
            
        else:
            return  render_template('Emenu.html')
            
    return  render_template('Eoff.html')


@node.route('/blogin', methods=['POST'])
def  blogin():
    error = None
    if  request.method  ==  'POST':
        username=request.form['username']
        password=request.form['password']
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from boothofficer where uasername='"+username+"' and password='"+password+"'"
        cur.execute(statement)
        if not cur.fetchone():  # An empty result evaluates to False.
            print("Login failed")
            error  =  'Invalid  username  or  password.  Please  try  again  !'
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", error) 
            root.destroy()
            
        else:
            return  render_template('StartVote.html')
            
    return  render_template('Boff.html')


@node.route('/div2eoff')
def  div2eoff():
    return  render_template('eoff.html')

@node.route('/div2voting')
def  div2voting():
    return  render_template('voting.html')


@node.route('/logout')
def  logout():
    return  render_template('index.html')




@node.route('/div2boff')
def  div2boff():
    return  render_template('boff.html')

@node.route('/div2voter')
def  div2voter():
    return  render_template('newvoter.html')

@node.route('/div2cand')
def  div2cand():
    return  render_template('candidate.html')

@node.route('/div2bak')
def  div2bak():
    return  render_template('Emenu.html')

@node.route('/div2Emenu')
def  div2Emenu():
    return  render_template('Emenu.html')

@node.route('/div2Bmenu')
def  div2Bmenu():
    return  render_template('StartVote.html')


@node.route('/addvoter', methods=['POST'])
def  addvoter():
    report = None
    if  request.method  ==  'POST':

        con = sql.connect("vote.db")
        cur = con.cursor()

        votername=request.form['votername']
        voterid=request.form['voterid']
        age=request.form['age']
        area=request.form['area']
        city=request.form['city']
        txtIsoTemplate=request.form['txtIsoTemplate']
        gender=request.form['gender']

        print(len(txtIsoTemplate))

        # if len(txtIsoTemplate)==1:
        #
        #     report="Finger Not Scanned , Scan and Try again"
        #     root = tk.Tk()
        #     root.withdraw()
        #     root.call('wm', 'attributes', '.', '-topmost', True)
        #     messagebox.showinfo("Info", report) 
        #     root.destroy()            
        #     return  render_template('newvoter.html')
        

        records = [(voterid,votername, age,area,city,txtIsoTemplate,"NV",gender)]

        print(records)


        
        cur.executemany('INSERT INTO voter VALUES(?,?,?,?,?,?,?,?);',records);

        con.commit()
        report="Voter added"
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", report) 
        root.destroy()

        return  render_template('newvoter.html')



@node.route('/delVoter', methods=['POST'])
def  delVoter():
    report = None
    if  request.method  ==  'POST':

        con = sql.connect("vote.db")
        cur = con.cursor()

        
        voterid=request.form['voteid']
        
        statement = "delete from voter where voterid='"+voterid+"'"
        cur.execute(statement)

        con.commit()
        report="Voter Deleted"
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", report) 
        root.destroy()

        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from voter"
        cur.execute(statement)
        data = cur.fetchall()
        con.commit()
    
        return  render_template('Voterlist.html',  data  =  data)
        
    
@node.route('/voterlist')
def  voterlist():

    con = sql.connect("vote.db")
    cur = con.cursor()
    statement = "select * from voter"
    cur.execute(statement)
    data = cur.fetchall()
    con.commit()
    
    return  render_template('Voterlist.html',  data  =  data)



@node.route('/searchvoter', methods=['POST'])
def  searchvoter():
    if  request.method  ==  'POST':

        voterid=request.form['voterid']
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from voter where voterid='"+voterid+"'"
        cur.execute(statement)
        data = cur.fetchall()
        con.commit()
        print(data)

        if len(data)==0:
            report="Voter Not Found"
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", report) 
            root.destroy()
            return  render_template('voting.html')
        
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from voter where voterid='"+voterid+"' and status='NV'"
        cur.execute(statement)
        data = cur.fetchall()
        con.commit()

        if len(data)==0:
            report="Already Voted"
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", report) 
            root.destroy()
            return  render_template('voting.html')        
        
        session["voterid"] = voterid
        return  render_template('voting.html',  code  =  data[0][5],code2  =  data[0][1])

        
            

@node.route('/searcheoff', methods=['POST'])
def  searcheoff():
    if  request.method  ==  'POST':

        username=request.form['username']
        password=request.form['password']
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from eofficer where username='"+username+"' and password='"+password+"'"

        print(statement)
        cur.execute(statement)
        data = cur.fetchall()
        con.commit()
        
        if len(data)==0:  # An empty result evaluates to False.
            print("Login failed")
            
            error  =  'Invalid  username  or  password.  Please  try  again  !'
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", error) 
            root.destroy()
            return  render_template('eoff.html')
        
        return  render_template('eoff.html',  code  =  data[0][2])



@node.route('/searchboff', methods=['POST'])
def  searchboff():
    if  request.method  ==  'POST':

        username=request.form['username']
        password=request.form['password']
        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "select * from boothofficer where uasername='"+username+"' and password='"+password+"'"

        print(statement)
        cur.execute(statement)
        data = cur.fetchall()
        con.commit()
        
        if len(data)==0:  # An empty result evaluates to False.
            print("Login failed")
            
            error  =  'Invalid  username  or  password.  Please  try  again  !'
            root = tk.Tk()
            root.withdraw()
            root.call('wm', 'attributes', '.', '-topmost', True)
            messagebox.showinfo("Info", error) 
            root.destroy()
            return  render_template('boff.html')
        
        return  render_template('boff.html',  code  =  data[0][2])





    
@node.route('/addcandidate', methods=['POST'])
def  addcandidate():
    report = None

    
    if  request.method  ==  'POST':

        
        con = sql.connect("vote.db")
        cur = con.cursor()

        cname=request.form['cname']
        party=request.form['party']
        symbol="../static/images/"+request.form['symbol']

        records = [(cname,party, symbol,0)]

        print(records)
        
        cur.executemany('INSERT INTO Candidate VALUES(?,?,?,?);',records);

        con.commit()
        report="Candidate added"
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", report) 
        root.destroy()

        return  render_template('candidate.html')

@node.route('/candlist')
def  candlist():

    con = sql.connect("vote.db")
    cur = con.cursor()
    statement = "select * from candidate"
    cur.execute(statement)
    data = cur.fetchall()

    print(data)
    return  render_template('candlist.html',  data  =  data)


@node.route('/votechart')
def  votechart():

    con = sql.connect("vote.db")
    cur = con.cursor()
    statement = "select * from candidate"
    cur.execute(statement)
    data = cur.fetchall()

    print(data)
    return  render_template('votechart.html',  data  =  data)

@node.route('/result')
def  result():

    con = sql.connect("vote.db")
    cur = con.cursor()
    statement = "select * from candidate"
    cur.execute(statement)
    data = cur.fetchall()

    print(data)
    return  render_template('result.html',  data  =  data)

@node.route('/winner')
def  winner():

    con = sql.connect("vote.db")
    cur = con.cursor()
    
    statement = "SELECT * FROM candidate WHERE votes = (SELECT Max(votes) FROM candidate)" 
    cur.execute(statement)
    data = cur.fetchall()
    print(data)
    report="Winner is "+data[0][0]+" with votes "+str(data[0][3])
    

    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    messagebox.showinfo("Info", report) 
    root.destroy()

    
    return  render_template('emenu.html')


@node.route('/resedata')
def  resedata():

    con = sql.connect("vote.db")
    cur = con.cursor()
    
    statement = "update candidate set votes =0"
    cur.execute(statement)
    con.commit()

    statement = "update Voter set status ='NV'"
    cur.execute(statement)
    con.commit()


    root = tk.Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    messagebox.showinfo("Info", "Done!!") 
    root.destroy()
    
    return  render_template('emenu.html')


@node.route('/castvote', methods=['POST'])
def  castvote():
    
    if  request.method  ==  'POST':      
        cname=request.form['cname']
        party=request.form['party']
        report="You Casted Vote for "+cname+"-"+party

        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "update Candidate set votes=votes+1 where Cname='"+cname+"'"
        cur.execute(statement)
        con.commit()

        con = sql.connect("vote.db")
        cur = con.cursor()
        statement = "update Voter set status='V' where voterid='"+session["voterid"]+"'"
        cur.execute(statement)
        con.commit()

         
        
        ##print(report)
        root = tk.Tk()
        root.withdraw()
        root.call('wm', 'attributes', '.', '-topmost', True)
        messagebox.showinfo("Info", report) 
        root.destroy()
        return  render_template('voting.html')

if __name__== '__main__':

    if len(sys.argv) >= 2:
        port = sys.argv[1]
    else:
        port = 8000

    node.run(host='127.0.0.1', port=port)
