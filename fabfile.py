from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration

env.user="chtoes_li"
env.hosts = ["shared.libc6.org"]
path = {
        "dev": '/var/www/chtoes_li/data/www/dev.chtoes.li/',
        "prod": '/var/www/chtoes_li/data/www/chtoes.li/'
        }

def clean():
    if os.path.isdir(DEPLOY_PATH):
        local('rm -rf {deploy_path}'.format(**env))
        local('mkdir {deploy_path}'.format(**env))

def build(environment):
    local('pelican -q -s pelicanconf-{}.py'.format(environment))

def rebuild(environment):
    clean()
    build(environment)

def regenerate(environment):
    local('pelican -q -r -s pelicanconf-{}.py'.format(environment))

def serve():
    local('cd {deploy_path} && python2 -m SimpleHTTPServer'.format(**env))

def reserve(environment):
    build(environment)
    serve()

def preview(environment):
    local('pelican -s pelicanconf-{}.py'.format(environment))

def publish(environment):
    local('pelican -q -s pelicanconf-{}.py'.format(environment))
    project.rsync_project(
        remote_dir=path[environment],
        exclude=".DS_Store",
        local_dir=DEPLOY_PATH.rstrip('/') + '/',
        delete=True
    )
