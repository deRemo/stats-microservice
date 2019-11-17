# -*- coding: utf-8 -*-
from service import create_app, create_celery


app = create_app(config='./service/config.py')
celery = create_celery(app)

#starts period stat gathering's task
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 2 seconds.
    sender.add_periodic_task(2.0, test.s("ciao"), name='add every 2')

@celery.task
def test(arg):
    print(arg)


celery.start()