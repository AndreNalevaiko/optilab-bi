from fabric.api import task, run, local

VERSION = '1.0.0'
CONTAINER_NAME = 'optilab-bi'
IMAGE_NAME = 'optilab-bi/%s' % CONTAINER_NAME

@task
def build():
    local('docker build -t %s:%s --rm .' % (IMAGE_NAME, VERSION))
    local('docker tag %s:%s %s:latest' % (IMAGE_NAME, VERSION, IMAGE_NAME))

@task
def run():
    local('export $(cat env_file | xargs) && .venv/bin/python3 run.py')

@task
def run_like_prod():
    local('export $(cat env_file | xargs) && .venv/bin/gunicorn --config=gunicorn.py run:app')
