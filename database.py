import sqlite3

class Db:
    #creates the db when object is initialised
    def __init__(self):
        self.connectDb()
        self.nextId = self.currentMaxId() + 1

    #makes db tables in needed, and connects to the db file and its tables
    def connectDb(self):
        self.dbConnetion = sqlite3.connect("ToDo.db")
        self.cursor = self.dbConnetion.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, task TEXT)")

        #adds a new task to db in tasks table, returns the taskid
    def addTask(self, taskText):
        self.cursor.execute("INSERT INTO tasks(id, task) VALUES (?, ?)", (self.nextId, taskText))
        self.dbConnetion.commit()
        self.nextId += 1
        return self.nextId - 1
    
    #removes a task from tasks table using the taskid
    def removeTask(self, taskId):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskId,))
        self.dbConnetion.commit()

    #counts the number of rows in the table 
    def rowCount(self):
        self.cursor.execute("SELECT * FROM tasks")
        count = 0
        for row in self.cursor.fetchall():
            count += 1
        return count
    
    #returns the largest id in the database
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

    #checks if the db is empty    
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
           