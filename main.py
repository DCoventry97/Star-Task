from tkinter import *
from database import Db
from Task import Task
db = Db()
root = Tk()
root.title("Star Task")
minWindowX = 220
minWindowY = 200
root.minsize(minWindowX, minWindowY)

#adds a new task to the database and calls main again
def makeNewTask(text, windowObject):
    db.addTask(text)
    windowObject.destroy()
    root.after(0, main)

#removes the task from the GUI and calls main again
def destroyTask(taskObject):
    taskObject.deleteTask(db)
    for child in root.winfo_children():
        child.destroy()
    
    root.after(0, main)

#makes a new window for a new task to be created 
def addTaskWindow():
    addTaskWindow = Toplevel()
    addTaskWindow.title("Add Task")
    
    entryExplination = Label(addTaskWindow, text = "Task:")
    entryExplination.grid(row = 0, column = 0)
    
    taskTextEntry = Entry(addTaskWindow)
    taskTextEntry.grid(row = 0, column = 1) 

    confirmButton = Button(addTaskWindow, text = "Add Task", command = lambda: makeNewTask(taskTextEntry.get(), addTaskWindow))
    confirmButton.grid(row = 1, column = 1)


def main():

    #Creates a button for adding a new task, a new window opens  where task details are added
    addTestButtom = Button(root, text = "Add New Task", command = addTaskWindow)
    addTestButtom.grid(row = 0, column = 0, ipadx = (minWindowX / 2), columnspan = 2)

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
            taskList[i].taskLabel.grid(row = i + 1, column = 0, padx = 0)
            taskList[i].taskButton.grid(row = i + 1, column = 1, padx = 0)        
    root.mainloop()


main()
