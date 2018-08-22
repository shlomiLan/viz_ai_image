import json
import os

import yaml
from invoke import task

BASEDIR = os.path.abspath(os.path.dirname(__file__))
active_venv = 'source {}/venv/bin/activate'.format(BASEDIR)
heroku_app_name = 'slots-tracker'


def run(c, command, with_venv=True):
    if with_venv:
        command = '{} && {}'.format(active_venv, command)

    print('Running: {}'.format(command))
    c.run(command)


@task()
def init_app(c, env=None):
    # Load the basic configs
    env_vars = load_yaml_from_file('{}/resources/config.yml'.format(BASEDIR))

    if env:
        env_vars.update(load_yaml_from_file('{}/resources/config_stage.yml'.format(BASEDIR)))

    for name, data in env_vars.items():
        set_env_var(c, name, data.get('value'), env, data.get('is_protected', False))


@task(init_app)
def run_app(c):
    run(c, 'flask run')


@task(init_app)
def test(c, cov=False, file=None):
    # cov - if to use coverage, file - if to run specific file
    set_env_var(c, 'APP_SETTINGS', 'config.TestingConfig', '')
    command = 'pytest -s'
    if cov:
        command = '{} --cov=slots_tracker_server --cov-report term-missing'.format(command)
    if file:
        command = '{} {}'.format(command, file)

    run(c, command)


# run scripts
@task(init_app)
def run_command(c, command):
    run(c, 'cd {} && flask {}'.format(BASEDIR, command))


# helper
def set_env_var(c, name, value, env, is_protected=True):
    # env codes: h - Heroku, t - Travis-CI
    if isinstance(value, dict):
        value = json.dumps(value)

    if env in ['h', 't']:
        command = ''
        if env == 'h':
            command = "heroku config:set {}='{}' -a {}".format(name, value, heroku_app_name)
        elif env == 't':
            command = "travis env set {} '{}'".format(name, value)
            if not is_protected:
                command = '{} --public'.format(command)

        if command:
            run(c, command, False)

    else:
        os.environ[name] = value


def load_yaml_from_file(file_path):
    with open(file_path, 'r') as stream:
        return yaml.safe_load(stream)


@task()
def build_venv(c):
    run(c, 'python3 -m venv venv', with_venv=False)
    install_requirements(c)


@task()
def install_requirements(c, dev=False):
    requirements_name = 'dev.txt' if dev else 'requirements.txt'
    requirements_path = '{}/{}'.format(BASEDIR, requirements_name)
    run(c, 'pip install --upgrade pip')
    run(c, 'pip install -r {}'.format(requirements_path))
