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
def makeNewTask(text, category, windowObject):
    db.addTask(text, category[2:-3])
    windowObject.destroy()
    root.after(0, main)

#removes the task from the GUI and calls main again
def destroyTask(taskObject):
    taskObject.deleteTask(db)
    for child in root.winfo_children():
        child.destroy()
    
    root.after(0, main)

#adds category text to db and closes window
def addCategory(text, WindowObject):
    db.addCategory(text)
    WindowObject.destroy()
    root.after(0, main)

#removes selected category from window and closes remove category window
def destroyCategory(text, windowObject):
    db.removeCategory(text)
    windowObject.destroy()


#makes a new window for a new task to be created 
def addTaskWindow():
    addTaskWindow = Toplevel()
    addTaskWindow.title("Add Task")
    
    entryExplination = Label(addTaskWindow, text = "Task:")
    entryExplination.grid(row = 0, column = 0)
    
    taskTextEntry = Entry(addTaskWindow)
    taskTextEntry.grid(row = 0, column = 1) 

    categoryList = db.getAllCategories()
    selectedCat = StringVar()
    selectedCat.set(categoryList[0])


    categoryOption = OptionMenu(addTaskWindow, selectedCat, *categoryList)
    categoryOption.grid(row = 1, column = 0)

    confirmButton = Button(addTaskWindow, text = "Add Task", command = lambda: makeNewTask(taskTextEntry.get(), selectedCat.get(), addTaskWindow))
    confirmButton.grid(row = 1, column = 1)

#makes a new window to select a category to be removed from db
def removeCategoryWindow():
    removeCatWindow = Toplevel()
    removeCatWindow.title("Remove Category")
    explinationLabel = Label(removeCatWindow, text = "Select the category to be removed")
    explinationLabel.grid(row = 0, column = 0)
    categories = db.getAllCategories()
    
    for i in range (1, len(categories)):
        catLable = Label(removeCatWindow, text = categories[i][0])
        catLable.grid(row = i, column = 0)
        catButton = Button(removeCatWindow, text = "Delete", command = lambda position = i: destroyCategory(categories[position], removeCatWindow))
        catButton.grid(row = i, column = 1)




# makes a new window for a category to be added 
def addCategoryWindow():
    addCatWindow = Toplevel()
    addCatWindow.title("Add Category")

    entryExplination = Label(addCatWindow, text = "Category Name:")
    entryExplination.grid(row = 0, column = 0)

    categoryTextEntry = Entry(addCatWindow)
    categoryTextEntry.grid(row = 0, column = 1) 

    confirmButton = Button(addCatWindow, text = "Add Category", command = lambda: addCategory(categoryTextEntry.get(), addCatWindow) )
    confirmButton.grid(row = 1, column = 1)


def main():
    #makes root menu object
    menubar = Menu(root)
    
    ##makes menu object for file buton, has buttons for adding new task, add new category, view categories, empty db and quit program
    fileMenu = Menu(menubar, tearoff = False)
    fileMenu.add_command(label = "Add Task", command = addTaskWindow)
    fileMenu.add_command(label = "Add Category", command = addCategoryWindow)
    fileMenu.add_command(label = "Remove Categories", command = removeCategoryWindow)
    fileMenu.add_command(label = "Quit", command = root.quit)
    menubar.add_cascade(label = "File", menu = fileMenu)
    
    #displays root menubar object
    root.config(menu = menubar)

    #Creates a button for adding a new task, a new window opens  where task details are added
    addTestButtom = Button(root, text = "Add New Task", command = addTaskWindow)
    addTestButtom.grid(row = 0, column = 0, ipadx = (minWindowX / 2), columnspan = 3)

    #checks if the database is not empty
    if not db.checkIfEmpty():
        #gets all the tasks in the database, makes a task object with them and then adds them to an array
        taskTextList = db.getAllTasks()
        listCounter = 0
        taskList = []
        for taskText in taskTextList:
            task = Task(taskText, Label(root, text = taskText), Button(root, text = "Task Complete", command =lambda position = listCounter: destroyTask(taskList[position]) ),db, root) 
            taskList.append(task)
            listCounter += 1
        #task array is used to draw the task label and button to remove task from the program
        for i in range(0,db.rowCount()):
            label = Label(root, text = taskList[i].category)
            taskList[i].taskLabel.grid(row = i + 1, column = 0, padx = 0)
            if (taskList[i].category != "None"):
                label.grid(row = i + 1, column = 1)
            taskList[i].taskButton.grid(row = i + 1, column = 2, padx = 0)   
            
            
    
    root.mainloop()


if __name__ == "__main__":
    main()
