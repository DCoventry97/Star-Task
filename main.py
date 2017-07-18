from tkinter import *
from database import Db
from Task import Task
db = Db()
root = Tk()
root.title("Star Task")
root.minsize(250, 200)

#adds a new task to the database and calls main again
def makeNewTask(text):
    db.addTask(text)
    root.after(0, main)

#removes the task from the GUI and calls main again
def destroyTask(taskObject):
    taskObject.deleteTask(db)
    for child in root.winfo_children():
        child.destroy()

    root.after(0, main)

def main():
    #creates the text entry box for adding a new task and button for adding the task
    taskEntry = Entry(root)
    taskEntry.grid(row = 0, column = 0, padx = 10)
    newTaskButton = Button(root, text = "Add Task", command = lambda: makeNewTask(taskEntry.get())) 
    newTaskButton.grid(row = 0, column = 1, padx = 10)
    
    #checks if the database is not empty
    if not db.checkIfEmpty():
        #gets all the tasks in the database, makes a task object with them and then adds them to an array
        taskTextList = db.getAllTasks()
        listCounter = 0
        taskList = []
        for taskText in taskTextList:
            task =Task(taskText, Label(root, text = taskText), Button(root, text = "Task Complete", command =lambda position = listCounter: destroyTask(taskList[position]) ), db) 
            taskList.append(task)
            listCounter += 1
        #task array is used to draw the task label and button to remove task from the program
        for i in range(0,db.rowCount()):
            taskList[i].taskLabel.grid(row = i + 1, column = 0, padx = 5)
            taskList[i].taskButton.grid(row = i + 1, column = 1)        
    root.mainloop()

main()
