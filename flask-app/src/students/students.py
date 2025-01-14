from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


students = Blueprint('students', __name__)

# View a student profile
@students.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    cursor = db.get_db().cursor()

    cursor.execute(f'SELECT * FROM Students WHERE student_id={student_id}')
    
    column_headers = [x[0] for x in cursor.description]

    json_student_data = []

    student_data = cursor.fetchall()

    for row in student_data:
        json_student_data.append(dict(zip(column_headers, row)))

    response = jsonify(json_student_data)

    return response

# View all of a student's folders
@students.route('/students/<student_id>/studentfolders', methods=['GET'])
def get_specific_student_student_folders(student_id):
    cursor = db.get_db().cursor()

    cursor.execute(f'SELECT * FROM StudentFolders WHERE student_id={student_id}')
    
    column_headers = [x[0] for x in cursor.description]

    json_folder_data = []

    folder_data = cursor.fetchall()

    for row in folder_data:
        json_folder_data.append(dict(zip(column_headers, row)))

    response = jsonify(json_folder_data)

    return response

# Add a student folder
@students.route('/students/<student_id>/studentfolders', methods=['POST'])
def add_new_student_folder(student_id):

    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    name = the_data['folder_name']

    # Constructing the query
    query = f'INSERT INTO StudentFolders (folder_name, student_id) values ({name}, {student_id})'

    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = jsonify('Student folder created')
    
    return response

# View contents of a specific student folder
@students.route('/students/<student_id>/studentfolders/<folder_name>', methods=['GET'])
def get_notes_in_student_folder(student_id, folder_name):
    cursor = db.get_db().cursor()

    cursor.execute(f'SELECT * FROM StudentFolders WHERE student_id={student_id} AND folder_name = {folder_name}')
    
    column_headers = [x[0] for x in cursor.description]

    json_folder_data = []

    folder_data = cursor.fetchall()

    for row in folder_data:
        json_folder_data.append(dict(zip(column_headers, row)))

    response = jsonify(json_folder_data)

    return response


# Add a note to a specific student folder
@students.route('/students/<student_id>/studentfolders/<folder_name>', methods=['POST'])
def add_note_to_student_folder(student_id, folder_name):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    note_id = the_data['note_id']

    # Constructing the query
    query = f'''UPDATE Notes
                SET student_folder = {folder_name}
                WHERE student_id = {student_id} AND note_id = {note_id}'''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = jsonify('Note added to student folder')
    
    return response

# Delete a specific student folder
@students.route('/students/<student_id>/studentfolders/<folder_name>', methods=['DELETE'])
def delete_student_folder(student_id, folder_name):
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # Constructing the query
    query = f'''DELETE FROM StudentFolders
                WHERE student_id = {student_id} AND folder_name = {folder_name}'''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = jsonify('Student folder deleted')
    
    return response
