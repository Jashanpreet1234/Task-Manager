class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.current_id = 1

    def add_task(self, title, priority):
        task_id = self.current_id
        self.tasks[task_id] = {"title": title, "priority": priority.capitalize(), "completed": False}
        self.current_id += 1

    def get_tasks(self):
        return self.tasks

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]

    def complete_task(self, task_id):
        if task_id in self.tasks:
            self.tasks[task_id]["completed"] = True
