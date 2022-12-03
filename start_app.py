#!venv/bin/python
import os
import sys

from src.settings import DOCKER_REDIS_NAME

redis_stop = 'sudo docker stop %s' % DOCKER_REDIS_NAME
redis_rm = 'sudo docker rm %s' % DOCKER_REDIS_NAME
redis_run = 'sudo docker run --name %s -d -p 6379:6379 redis' % DOCKER_REDIS_NAME
app_run = 'celery worker -A src.celery_tasks.tasks -B -l info --purge & python flask_run.py'


if __name__ == '__main__':
    try:
        assert sys.version_info >= (2, 7)
        try:
            os.system(redis_stop)
            os.system(redis_rm)
        except Exception:
            pass
        os.system(redis_run)
        os.system(app_run)
    
    except KeyboardInterrupt:
        raise KeyboardInterrupt
