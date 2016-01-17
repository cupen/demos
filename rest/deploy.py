# coding:utf-8
from fabric.api import task, run, local, sudo, put
from fabric.colors import red, green
from fabric.context_managers import cd, settings, hide
import os

from fabric.tasks import execute

ROOT_DIR = os.path.dirname(__file__)
ROOT_DIR_REMOTE = '/home/cupen/rest'
path2unix = lambda *path: os.path.join(*path).replace('\\', '/')

def ok(msg):
    print(green(msg))

def error(msg):
    print(red(msg))

def upload_project(local_dir=None, remote_dir="", use_sudo=False,\
                   user="root:root", mode=620,\
                   exclude=(".[a-zA-Z0-9]*",), verbose=False,\
                   extra_exclude=(".[a-zA-Z0-9]*", "__pycache__/", "*.py[cd]",), ):

    path2unix = lambda *path: os.path.join(*path).replace('\\', '/')
    local_dir = local_dir or os.getcwd()
    exclude = " ".join(map(lambda x:"--exclude=%s"%x, exclude + extra_exclude))
    runner = use_sudo and sudo or run

    local_name = os.path.basename(os.path.realpath(local_dir))
    # tmp_folder = path2unix(mkdtemp())

    tmp_folder = path2unix(os.path.join(local_dir, '.temp'))
    # tmp_folder = local_dir
    if not os.path.isdir(tmp_folder):
        os.mkdir(tmp_folder)

    tar_file   = path2unix("%s.tar.gz" % local_name)
    local_tar  = path2unix(os.path.join(tmp_folder, tar_file))
    remote_tar = path2unix(os.path.join(remote_dir, tar_file))
    try:
        local("tar -czf %(local_tar)s %(local_dir)s -C %(local_dir)s %(exclude)s" % locals())
        runner('mkdir -p %(remote_dir)s'%locals())
        put(local_tar, remote_tar, use_sudo=use_sudo)
        with cd(remote_dir):
            try:
                cmd = "tar -xzf %(tar_file)s"
                if verbose: cmd = "tar -xvzf %(tar_file)s"
                runner(cmd %locals())
                runner("chown %(user)s -R %(remote_dir)s"%locals())
                runner("chmod 700 -R %(remote_dir)s"%locals())
            finally:
                runner("rm -f %(tar_file)s" %locals())
    finally:
        local("rm %(local_tar)s" %locals())
        pass
    pass


@task
def deploy():
    upload_project(
        use_sudo=True,
        local_dir='.',
        remote_dir=ROOT_DIR_REMOTE,
        user='cupen:cupen',
        exclude=('*.db',)
    )
    execute(restart)
    pass

@task
def restart():
    with cd(ROOT_DIR_REMOTE):
        sudo('pip3 install -r requrements.txt')
        put('supervisor.conf', '/etc/supervisor/conf.d/restdemo.conf', use_sudo=True)
        sudo('supervisorctl restart restdemo')
    pass