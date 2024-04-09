from flask import (
  Flask,
  redirect,
  url_for,
  render_template,
  request,  # for receiving data
  jsonify,  # for sending data as json
  flash,
)
import sqlite3  # for the database
from datetime import date

#End

app = Flask(__name__)
#The API implementation task as mentioned in the application requirements
app.secret_key = 'dvcdsvcsducvsducsvccysgcdcdfuwu'  # Replace with your secret key

#creating tables
db = sqlite3.connect('flask.db')  # flask.db is the filename
cursor = db.cursor()  # create a cursor object
cursor.execute('CREATE TABLE IF NOT EXISTS todolist (\
ID INTEGER PRIMARY KEY AUTOINCREMENT, \
description TEXT, \
done INTEGER DEFAULT 0, \
date TEXT NOT NULL)')
db.commit()  # save changes
db.close()


#End
#function has two arguments, cmd is the sql command, vals is any values (to prevent SQL injection) and defaults to None.
def sql(cmd, vals=()):
  conn = sqlite3.connect('flask.db')
  cur = conn.cursor()
  cur.execute(cmd, vals)
  conn.commit()

  if "SELECT" in cmd:  # Check if it's a SELECT query
    columns = [column[0] for column in cur.description]
    data = [dict(zip(columns, row)) for row in cur.fetchall()]
    conn.close()
    return data if data else None
  else:
    conn.close()
    return None  # Return None for non-SELECT queries


#HOME
@app.route('/')
def index():

  data = sql('SELECT * FROM todolist order by id desc')
  #return jsonify(data)
  return render_template('dashboard.html', data=data)


#ADD
@app.route('/add', methods=['POST'])
def add():
  Date = date.today().isoformat()
  done = False
  sql(
    'INSERT INTO todolist (description, done, date) VALUES (?, ?, ?)',
    (
      request.form['description'], done, Date
      #request.form.get('email'),
      #request.form['description'],
    ))
  return redirect(url_for("index"))


#UPDATE
@app.route('/update/<int:todo_id>')
def update(todo_id):
  # Retrieve the existing task from the database
  existing_task = sql('SELECT * FROM todolist WHERE ID = ?', (todo_id, ))

  if not existing_task:
    flash('Task not found. Update failed.', 'error')
    return redirect(url_for("index"))

  # Get the current status (done) of the task
  current_status = existing_task[0]['done']

  # Toggle the status (if current status is False, set to True, and vice versa)
  new_status = not current_status

  # Update the task in the database with the new status
  sql('UPDATE todolist SET done = ? WHERE ID = ?', (new_status, todo_id))

  flash('Task updated successfully!', 'success')
  return redirect(url_for("index"))


#DELETE
@app.route('/delete/<int:todo_id>')
def delete(todo_id):
  # Check if the task exists in the database
  existing_task = sql('SELECT * FROM todolist WHERE ID = ?', (todo_id, ))

  if not existing_task:
    flash('Task not found. Deletion failed.', 'error')
  else:
    # Delete the task from the database
    sql('DELETE FROM todolist WHERE ID = ?', (todo_id, ))
    flash('Task deleted successfully!', 'success')

  return redirect(url_for("index"))


@app.route('/list')
def list():
  data = sql('SELECT * FROM todolist')
  return jsonify(data)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
#app.run(host='0.0.0.0', port=81)
