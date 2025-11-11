from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS

# --- Class Logic ---

class Task:
    """Represents a single To-Do task."""
    def __init__(self, task_id, content):
        self.id = task_id
        self.content = content
        self.completed = False

    def to_dict(self):
        """Returns a dictionary representation of the task."""
        return {
            "id": self.id,
            "content": self.content,
            "completed": self.completed
        }

class TaskManager:
    """Manages a collection of tasks."""
    def __init__(self):
        self._tasks = {} 
        self._next_id = 1
        # Pre-populate with a few tasks to show it's working
        self.add_task("Run the Python backend")
        self.add_task("Open the HTML file")
        self.add_task("Add a new task!")

    def add_task(self, content):
        """Creates a new task and adds it to the manager."""
        task_id = self._next_id
        new_task = Task(task_id, content)
        self._tasks[task_id] = new_task
        self._next_id += 1
        return new_task

    def get_all_tasks(self):
        """Returns a list of all task dictionaries."""
        return [task.to_dict() for task in self._tasks.values()]

    def get_task(self, task_id):
        """Returns a single task object by its ID."""
        return self._tasks.get(task_id)

    def toggle_task_status(self, task_id):
        """Toggles the completion status of a task."""
        task = self.get_task(task_id)
        if task:
            task.completed = not task.completed
            return task
        return None

    def delete_task(self, task_id):
        """Deletes a task by its ID."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

# --- Flask App & API Routes ---

app = Flask(__name__)
# Enable CORS for all routes, allowing our index.html to talk to this server
CORS(app) 

# Instantiate our manager. This will keep the tasks in memory.
task_manager = TaskManager()

@app.route('/')
def home():
    return "Pomo-Do Backend is running."

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Endpoint to get all tasks."""
    all_tasks = task_manager.get_all_tasks()
    return jsonify(all_tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Endpoint to create a new task."""
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request body"}), 400
    
    content = data['content']
    new_task = task_manager.add_task(content)
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    """Endpoint to toggle a task's completion status."""
    task = task_manager.toggle_task_status(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Endpoint to delete a task."""
    if task_manager.delete_task(task_id):
        return jsonify({"message": "Task deleted successfully"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404


if __name__ == '__main__':
    # Starts the Flask web server
    app.run(debug=True, port=5000)
