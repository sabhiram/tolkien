import os
import subprocess

class BasePlugin:
	def __init__(self, project_base_dir=None):
		if self.name == None:
			print "Error initializing BasePlugin! Plugin Name is not defined!"
		if self.git_repo == None:
			print "Error initializing BasePlugin! Plugin Git Repo is not defined!"
		if self.project_dir_name == None:
			print "Error initializing BasePlugin! Plugin Project Folder Name is not defined!"
		
		# Setup the base dir for the project we care about
		if project_base_dir == None:
			self.project_dir = os.path.join(os.getcwd(), self.project_dir_name)
		else:
			self.project_dir = os.path.join(project_base_dir, self.project_dir_name)


	"""
		Plugin info for debug etc
	"""
	def print_plugin_info(self):
		print ""
		print "Plugin Name:     " + self.name
		print "Git Repo:        " + self.git_repo
		print "Project Dir:     " + self.project_dir


	"""
		Simple run method which changes dir, then runs a command,
		and then changes dir back to the original working dir.
	"""
	def run(self, cmd, dir=None):
		cwd = os.getcwd();
		if dir != None:
			os.chdir(dir)
		print cmd
		os.system(cmd)
		os.chdir(cwd)


	"""
		Runs a list of lines (optionally in a directory)
	"""
	def run_lines(self, lines, dir=None):
		for line in lines:
			self.run(line, dir)


	"""
		Returns a plugins name
	"""
	def name(self):
		return self.name


	"""
		Base purge function which will simply do a "rm -rf <proj dir>"
	"""
	def purge(self):
		if self.project_dir != None and os.path.exists(self.project_dir):
			print "Purging dir: " + self.project_dir
			self.run('rm -rf ' + self.project_dir)
		else:
			print "Nothing to purge " + self.project_dir + " does not exist."


	"""
		Base build function - typically does nothing
	"""
	def build(self):
		print "Base build() called for plugin " + self.name + ". Nothing to do."


	"""
		Base install_dependencies function - typically does nothing
	"""
	def install_dependencies(self):
		print "Base install_dependencies() called for plugin " + self.name + ". Nothing to do."


	"""
		Check to see if brew package is already installed
	"""
	def check_brew_package(self, pkg):
		installed = False
		try:
			cmd = 'brew list | grep %s'%(pkg)
			output = subprocess.check_output(cmd, shell=True)
			if output.strip() == pkg:
				installed = True
		except:
			installed = False
		return installed


	"""
		Install brew package if applicable
	"""
	def install_brew_package(self, pkg):
		try:
			if self.check_brew_package(pkg) == False:
				self.run("brew install %s"%(pkg))
		except:
			print "Exception raised installing brew package %s"%(pkg)
			

	"""
		Base update function - does either a git clone / git pull
	"""
	def update(self):
		if self.project_dir != None and self.project_dir_name != None:
			# Clone project if it does not exist
			if not os.path.exists(self.project_dir):
				os.makedirs(self.project_dir)
				self.run('git clone ' + self.git_repo + ' ' + self.project_dir)
			# The dir exists, so attempt to pull from within it
			else:
				self.run('git pull ' + self.git_repo, self.project_dir)
		else:
			print "Error - project_dir is None"
# END OF FILE
	