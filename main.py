# pip install python-fasthtml

from fasthtml.common import *

def render(tasks):
    return Li(f"{tasks.task}",
           A("Delete", hx_delete=f"/{tasks.id}", hx_swap="outerHTML", target_id=f'tasks-{tasks.id}'),
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
    return Input(name="task", id="task", placeholder="Task", hx_swap_oob="true", required=True)

def empty_alert(text):
    return Div(
        alert(text)
        P(text),
        Button("OK", hx_get="/close_alert", hx_swap_oob="true"),
        id="alert",
        open=True
    ),
    )

# Route to display the contact list
@rt('/')
def get():
    # create_contacts()
    # items = [Li(o) for o in contacts()]
    return Titled("Vienna's To-Do List", Div(
        Div(id="alert"),
        Ul(*tasks(), id="task_list"),
        H2("Add a new task:"),
        Form(
            reset_task_input(),
            Button("Add Task", hx_post="/", target_id="task_list", hx_swap="beforeend")
        )
    )
    )

# Route to add a new contact
@rt('/')
def post(task: str):
    task = task.strip()
    if not task:
        alert("Message cannot be empty!")
    
    new_task = tasks.insert(task=task) 
    return new_task, reset_task_input()

@rt('/{id}')
def delete(id: int):
    tasks.delete(id)

@rt('/close_alert')
def close_alert():
    return Dialog(id="alert", open=False, hx_swap_oob="true")

# Start the server
serve()

# cd Documents (or wherever the python thing is installed)
# python file must be named main.py
#  python -m uvicorn main:app --reload