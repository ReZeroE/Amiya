import schedule
import time

class Scheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, time, function):
        """Adds a new task to the scheduler."""
        task = schedule.every().day.at(time).do(function)
        self.tasks[name] = task
        print(f"Task '{name}' added to run daily at {time}.")

    def remove_task(self, name):
        """Removes a scheduled task by name."""
        if name in self.tasks:
            task = self.tasks[name]
            schedule.cancel_job(task)
            del self.tasks[name]
            print(f"Task '{name}' removed.")
        else:
            print(f"Task '{name}' not found.")

    def list_tasks(self):
        """Lists all scheduled tasks."""
        if not self.tasks:
            print("No tasks scheduled.")
        for name in self.tasks:
            print(f"Scheduled task: {name}")

# Example usage
def my_task():
    print("Running my scheduled task!")

scheduler = Scheduler()

# Schedule a new task
scheduler.add_task("my_daily_task", "10:30", my_task)

# List scheduled tasks
scheduler.list_tasks()

# Main loop to run tasks
while True:
    schedule.run_pending()
    time.sleep(1)
