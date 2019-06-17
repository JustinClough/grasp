import sys
import os
import shutil
import subprocess
import meshio
import math

# project classes in other files
from settings import Setting
from problem import Problem


# FIXME: There is duplicated code between
#        this file and make_surface.py


# Read the settings file into memory
def get_input_settings():
    settings = Setting()
    settings.load_from_file();
    return settings

# Copy the base input scripts into this build
# directory
## Throws error if the directory already exists
def copy_base_input_scripts( settings):
    build_dir = settings.build_dir
    base_dir  = settings.base_inputs

    settings.local_bases = build_dir + "/local_base"

    os.chdir( build_dir)
    os.mkdir( settings.local_bases)
    bases = os.listdir( base_dir)
    for file in bases:
        full_file_path = os.path.join( base_dir, file)
        if( os.path.isfile( full_file_path)):
            shutil.copy( full_file_path, settings.local_bases)
    return None

# Step through problems, solving each.
# Branch-and-cut method currently used for configuration stepping.
def run_problem_loop( settings):
    # FIXME: Should get these from the settings file
    init_number_ribs  = 1
    init_number_spars = 1

    # Create and solve the first problem configuration
    first_problem = Problem()
    first_problem.init_problem( init_number_ribs, init_number_spars, settings, None)

    first_problem.solve()
    min_deflection = first_problem.max_deflection


    # Create the child problems of this configuration and solve those.
    # Do so until we meet the user define deflection limit or
    # hit the fail safe
    fail_safe = 0
    root = first_problem
    while fail_safe < settings.maximum_tree_levels and min_deflection > settings.max_allowable_deflection:
        fail_safe = fail_safe + 1
        # Get child problems from current root
        childs = root.create_child_problems()

        more_ribs = childs[0]
        more_ribs.solve()

        more_spars = childs[1]
        more_spars.solve()

        msg = "Adding more ribs gave max deflection  = " + repr( more_ribs.max_deflection) + "\n"
        msg+= "Adding more spars gave max deflection = " + repr( more_spars.max_deflection) + "\n"
        print( msg)

        if more_ribs.max_deflection < more_spars.max_deflection:
            root = more_ribs
        else:
            root = more_spars

        min_deflection = root.max_deflection

    msg = "Finished! \n"
    msg+= "Final problem description: \n"
    print( msg)
    root.print_description()

    return None

# See if the user needs help
def needs_help():
    cmd_line_args_given = (len(sys.argv) > 1)

    return cmd_line_args_given

# Print helpful (?) info to the user
def print_help():
    msg = "This is the Guided Rib and Spar Placement (GRASP) program!\n"
    msg+= "Modify `aux/setup.sh` to match your system.\n"
    msg+= "Then:  `source aux/setup.sh` \n"
    msg+= "Finally `cd` to the `build` directory and `python ../src/grasp.py`.\n"
    msg+= "\n"
    sys.exit( msg)

    return None


def main():
    if needs_help():
        print_help()
    settings = get_input_settings()
    copy_base_input_scripts( settings)
    run_problem_loop( settings)


if __name__ == "__main__":
    main()
