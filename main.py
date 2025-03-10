# pip install python-fasthtml

from fasthtml.common import *

def render(tasks):
    return Li(f"{tasks.task}",
           A("Complete", hx_delete=f"/{tasks.id}", hx_swap="outerHTML", target_id=f'tasks-{tasks.id}'),
           id=f'tasks-{tasks.id}'
        ) 

# Initialize FastHTML app with SQLite
app,rt,tasks,Task = fast_app(
    'tasks.db',
    live=True, 
    render=render,
    id=int, 
    task=str, 
    pk="id"
)

def reset_task_input():
    return Input(name="task", id="task", placeholder="Task Name", hx_swap_oob="true", required=True)

# Route to display the to-do list
@rt('/')
def get():
    return Titled("Vienna's To-Do List", Div(
        Ul(*tasks(), id="task_list"), 
        H2("Add a new task:"),
        Form(
            reset_task_input(),
            Button("Add Task", hx_post="/", target_id="task_list", hx_swap="beforeend", styLe="background-color: pink; color: white; border-color: pink; box-shadow: none;")
        ),
        Div(
            H4(" "),
            P(id="alert")),
        ))

# Route to add a new task
@rt('/')
def post(task: str):
    task = task.strip()
    if not task:
        return P("Task cannot be empty!", id="alert", style="color: red;", hx_swap_oob="true")
    
    task = task + " "
    new_task = tasks.insert(task=task)
    
    return new_task, reset_task_input(), P("", id="alert", hx_swap_oob="true")

@rt('/{id}')
def delete(id: int):
    tasks.delete(id)

# Start the server
serve()

# cd Documents (or wherever the python thing is installed)
# python file must be named main.py
#  python -m uvicorn main:app --reload
