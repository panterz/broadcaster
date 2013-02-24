from fabric.api import env, put, run, task, local, prompt, sudo
import os

@task
def deploy_local():
    env.user = "panterz"
    env.hosts = ['',]
    home = os.environ['HOME']
    #create local if not exists
    if not os.path.exists(os.path.join(home, 'local')):
        local('mkdir %s' % os.path.join(home, 'local'))
    current_path = os.path.abspath(os.path.dirname(__file__))
    proj_path = os.path.join(home, 'local', 'polls')
    run("cd %(current_release)s; virtualenv --no-site-packages ." % { 'current_release':proj_path })
    run("cd %(current_release)s; ./bin/pip -q install -E %(current_release)s -r %(domain_path)s/etc/requirements.txt" % { 'current_release':proj_path, 'domain_path':current_path })
    local('ln s %s %s' %(os.path.join(current_path, 'broadcaster'), os.path.join(proj_path, 'broadcaster')))

@task
def devel():
    """Defines devel environment"""
    env.user = prompt('Type the name of the user ')
    env.hosts = prompt('Type the name of the host')
    env.base_dir = "/home/%s/dist" %(env.user)
    env.app_name = "broadcaster"
    env.domain_path = "%(base_dir)s/%(app_name)s" % { 'base_dir':env.base_dir, 'app_name':env.app_name }
    env.current_path = "%(domain_path)s/current" % { 'domain_path':env.domain_path }
    env.releases_path = "%(domain_path)s/releases" % { 'domain_path':env.domain_path }
    # env.shared_path = "%(domain_path)s/shared" % { 'domain_path':env.domain_path }
    # env.git_clone = "geodev@devel.edina.ac.uk:cartogram/cartogrammer.git"
    env.env_file = "etc/requirements.txt"
    env.app_local = "./%(app_name)s" % { 'app_name':env.app_name }

@task
def setup():
    """Prepares one or more servers for deployment"""
    run("mkdir -p %(domain_path)s" % { 'domain_path':env.domain_path })
    run("mkdir -p %(domain_path)s/etc" % { 'domain_path':env.domain_path })
    put("%(env_file)s" % { 'env_file':env.env_file }, "%(domain_path)s/etc" % { 'domain_path':env.domain_path })
    run("mkdir -p %(releases_path)s" % { 'releases_path':env.releases_path })

@task
def deploy():
    """Deploys your project, updates the virtual env then restarts"""
    _update()
    restart()


def _update():
    """Copies your project and updates environment and symlink"""
    _checkout()
    _update_env()
    _symlink()

def _checkout():
    """Checkout code to the remote servers"""
    from time import time
    env.current_release = "%(releases_path)s/%(time).0f" % { 'releases_path':env.releases_path, 'time':time() }
    run("mkdir -p %(current_release)s" % { 'current_release':env.current_release })
    put("%(app_local)s" % { 'app_local':env.app_local }, "%(current_release)s" % { 'current_release':env.current_release })

def _update_env():
    """Update servers environment on the remote servers"""
    if not env.has_key('current_release'):
        _releases()
    run("cd %(current_release)s; virtualenv --no-site-packages ." % { 'current_release':env.current_release })
    run("cd %(current_release)s; ./bin/pip -q install -E %(current_release)s -r %(domain_path)s/%(env_file)s" % { 'current_release':env.current_release, 'domain_path':env.domain_path, 'env_file':env.env_file })

def _symlink():
    """Updates the symlink to the most recently deployed version"""
    if not env.has_key('current_release'):
        _releases()
    run("rm %(current_path)s" % { 'current_path':env.current_path })
    run("ln -s %(current_release)s %(current_path)s" % { 'current_release':env.current_release, 'current_path':env.current_path })

# Apache server tasks, change the command if your server is not ubuntu
@task
def restart():
    """Restarts the apache server"""
    sudo("/etc/init.d/apache2 restart")