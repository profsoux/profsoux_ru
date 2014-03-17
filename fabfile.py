# encoding=utf-8

from fabric.api import *

env.hosts = ["profsoux.ru",]


def deploy(branch="test"):
    services = {
        "test": "profsoux-test",
        "www": "profsoux-ru",
    }
    code_dir = "/home/h4/sites/profsoux.ru/{}/htdocs".format(branch)
    with cd(code_dir):
        run("git pull")
        run("/home/h4/envs/profsoux/bin/python manage.py collectstatic --noinput")
        sudo("service {} restart".format(services[branch]))
