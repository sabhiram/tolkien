Tolkien
=======

A plugin-based git sub-project manager


Project Structure:
------------------

     |- tolkien.py
     |- base_plugin.py
     |- plugins
        |- foo.py
        |- bar.py
        |- ...

 * ***tolkien.py*** -- Main entry-point. Contains all the logic to load the various plugins.
 * ***base_plugin.py*** -- Base plugin from which other plugins derive from. Includes functions like build, update, purge etc, as well as other helper functions like run and run_lines.
 * ***plugins*** - Folder of plugins which we wish to operate on, these can be any valid path and does not need to be relative to the other py files.


Plugin Anatomy:
---------------

A plugin must have the following signature:

    class Plugin(BasePlugin):
    def __init__(self, project_base_dir=None):
        self.name               = "FOO"
        self.project_dir_name   = "foo"
        self.git_repo           = "https://foobar.com/foo.git"
        
        # Super Init...
        BasePlugin.__init__(self, project_base_dir)

 * ***name*** -- This refers to the name of the sub-project. This is the name we select this sub-project with.
 * ***project_dir_name*** -- The name where Tolkien will fetch this particular sub-project.
 * ***git_repo*** -- Path to git repo with sub-project files


Plugins may optionally implement the following overrides:
---------------------------------------------------------

    def install_dependencies(self):
        self.run('./install_deps.sh', some_path)
        self.run('echo "any statement you want"')

 and / or

    def build(self):
        self.run('./build.sh', some_path)
        self.run('echo "any other statements you want"')


Sample Usage:
-------------

Tolkien help:

    $python tolkien.py -h
    usage: tolkien.py [-h] [-c] [-u] [-b] [-d] [-p PLUGIN_DIR] [-o OUTPUT_DIR] subprojects [subprojects ...]
    
    positional arguments:
      subprojects           The sub-projects we wish to build / update. All for all of them.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c, --clean           Purge a sub-project. This will removal all subproject folders!
      -u, --update          Fetch / Update the sub-project repos.
      -b, --build           Build each sub-project (and install any dependencies).
      -d, --dependencies    Install any dependencies for the sub-project.
      -p PLUGIN_DIR, --plugin_dir PLUGIN_DIR
                            Path where plugin folders exist.
      -o OUTPUT_DIR, --output_dir OUTPUT_DIR 
                            Path where sub-projects will be fetched.

Purge project dirs for sub-project "foo"
> $python tolkien.py -c foo

Purge, and update sub-projects "foo" and "BAR"
> $python tolkien.py -c -u foo bar

Purge, and update sub-projects "BAR" then "foo" in that order
> $python tolkien.py -c -u bar foo

Update, install dependencies and then build for all sub-projects (all "plugins" found)
> $python tolkien.py -u -d -b All

Purge sub-project "foo" but use a specific plugins dir
> $python tolkien.py -c -p ./plugins/test_plugins foo

Purge sub-project "foo" from output dir "output"
> $python tolkien.py -c -o ./output foo

