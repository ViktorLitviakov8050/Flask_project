from rq import get_current_job
from app import db
from app.models import Task, Post, User
import time
from app import create_app
import json
import sys
import app.admin as admin
import json

app = create_app()
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notification('task_progress', {'task_id': job.get_id(),
                                                     'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        i = 0
        total_posts = user.posts.count()
        for post in user.posts.order_by(Post.timestamp.asc()):
            data.append({'body': post.body,
                         'timestamp': post.timestamp.isoformat() + 'Z'})
            time.sleep(0.1)
            i += 1
            _set_task_progress(100 * i // total_posts)
        filename = user.get_posts_filename()
        with open(filename, 'w') as fp:
            json.dump({'posts': data}, fp, indent=4)

        admin.send_message(user.username)
    except:
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())
    finally:
        _set_task_progress(100)
