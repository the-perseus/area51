from flask import Blueprint, render_template, request, flash, jsonify #import
from flask_login import login_required, current_user #for logged in status, current_user give infos about user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__) #name of blueprint


@views.route('/', methods=['GET', 'POST']) #URL to route -> root
@login_required #make sure can not go to home if not logged in
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') #check length of the note
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note. pass the note to db for note+user.
            db.session.add(new_note) #adding the note to the database 
            db.session.commit() #commit
            flash('Note added!', category='success') #message confirmation

    return render_template("home.html", user=current_user) #call the home.html


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId) #find the note in the db
    if note: #if note exists
        if note.user_id == current_user.id: #and if note and user match, then allow only to delete
            db.session.delete(note)
            db.session.commit()

    return jsonify({}) #empty response because something need to return in flask
