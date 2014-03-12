"""
    Sample plugin
"""
from base_plugin import BasePlugin
import os
import re

class Plugin(BasePlugin):
    def __init__(self, project_base_dir=None):
        self.name               = "docker_jenkins"
        self.project_dir_name   = "docker_jenkins"
        self.git_repo           = "https://github.com/sabhiram/docker-jenkins"
        
        # Super Init...
        BasePlugin.__init__(self, project_base_dir)


    def install_dependencies(self):
        print "Sample install_dependencies() called"
        # TODO: Add calls to run any dependencies


    def build(self):
        print "Sample build() called"
        