import os
import sys
from enum import Enum

# Enumeration of test types
class Test_type( Enum):
    deflection = 0
    torsion    = 1

# In memory storage for user defined settings
class Setting:
    # TODO: Add sanity checks for user input.
    #       E.g., do not allow negative max deflections.

    # Full paths to exec files
    esp_exe    = ""
    gmsh_exe   = ""
    albany_exe = ""

    # Full paths to useful directories
    grasp_root  = ""
    base_inputs = ""
    build_dir   = ""
    local_bases = ""

    # Maximum allowable deflection
    max_allowable_deflection = 0.0
    total_weight = 0.0

    # Material Properties
    elastic_modulus = 0.0
    poisson_ratio   = 0.0

    # Test types
    test_type = None

    # Number of threads to use
    num_threads = 0

    # Order of mesh
    mesh_order = 0

    # Component thicknesses
    rib_thickness  = 0.0
    spar_thickness = 0.0

    # Wing parameters
    naca_series  = 0
    span         = 0.0
    c_tip        = 0.0
    c_root       = 0.0
    sweep_length = 0.0

    # Fail safe to keep out of infinite loops
    maximum_tree_levels = 0

    # Check if the settings file exists
    def check_for_settings_file( self):
        found_settings_file = os.path.isfile('settings.txt')
        if not found_settings_file:
            message = "Cannot Find settings.txt! \n"
            message +="Run aux/setup.sh and call from build dir.\n"
            print( message)
            print_help()

        return None
    
    # Load settings from the settings file. 
    # Populates this class.
    def load_from_file( self):
        self.check_for_settings_file()
        file = open("settings.txt", "r")

        lines = file.readlines()
        for line in lines:
            name  = line.split('=')[0]
            value = line.split('=')[1].rstrip()

            if  name == "GRASP_ROOT":
                self.grasp_root = value;
            elif name == "GRASP_ALBANY_EXE":
                self.albany_exe = value;
            elif name == "GRASP_ESP_EXE":
                self.esp_exe = value;
            elif name == "GRASP_GMSH_EXE":
                self.gmsh_exe = value;
            elif name == "GRASP_BUILD_DIR":
                self.build_dir = value;
            elif name == "GRASP_BASE_DIR":
                self.base_inputs = value;
            elif name == "MAX_DEFLECTION":
                self.max_allowable_deflection = float(value)
            elif name == "WEIGHT":
                self.total_weight = float( value)
            elif name == "ELASTIC_MODULUS":
                self.elastic_modulus = float( value)
            elif name == "POISSON_RATIO":
                self.poisson_ratio = float( value)
            elif name == "TEST_TYPE":
                if   value == "DEFLECTION":
                    test_type = Test_type.deflection
                elif value == "TORSION":
                    test_type = Test_type.torsion
            elif name == "MAXIMUM_TREE_LEVELS":
                self.maximum_tree_levels = int( value)
            elif name == "NUM_THREADS":
                self.num_threads = int( value)
            elif name == "MESH_ORDER":
                self.mesh_order = int( value)
            elif name == "RIB_THICKNESS":
                self.rib_thickness = float( value)
            elif name == "SPAR_THICKNESS":
                self.spar_thickness = float( value)
            elif name == "NACA_SERIES":
                self.naca_series = int( value)
            elif name == "SPAN":
                self.span = float( value)
            elif name == "C_ROOT":
                self.c_root = float( value)
            elif name == "C_TIP":
                self.c_tip = float( value)
            elif name == "SWEEP_LENGTH":
                self.sweep_length = float( value)
            else:
                message = "Unrecognized settings option:\n"
                message+= name + "\n\n"
                message+= "With value: \n"
                message+= value + "\n\n"
                sys.exit( message)

        return None


