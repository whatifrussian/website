# -*- coding: utf-8 -*-

from fabric.api import *
import fabric.contrib.project as project
import os

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'
DEPLOY_PATH = env.deploy_path

# Remote server configuration

env.user="www-data"
env.hosts = ["chtoes.li"]
path = {
        "dev": '/var/www/dev.chtoes.li/public/',
        "prod": '/var/www/chtoes.li/public/',
        "ci": '/var/www/ci.chtoes.li/public/'
        }

TEMPLATE = "Title:\n\
Date: {{date}}\n\
Slug: {{slug}}\n\
Category: {{ category }}\n\
Source: http://what-if.xkcd.com/{{num}}/\n\
SourceNum: {{num}}\n\
SourceTitle: {{title}}\n\
Formulas: False\n\
Description: \n\
Image: https://chtoes.li/uploads/{{num}}-{{slug}}/front.png\n\
\n\
\n"

def new(num, title=None, category="What If?", overwrite="no"):
    import datetime

    if title is None:
        import urllib2
        from bs4 import BeautifulSoup
        html = urllib2.urlopen("http://what-if.xkcd.com/{}/".format(num))
        title = BeautifulSoup(html, "lxml").title.string

    slug = slugify(title)

    CATEGORIES = {
        "What If?": "what-if",
        "Новости проекта": "news",
        "Прочее": "other",
    }
    
    category_slug = CATEGORIES[category] 
    now = datetime.datetime.now()
    post_date = now.strftime("%Y-%m-%d")

    params = dict(
        date     = post_date,
        title    = title,
        slug     = slug,
        num      = num,
        category = category
    )

    out_file = "content/{}/{:03d}-{}.md".format(category_slug, int(num), slug)
    local("mkdir -p '{}' || true".format(os.path.dirname(out_file)))
    if not os.path.exists(out_file) or overwrite.lower() == "yes":
        render(TEMPLATE, out_file, **params)
    else:
        print("{} already exists. Pass 'overwrite=yes' to destroy it.".
            format(out_file))

def slugify(text):
    import re
    normalized = "".join([c.lower() if c.isalnum() else "-"
                    for c in text])
    no_repetitions = re.sub(r"--+", "-", normalized)
    clean_start = re.sub(r"^-+", "", no_repetitions)
    clean_end = re.sub(r"-+$", "", clean_start)
    return clean_end

def render(template, destination, **kwargs):
    from jinja2 import Template
    template = Template(TEMPLATE)
    text = template.render(**kwargs)
    with open(destination, "w") as output:
        puts("Rendering to {}".format(destination))
        output.write(text.encode("utf-8"))


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
    import sys
    PY3 = sys.version_info > (3,)
    # Determine major version of python as the one executes this script now.
    if PY3:
        local('cd {deploy_path} && python3 -m http.server'.format(**env))
    else:
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
