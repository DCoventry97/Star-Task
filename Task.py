class Task:
    def __init__(self, taskText, taskLabel, taskButton, db, root):
        self.taskText = taskText
        self.taskLabel = taskLabel
        self.taskButton = taskButton
        if db.taskExists(taskText):
             self.taskId = db.getTaskId(taskText)
        else:
            self.taskId = db.addTask(taskText)
        self.category = db.getTaskCat(self.taskId)


    #removes the task object when called
    def deleteTask(self, db):
        self.taskLabel.grid_forget()
        self.taskButton.grid_forget()
        db.removeTask(self.taskId)
