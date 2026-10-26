import argparse, json, os, shutil, time, zipfile
from datetime import datetime

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


class Task:
    def __init__(self, task_id, operation, source, destination, schedule, last_run=""):
        self.task_id = task_id
        self.operation = operation      # copy, move, delete, archive
        self.source = source
        self.destination = destination
        self.schedule = schedule        # daily:10:00 или weekly:mon:10:00
        self.last_run = last_run

    def __repr__(self):
        return f"[{self.task_id}] {self.operation} {self.source} -> {self.destination} | {self.schedule}"


class FileOperations:
    @staticmethod
    def run(operation, source, destination):
        if operation == "copy":
            shutil.copy2(source, destination)
        elif operation == "move":
            shutil.move(source, destination)
        elif operation == "delete":
            os.remove(source)
        elif operation == "archive":
            with zipfile.ZipFile(destination, "w") as z:
                z.write(source)


class Logger:
    def log(self, task, status):
        line = f"{datetime.now():%Y-%m-%d %H:%M:%S} | задача {task.task_id} | {task.operation} {task.source} | {status}"
        with open("scheduler.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line)


class Scheduler:
    def __init__(self):
        self.logger = Logger()
        self.tasks = []
        if os.path.exists("tasks.json"):
            with open("tasks.json", encoding="utf-8") as f:
                self.tasks = [Task(**t) for t in json.load(f)]

    def save(self):
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump([t.__dict__ for t in self.tasks], f, ensure_ascii=False, indent=4)

    def add_task(self, operation, source, destination, schedule):
        new_id = self.tasks[-1].task_id + 1 if self.tasks else 1
        self.tasks.append(Task(new_id, operation, source, destination, schedule))
        self.save()
        print("Добавлена задача:", self.tasks[-1])

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.task_id != task_id]
        self.save()
        print("Задача удалена:", task_id)

    def run_task(self, task):
        try:
            FileOperations.run(task.operation, task.source, task.destination)
            self.logger.log(task, "Успешно")
        except Exception as e:
            self.logger.log(task, f"Ошибка: {e}")

    def is_time(self, task, now):
        parts = task.schedule.split(":", 1)         # ['daily', '10:00'] или ['weekly', 'mon:10:00']
        if parts[0] == "weekly":
            day, parts[1] = parts[1].split(":", 1)
            if DAYS[now.weekday()] != day:
                return False
        minute = now.strftime("%Y-%m-%d %H:%M")
        return now.strftime("%H:%M") == parts[1] and task.last_run != minute

    def start(self):
        print("Шедулер запущен. Остановка: Ctrl+C")
        try:
            while True:
                now = datetime.now()
                for task in self.tasks:
                    if self.is_time(task, now):
                        self.run_task(task)
                        task.last_run = now.strftime("%Y-%m-%d %H:%M")
                        self.save()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Шедулер остановлен")


parser = argparse.ArgumentParser(description="Файловый шедулер")
parser.add_argument("command", choices=["add", "view", "delete", "run", "start"])
parser.add_argument("--operation", choices=["copy", "move", "delete", "archive"])
parser.add_argument("--source")
parser.add_argument("--destination")
parser.add_argument("--schedule", help="daily:10:00 или weekly:mon:10:00")
parser.add_argument("--id", type=int, help="номер задачи (для delete и run)")
args = parser.parse_args()

scheduler = Scheduler()
if args.command == "add":
    scheduler.add_task(args.operation, args.source, args.destination, args.schedule)
elif args.command == "view":
    print("\n".join(map(str, scheduler.tasks)) or "Задач нет")
elif args.command == "delete":
    scheduler.delete_task(args.id)
elif args.command == "run":
    for t in scheduler.tasks:
        if t.task_id == args.id:
            scheduler.run_task(t)
else:
    scheduler.start()
