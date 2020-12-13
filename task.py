from flask import Flask, render_template, url_for, request, redirect
from flask_mongoengine import MongoEngine
from datetime import datetime

import mongoengine as me
app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {                              #connection to databse
    'db' : 'mydb',
    'host' : 'localhost',
    'port' : 27017
}

db = MongoEngine()
db.init_app(app)                                                #creates the object of database connection


class Task(me.Document):                                        #creating database model
    content = me.StringField(max_length=200, required=True)
    created_on = me.DateTimeField(default=datetime.utcnow())


@app.route('/', methods=['POST', 'GET'])                       #default routing function
def index():
    if request.method == 'POST':                               #if method is POST
        task_content = request.form['content']                 #get the data from form  and
        new_task = Task(content=task_content)                  #create new object to store data

        try:
            new_task.save()                                    #push this newly created object into database
            return redirect('/')                               #redirect request to index page
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Task.objects()                                  #if request is GET, get all the data from database and store it into tasks variable
        return render_template('index.html', tasks=tasks)       #show all the data on index page

@app.route('/delete/<id>')                                      #deleting task by id
def delete(id):
    try:
        Task.objects.get(id = id).delete()                      #deleting task from databse
        return redirect('/')                                    #redirect request to index page
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<id>', methods=['POST', 'GET'])             #updating stored task by id
def update(id):
    task = Task.objects.get(id = id)                            #getting task from database using id

    if request.method == 'POST':                                #if method is POST then
        task.content = request.form['content']                  #getting new content from form and set into databse

        try:
            task.save()                                         #save updated object in database
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)        #if method is GET then redirect requet to update page to get the new content



if __name__=='__main__':
    app.run(debug = True)