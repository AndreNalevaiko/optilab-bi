from fabric.api import task, run, local

VERSION = '1.0.0'
CONTAINER_NAME = 'optilab-bi-api'
IMAGE_NAME = 'optilab-bi-api/%s' % CONTAINER_NAME

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

@task
def iterative_test():
    local('export $(cat env_file | xargs) && ipython')

@task
def build():

        local('docker build -t %s:%s --rm .' % (IMAGE_NAME, VERSION))

        local('docker tag %s:%s %s:latest' % (IMAGE_NAME, VERSION, IMAGE_NAME))
@task
def push():

    int_VERSION = int(VERSION.replace('.', ''))

    # if int_VERSION != 100 and int_VERSION > 1:
    #     local('docker pull andrenalevaiko/%s:latest' % CONTAINER_NAME)
    #     local('docker tag andrenalevaiko/%s:latest andrenalevaiko/%s:backup' % (CONTAINER_NAME, CONTAINER_NAME))
    #     local('docker push andrenalevaiko/%s:backup' % CONTAINER_NAME)

    local('docker tag %s:%s andrenalevaiko/%s:%s' % (IMAGE_NAME, VERSION, IMAGE_NAME, VERSION))
    local('docker tag %s:%s andrenalevaiko/%s:latest' % (IMAGE_NAME,VERSION, IMAGE_NAME))
    local('docker push andrenalevaiko/%s:%s' % (IMAGE_NAME, VERSION))
    local('docker push andrenalevaiko/%s:latest' % IMAGE_NAME)
