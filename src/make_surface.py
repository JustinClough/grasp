import sys
import os
import shutil
import subprocess
import meshio
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# project classes in other files
from settings import Setting
from problem import Problem

# FIXME: There is duplicated code between
#        this file and grasp.py

# Read the settings file into memory
def get_input_settings():
    settings = Setting()
    settings.load_from_file();

    return settings

def copy_base_input_scripts( settings):
    build_dir = settings.build_dir
    base_dir  = settings.base_inputs

    settings.local_bases = build_dir + "/local_base"

    os.chdir( build_dir)

    if not os.path.isdir( settings.local_bases):
        os.mkdir( settings.local_bases)
        bases = os.listdir( base_dir)
        for file in bases:
            full_file_path = os.path.join( base_dir, file)
            if( os.path.isfile( full_file_path)):
                shutil.copy( full_file_path, settings.local_bases)

    return None

# Create and solve problem configurations to populate a 
# matrix of maximum deflection values
def create_surface_data( settings, min_ribs, min_spars, max_ribs, max_spars):
    num_ribs_to_try  = max_ribs  - min_ribs  + 1
    num_spars_to_try = max_spars - min_spars + 1

    max_displacements = np.zeros( (num_ribs_to_try, num_spars_to_try))

    rib_it_count = 0
    for num_ribs in range( min_ribs, max_ribs+1):
        spar_it_count = 0
        for num_spars in range( min_spars, max_spars+1):
            problem = Problem()
            problem.init_problem( num_ribs, num_spars, settings, None)
            problem.solve()
            max_displacements[rib_it_count, spar_it_count] = problem.max_deflection

            msg = "Max deflection is: " + repr( problem.max_deflection) + "\n"
            print( msg)
            spar_it_count += 1
        rib_it_count += 1

    return max_displacements

# Create a surface plot of max_displacements
def plot_surface_data( max_displacements, min_ribs, min_spars, max_ribs, max_spars):
    fig = plt.figure()
    ax = fig.add_subplot( 111, projection='3d')

    ribs  = range( min_ribs,  max_spars+1)
    spars = range( min_spars, max_spars+1)

    X, Y = np.meshgrid( spars, ribs)
    Z = max_displacements.reshape( X.shape)

    ax.plot_surface( X, Y, Z)

    ax.set_xlabel('Number of Spars')
    ax.set_ylabel('Number of Ribs')
    ax.set_zlabel('Maximum Displacement Magnitude')

    plt.show()
    
    return None

# Save the matrix max_displacements to disk
def save_displacement_data( settings, max_displacements):
    os.chdir( settings.build_dir)
    np.savetxt('max_displacements.txt', max_displacements, fmt='%f')
    return None

# Check to see if the max_displacements file has been writen
def check_for_max_disp_file( settings):
    os.chdir( settings.build_dir)
    ans = os.path.isfile('max_displacements.txt')
    return ans

# Load the max_displacements from disk
def load_max_disp_file( settings):
    os.chdir( settings.build_dir)
    max_displacements = np.loadtxt('max_displacements.txt', dtype=float)
    return max_displacements

def needs_help():
    cmd_line_args_given = (len(sys.argv) > 1)

    return cmd_line_args_given

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

    min_ribs  = 1
    min_spars = 1

    max_ribs  = 4
    max_spars = 4

    if not check_for_max_disp_file( settings):
        max_displacements = create_surface_data( settings, min_ribs, min_spars, max_ribs, max_spars)
        save_displacement_data( settings, max_displacements)
    else:
        max_displacements = load_max_disp_file( settings)

    plot_surface_data( max_displacements, min_ribs, min_spars, max_ribs, max_spars)

    return None


if __name__ == "__main__":
    main()
