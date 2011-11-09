import os
import fabric
from fabric.api import env, local, sudo, cd, prefix

env.hosts = ['praveen@173.255.241.59']
env.master_repo = 'ssh://hg@bitbucket.org/pgollakota/django-chartit'
env.sec_repo = 'git+ssh://git@github.com/pgollakota/django-chartit.git'
env.activate = 'source /work/virtualenvs/chartit/bin/activate'
env.project_root = '/home/praveen/cows/django-chartit'


def run(cmd):
    with cd(env.project_root):
        with prefix(env.activate):
            fabric.api.run(cmd)


def push():
    local('hg push %(master_repo)s' % env)
    local('hg push %(sec_repo)s' % env)
    run('hg pull -u %(master_repo)s' % env)


def upload_to_pypi():
    local('python setup.py sdist upload')


def build_docs():
    with prefix('export DJANGO_SETTINGS_MODULE=demoproject.settings'):
        run('cd docs && make html')


def install_requirements():
    run('pip install -r requirements.txt -q')


def upgrade_db():
    run('cd demoproject && python manage.py syncdb')


def deploy_static():
    run('cd demoproject && python manage.py collectstatic -v0 --noinput')


def restart_webserver():
    sudo('supervisorctl restart nginx')
    sudo('supervisorctl restart chartit')


def deploy():
    push()
    build_docs()
    install_requirements()
    upgrade_db()
    deploy_static()
    restart_webserver()
