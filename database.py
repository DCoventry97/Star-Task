import sqlite3

class Db:
    #creates the db when object is initialised
    def __init__(self):
        self.connectDb()
        self.nextId = self.currentMaxId() + 1
        self.catId = self.maxcatId() + 1
        self.addNoneCategory()

    #makes db tables in needed, and connects to the db file and its tables for tasks and categories
    def connectDb(self):
        self.dbConnetion = sqlite3.connect("ToDo.db")
        self.dbConnetion.execute("PRAGMA foreign_keys = 1")
        self.cursor = self.dbConnetion.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS category(id INTEGER PRIMARY KEY, categoryText TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, task TEXT, category TEXT)")
        
    
    #adds none to the category table so that user can add a task with no category connected to it
    def addNoneCategory(self):
        if not (self.categoryExists("None")):
            self.addCategory("None")

    # adds a new category to the category table
    def addCategory(self, categoryText):
        self.cursor.execute("INSERT INTO category(id, categoryText) VALUES (?, ?)", (self.catId, categoryText))
        self.catId += 1
        self.dbConnetion.commit()

        #adds a new task to db in tasks table, returns the taskid
    def addTask(self, taskText, taskCat = None):
        self.cursor.execute("INSERT INTO tasks(id, task, category) VALUES (?, ?, ?)", (self.nextId, taskText, taskCat))
        self.dbConnetion.commit()
        self.nextId += 1
        return self.nextId - 1
    
    #removes a task from tasks table using the taskid
    def removeTask(self, taskId):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskId,))
        self.dbConnetion.commit()

    #removes category from db using category text 
    def removeCategory(self, catText):
        self.cursor.executemany("DELETE FROM category WHERE categoryText=?", (catText,))
        self.dbConnetion.commit()

    #counts the number of rows in tasks the table 
    def rowCount(self):
        self.cursor.execute("SELECT * FROM tasks")
        count = 0
        for row in self.cursor.fetchall():
            count += 1
        return count
    
    #returns the number of rows in the category table
    def catRowCount(self):
        self.cursor.execute("SELECT * FROM category")
        count = 0
        for row in self.cursor.fetchall():
            count += 1
        return count
    
    #returns all categories in category table
    def getAllCategories(self):
        self.cursor.execute("SELECT categoryText FROM category")
        return self.cursor.fetchall()

    #returns the largest id in the catagory table
    def maxcatId(self):
        self.cursor.execute("SELECT id FROM category")
        id = self.cursor.fetchall()
        if (self.catRowCount() == 0):
            return 0
        else:
            return id[-1][0]


    #returns the largest id in the tasks table
    def currentMaxId(self):
        self.cursor.execute("SELECT id FROM tasks")
        id = self.cursor.fetchall()
        if (self.rowCount() == 0):
            return 0
        else:
            return id[-1][0]

    #disconects program from db
    def disconectDb(self):
        self.cursor.close()
        self.dbConnetion.close()
    
    #returns task text using its taskid
    def getTask(self, taskId):
        self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskId,))
        task = self.cursor.fetchall()
        return task[0][0]

    #checks if the tasks table is empty    
    def checkIfEmpty(self):
        return (self.rowCount() == 0)
    
    #returns a list of all tasks in tasks in the db
    def getAllTasks(self):
        taskList = []
        self.cursor.execute("SELECT task FROM tasks")
        for row in self.cursor.fetchall():
            taskList.append(row[0])
        
        return taskList

    #returns the taskid of a task in tasks using the text of the task
    def getTaskId(self, taskText):
        self.cursor.execute("SELECT id FROM tasks WHERE task=?", (taskText,))
        value = self.cursor.fetchall()
        return value[0][0]
    
    #checks if the task exists, returns a boolean
    def taskExists(self, taskText):
        self.cursor.execute("SELECT task FROM tasks WHERE task=?", (taskText,))
        task = self.cursor.fetchall()
        return (taskText == task[0][0])
    
    #returns boolean if category exists in category table
    def categoryExists(self, category):
        self.cursor.execute("SELECT categoryText FROM category WHERE categoryText=?", (category,))
        return (self.cursor.fetchall() != []) 

    #get the category associated with a task       
    def getTaskCat(self, id):
        self.cursor.execute("SELECT category FROM tasks WHERE id=?",(id,))
        return self.cursor.fetchall()[0][0]
