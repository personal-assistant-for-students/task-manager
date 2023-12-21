from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, request

from flask_cors import CORS

from task_repository import TaskRepository
from task_service import TaskService

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['WTF_CSRF_ENABLED'] = False

db_path = "../data/mvp_db.csv"
repository = TaskRepository(db_path)
task_service = TaskService(repository)

scheduler = BackgroundScheduler()
scheduler.start()


def update_additional_status():
    task_service.get_all_tasks()
    pass

# schedule for update additional status (every day at в 00:00)
trigger = CronTrigger(hour=0, minute=0)
scheduler.add_job(update_additional_status, trigger=trigger)

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = task_service.create_task(data['title'], data['content'], data['deadline'])
    return jsonify(task.to_dict()), 201


@app.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    updated_task = task_service.update_task(task_id, **data)
    if updated_task:
        return jsonify(updated_task.to_dict()), 200
    else:
        return jsonify({"message": "Task not found"}), 404


@app.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        response = task_service.delete_task(task_id)
        if "not found" in response["message"]:
            return jsonify(response), 404
        return jsonify(response), 200
    except Exception as e:
        # В случае возникновения ошибки
        return jsonify({"error": str(e)}), 500


@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = task_service.get_all_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200


if __name__ == '__main__':
    app.run(debug=True)
