#!/usr/bin/env python3


import sys
import json
from datetime import datetime

TASKS_FILE = 'tasks.json'



def load_tasks():
    try:
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    # 异常处理，只读现有任务
    
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)
    #保存任务，变为格式化的json文件

if __name__ == "__main__":
    if len(sys.argv) < 2:
        #如果没有提供命令行参数，打印用法信息
        print("Usage: python task-cli.py [add|list|complete] [task_description|task_id]")
        sys.exit(1)
        #退出程序，状态码1表示错误

    command = sys.argv[1] #获取命令行参数中的命令,赋值给command
    if command == 'add':#添加任务
        if len(sys.argv) < 3:
            #add后面没写
            print("Please provide a task description.")
            sys.exit(1)
        description = ' '.join(sys.argv[2:])#将描述拼到command后面
        tasks = load_tasks()
        new_id = max([task['id'] for task in tasks], default=0) + 1
        #取id的最大值，新的id为最大值加1，默认id为0，按顺序+1
        new_task = {
            'id': new_id,
            'description': description,
            'status': 'todo',
            'createdAt': datetime.now().isoformat(timespec='seconds'),
            'updatedAt': datetime.now().isoformat(timespec='seconds')
        }#创建新任务的字典
        tasks.append(new_task)#tasks的变量类型是list，在list中添加新任务
        save_tasks(tasks)
        print(f"Task added successfully (ID: {new_id}).")

    elif command == 'list':  #列出任务
        tasks = load_tasks()
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        #如果有提供list后面的命令，就赋值给status_filter，如果list后面没有命令，就赋值为None，输出所有任务
        if status_filter and status_filter not in ['todo', 'done', 'in-progress']: #如果list后面的命令写错了
            print("Invalid status filter. Use 'todo', 'done', or 'in-progress'.")
            sys.exit(1)
        found = False #标记是否找到任务
        if status_filter == None:
            for task in tasks:             
                print(f"{task['id']},{task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
                found = True
        else:
            for task in tasks:
                if task['status'] == status_filter:
                    print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
                    found = True
        '''
        for task in tasks:
            if status_filter is None or task['status'] == status_filter:
            两个条件本来就是互斥的,所以可以用or连接,不需要if-else
                print(f"{task['id']},{task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")
                found = True
        '''
        if not found:
            if status_filter:#则判断是没有任务还是过滤器没匹配上
                print(f"No tasks found with status '{status_filter}'.")
            else:
                print("No tasks found.")

    elif command == 'update':   #更新任务描述
        if len(sys.argv) < 3:
            print("Please provide a task ID to update.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        if len(sys.argv) < 4:
            print("Please provide a new task description.")
            sys.exit(1)
        tasks = load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['description'] = ' '.join(sys.argv[3:])
                task['updatedAt'] = datetime.now().isoformat(timespec='seconds')
                save_tasks(tasks)
                print(f"Task {task_id} updated.")
                break
        else:
            print(f"No task found with ID {task_id}.")

    elif command == 'delete':   #删除任务
        if len(sys.argv) < 3:
            print("Please provide a task ID to delete.")
            sys.exit(1)
        if sys.argv[2] == 'all':
            save_tasks([])
            print("All tasks deleted.")
            sys.exit(0)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)
        tasks = load_tasks()
        for i, task in enumerate(tasks):
            if task['id'] == task_id:
                del tasks[i]
                save_tasks(tasks)
                print(f"Task {task_id} deleted.")
                break
        else:
            print(f"No task found with ID {task_id}.")
    
    elif command in ['mark-todo', 'mark-done', 'mark-in-progress']:  #标记任务状态
        if len(sys.argv) < 3:
            print("Please provide a task ID to update status.")
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Task ID must be an integer.")
            sys.exit(1)

        status_map = {
            'mark-todo': 'todo',
            'mark-done': 'done',
            'mark-in-progress': 'in-progress'
        }
        new_status = status_map[command]
        if not new_status:
            print("Invalid status command.")
            sys.exit(1)
        
        tasks = load_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['status'] = new_status
                task['updatedAt'] = datetime.now().isoformat(timespec='seconds')
                save_tasks(tasks)
                print(f"Task {task_id} marked as {new_status}.")
                break
        else:
            print(f"No task found with ID {task_id}.")

    elif command == 'help':
        print("Usage: python task-cli.py [add|list|update|delete|mark-todo|mark-done|mark-in-progress] [task_description|task_id]")
        print("Commands:")
        print("  add [task_description]       - Add a new task")
        print("  list                         - List all tasks")
        print("  update [task_id] [new_description] - Update task description")
        print("  delete [task_id|all]        - Delete a task by ID or all tasks")
        print("  mark-todo [task_id]         - Mark task as todo")
        print("  mark-done [task_id]         - Mark task as done")
        print("  mark-in-progress [task_id]  - Mark task as in-progress")

