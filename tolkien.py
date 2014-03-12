'''
	Tolkien is a simply python framework for pulling git repos, and 
	building them. This can also include the scripts necessary to 
	install any dependencies needed to "build" a sub-project. Each
	sub-project will be managed using its own git interface.

	Tolkien also assumes you will have the 'homebrew' package manager
	installed to fetch other OSX related dependencies.
	Source: https://github.com/mxcl/homebrew
'''
import argparse
import os, sys, subprocess
import re
import time


PLUGIN_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'plugins')
TOLKIEN_HEADER = """#################################################################
##                                                             ##
##             Tolkien v0.1  - Scripting framework             ##
##                                                             ##
#################################################################
"""


"""
Function:
	validate_brew_install
Inputs:
	None
Outputs:
	True / False if brew is installed
"""
def validate_brew_install():
    brew_installed = False
    try:
        brew_path = subprocess.check_output('which brew', shell=True)
        brew_installed = True
    except:
        print "brew installation not found..."
    return brew_installed


"""
Function:
	attempt_brew_install
Inputs:
	None
Outputs:
	None if install success - Error otherwise
"""
def attempt_brew_install():
    error = None
    os.system('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"')
    if validate_brew_install() == False:
        error = "Unable to install homebrew... aborting"
    return error


"""
Function:
	load_plugins
Inputs:
	args 	- arg parse arguments
Outputs:
	error 	- Error object or string [default = None] 
	plugins - Imported plugins which we can update / call functions on
Description:
	Load plugins from the 'plugins' dir, these will determine
	how we can build, and update our sub-projects
"""
def load_plugins(args):
	error, plugins = None, []
	sys.path.append(args.plugin_dir)
	for dirpath, dirs, files in os.walk(args.plugin_dir):
		for f in files:
			if f.endswith(".py"):
				fname, ext = os.path.splitext(f)
				plugin_module = __import__(fname, fromlist=["Plugin"])
				Plugin_ = getattr(plugin_module, "Plugin")
				plugin = Plugin_(args.output_dir)
				#print "Imported plugin " + plugin.name
				plugins.append(plugin)
	return error, plugins


"""
Function:
	purge_subproject
Inputs:
	plugin 	- The subproject we wish to purge's plugin
Outputs:
	error 	- Error object or string [default = None] 
Description:
	Given a plugin, invokes the purge function 
"""
def purge_subproject(plugin):
	error = None
	return plugin.purge()


"""
Function:
	update_subproject
Inputs:
	plugin 	- The plugin we wish to clone / update
Outputs:
	error 	- Error object or string [default = None] 
Description:
	Given a plugin, invokes the update function to pull / update
	a sub-project's git repo
"""
def update_subproject(plugin):
	error = None
	return plugin.update()


"""
Function:
	build_subproject
Inputs:
	plugin 	- The plugin we wish to build
Outputs:
	error 	- Error object or string [default = None] 
Description:
	Given a plugin, invokes the build function to build a
	given sub-project
"""
def build_subproject(plugin):
	error = None
	return plugin.build()


"""
Function:
	install_subproject_deps
Inputs:
	plugin 	- The plugin we wish to install dependencies for
Outputs:
	error 	- Error object or string [default = None] 
Description:
	Given a plugin, invokes the the install of any dependencies
"""
def install_subproject_deps(plugin):
	error = None
	return plugin.install_dependencies()


"""
Function:
	filter_plugins
Inputs:
	plugins 	- array of plugins we wish have loaded
	user_plugins- array of plugins the user wants us to process
Outputs:
	Yields a list of matching plugins
"""
def filter_plugins(plugins, user_plugins):
	for u_p in user_plugins:
		found_up = False
		for p in plugins:
			if p.name.lower() == u_p.lower():
				yield p
				found_up = True
				break
		if found_up == False:
			print "Did not find plugin for project: " + u_p


def main():
	print TOLKIEN_HEADER
	# Setup parser
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--clean", action="store_true", help="Purge a sub-project. This will removal all subproject folders!")
	parser.add_argument("-u", "--update", action="store_true", help="Fetch / Update the sub-project repos.")
	parser.add_argument("-b", "--build", action="store_true", help="Build each sub-project (and install any dependencies).")
	parser.add_argument("-d", "--dependencies", action="store_true", help="Install any dependencies for the sub-project.")
	parser.add_argument("-p", "--plugin_dir", help="Path where plugin folders exist.")
	parser.add_argument("-o", "--output_dir", help="Path where sub-projects will be fetched.")
	parser.add_argument("subprojects", nargs="+", help="The sub-projects we wish to build / update. All for all of them.")

	# Parse args
	args = parser.parse_args()

	if args.plugin_dir == None:
		args.plugin_dir = PLUGIN_DIR

	if args.output_dir == None:
		args.output_dir = os.getcwd()
		print ""
		print "Using CWD as output directory - " + args.output_dir

	# Load "plugins"
	error, plugins = load_plugins(args)
	if error:
		print ""
		print "Unable to load plugins, exiting with error: " + error
		sys.exit()

	# Check for "homebrew" install
	print ""
	print "Checking homebrew install"
	if validate_brew_install() == False:
		error = attempt_brew_install()

	# List plugins which were found
	print ""
	print "Loaded the following plugins from %s"%(args.plugin_dir)
	for plugin in plugins:
		print "* %s"%(plugin.name)

	# Filter plugins so we operate on the ones we care about
	if not (len(args.subprojects) == 1 and args.subprojects[0].lower() == 'all'):
		# Filter plugins so we only use the ones we care about...
		plugins = list(filter_plugins(plugins, args.subprojects))

	# Iterate over valid plugins
	for plugin in plugins:
		#plugin.print_plugin_info()
		p_error = None

		# Purge plugins (... if needed)
		if args.clean:
			print ""
			print "Purging sub-projects for %s..."%(plugin.name)
			p_error = purge_subproject(plugin)

		# Update plugins (... if needed)
		if args.update and p_error == None:
			print ""
			print "Updating sub-projects for %s..."%(plugin.name)
			p_error = update_subproject(plugin)

		# Install their deps (... if needed)
		if args.dependencies and p_error == None:
			print ""
			print "Installing sub-project dependencies for %s..."%(plugin.name)
			p_error = install_subproject_deps(plugin)

		# Build them (... if needed)
		if args.build and p_error == None:
			print ""
			print "Building sub-projects for %s..."%(plugin.name)
			p_error = build_subproject(plugin)

		# Error?
		if p_error:
			print "ERROR: [Plugin: %s] - %s"%(plugin.name, p_error)

	# Done
	print ""
	print "Farewell!"
	sys.exit(0)

if __name__ == "__main__":
	main()
# END OF FILE