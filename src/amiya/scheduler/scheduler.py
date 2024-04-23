import schedule
import time
import threading

from amiya.scheduler.scheduler_config_handler import SchedulerConfigHandler
from amiya.apps_manager.apps_manager import AppsManager
from amiya.apps_manager.app import App
from amiya.utils.helper import *

class AmiyaScheduler:
    def __init__(self):
        self.apps_manager = AppsManager(verbose=False)
        self.config_handler = SchedulerConfigHandler()

        self.tasks = set()
        self.__load_saved_schedule()
        
        self.running = True

    def __load_saved_schedule(self):
        tasks = self.config_handler.load_tasks()
        for task in tasks:
            task_name = task["task_name"]
            app_tag = task["application_tag"]
            seq_name = task["sequence_name"]
            execution_time = task["execution_time"]
            self.add_task(task_name, execution_time, self.apps_manager.run_sequence_with_tag(app_tag, seq_name))


    def add_task(self, task_name, app_tag, seq_name, execution_time):
        # Schedule task
        task = schedule.every().day.at(execution_time).do(self.apps_manager.run_sequence_with_tag(app_tag, seq_name))
        
        # Save task to config
        self.config_handler.save_task(task_name, app_tag, seq_name, execution_time)
        
        # Cache task
        self.tasks[task_name] = task
        aprint(f"Task '{task_name}' scheduled to run daily at {execution_time}.")


    # def remove_task(self, task_name):
    #     if task_name in self.tasks:
    #         task = self.tasks[task_name]
    #         schedule.cancel_job(task)
    #         del self.tasks[task_name]
            
    #         print(f"Task '{task_name}' removed.")
    #     else:
    #         print(f"Task '{task_name}' not found.")


    # def list_tasks(self):
    #     if not self.tasks:
    #         print("No tasks scheduled.")
    #     for task_name in self.tasks:
    #         print(f"Scheduled task: {task_name}")


    def new_schedule(self, task_name=None, app_tag=None, seq_name=None, time=None):
        if not task_name:
            aprint("New schedule task name: ", end="")
            task_name = input().strip()
        
        app = None
        if not app_tag:
            self.apps_manager.print_apps()
            aprint("Which application would you like to schedule an automation of? ", end="")
            app_id = input().strip()
            app = self.apps_manager.get_app_with_id(app_id)
            app_tag = app.tags[0]
        else:
            app = self.apps_manager.get_app_by_tag(app_tag)
        
        if not seq_name:
            self.apps_manager.list_sequences_with_tag(app_tag)
            aprint("Which sequence would you like to schedule? (expecting sequence name) ", end="")
            sequence_name = input().strip()
            self.apps_manager.sequence_exists(app, sequence_name)

        if not time:
            aprint("What time of the day would you like to run this automation sequence (i.e. 10:30 or 16:20)? ")
            time = input().strip()

        self.add_task(task_name, time, self.apps_manager.run_sequence_with_tag(app_tag, seq_name))
    

    def start_scheduler(self, time_started):
        aprint(f"Scheduler started, {len(self.tasks)} tasks are currently scheduled...")
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            aprint("Scheduler stopped by keyboard interrupt.")


    def stop_scheduler(self):
        self.running = False
        aprint("Stopping scheduler...")

    def run_scheduler(self):
        scheduler_thread = threading.Thread(target=self.start_scheduler, args=(time.time(),))
        scheduler_thread.start()
        
        try:
            while True:
                schedule.run_pending()
                aprint("To add a new task, enter 'add'. To exit, enter 'exit'.")
                command = input().strip().lower()
                if command == 'add':
                    # Implement a more interactive approach or directly call new_schedule
                    self.new_schedule()
                elif command == 'exit':
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            self.stop_scheduler()
            scheduler_thread.join() 
            aprint("Main program exited.")