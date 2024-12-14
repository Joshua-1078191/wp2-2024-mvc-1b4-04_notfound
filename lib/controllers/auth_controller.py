from flask import render_template, request, redirect, session, url_for, flash
from lib.database.db import get_db

def login():
    if 'user_id' in session:
        return redirect('/')
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Please enter both email and password', 'error')
            return render_template("login.html.jinja")
        
        conn = get_db()
        try:
            # First check if email exists
            user = conn.execute('SELECT * FROM users WHERE login = ?', (email,)).fetchone()
            
            if not user:
                flash('No account found with this email', 'error')
                return render_template("login.html.jinja")
            
            # Then check if password matches
            user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', 
                              (email, password)).fetchone()
            
            if not user:
                flash('Incorrect password', 'error')
                return render_template("login.html.jinja")
            
            session['user_id'] = user['user_id']
            session['display_name'] = user['display_name']
            session['is_admin'] = user['is_admin']
            return redirect('/')
            
        except Exception as e:
            flash('An error occurred while logging in', 'error')
        finally:
            conn.close()
    
    return render_template("login.html.jinja")

def sign_up():
    if 'user_id' in session:
        return redirect('/')
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template("sign_up.html.jinja")
            
        display_name = email.split('@')[0]
        
        conn = get_db()
        try:
            # Check if email already exists
            existing_user = conn.execute('SELECT * FROM users WHERE login = ?', (email,)).fetchone()
            if existing_user:
                flash('Email already registered', 'error')
                return render_template("sign_up.html.jinja")
            
            conn.execute('INSERT INTO users (login, password, display_name, is_admin) VALUES (?, ?, ?, ?)',
                        (email, password, display_name, 1))
            conn.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect('/index/login')
        except Exception as e:
            flash('An error occurred while creating your account', 'error')
        finally:
            conn.close()
    
    return render_template("sign_up.html.jinja")

def logout():
    session.clear()
    return redirect('/index/login')
