import sys
import os
import shutil
import subprocess
import meshio
import math

from settings import Setting
from file_handeler import File_Handeler

# A class to handle a problem configuration 
# and solution method
class Problem:
    # Number of ribs and spar
    num_ribs  = -1
    num_spars = -1

    # Pointers to this problems parent and child problems
    parent = None
    left   = None
    right  = None

    # String of this problem's working directory
    my_dir = ""

    # Maximum deflection of this configuration
    max_deflection = 0.0

    # Pointer to the in memory settings
    settings = None

    # Pointer to the file handeler
    file_handeler = None

    # Boolean of if this problem is solved or not
    is_solved = False

    # Strings of the base input file names
    csm_file_name = ""
    geo_file_name = ""
    alb_file_name = ""
    mat_file_name = ""

    # initialize this problem instance
    def init_problem( self, num_ribs, num_spars, settings, parent):
        self.num_ribs  = num_ribs
        self.num_spars = num_spars
        self.parent    = parent
        self.settings  = settings

        self.file_handeler = File_Handeler()
        self.create_my_dir()
        return None

    # create this problem's working directory
    def create_my_dir( self):
        build_dir = self.settings.build_dir

        dir_name = "/problem_" + repr( self.num_ribs) +"_ribs_" + repr( self.num_spars) + "_spars"
        self.my_dir = build_dir + dir_name

        os.mkdir( self.my_dir)
        return None

    # Print a description of this problem instance
    def print_description( self):
        message = "Problem Description: \n"
        message +="Number of Ribs: "  + repr( self.num_ribs)  + ". \n"
        message +="Number of Spars: " + repr( self.num_spars) + ". \n"
        message +="My Dir is: " + self.my_dir + ".\n"
        print( message)
        return None

    # Create child problem of this one by incrementing 
    # component counts by one each way
    def create_child_problems( self):
        more_ribs = Problem()
        more_ribs.init_problem( self.num_ribs+1, self.num_spars,  self.settings, self)

        more_spars = Problem()
        more_spars.init_problem( self.num_ribs,  self.num_spars+1, self.settings, self)
        return [more_ribs, more_spars]

    # Copy the base input file into this problem's
    # working directory
    def copy_bases_to_my_dir( self):
        bases = os.listdir( self.settings.local_bases)
        for file in bases:
            full_file_path = os.path.join( self.settings.local_bases, file)
            if os.path.isfile( full_file_path):
                shutil.copy( full_file_path, self.my_dir)
                new_file_path = os.path.join( self.my_dir, file)

                # FIXME: this will also copy vim's swp files 
                #        from the base dir. Causes downstream
                #        errors and crashes.

                if   "wing_spars_ribs.csm" in new_file_path:
                    self.csm_file_name = new_file_path
                elif "material.yaml" in new_file_path:
                    self.mat_file_name = new_file_path
                elif "albany.yaml" in new_file_path:
                    self.alb_file_name = new_file_path
                elif "mesh_wing.geo" in new_file_path:
                    self.geo_file_name = new_file_path
                else:
                    msg = "Copied file: " + full_file_path + "\n"
                    msg+= "But unsure what it is used for!\n"
                    msg+= "Exiting...\n\n"
                    sys.exit( msg)
        return None

    # Get the number of components this configuration has by name
    def get_component_count( self, component):
        if component == "ribs":
            comp_count = self.num_ribs
        elif component == "spars":
            comp_count = self.num_spars
        else:
            msg = "Unknown component: " + component + "\n"
            msg+= "Exiting..."
            print( msg)
        return comp_count
        

    # Get the text to restore and dump components files for the csm script
    def get_restore_dump_text( self, component):
        comp_count = self.get_component_count( component)

        template_restore_text = "restore COMP NUM 0\n"
        template_dump_text    = "dump COMP/COMP_NUM.stp 1 0\n"

        full_text = ""
        restore_count = 2
        dump_count    = 1
        for i in range( comp_count):
            restore = template_restore_text.replace( "NUM", str( restore_count))
            dump    = template_dump_text.replace( "NUM", str( dump_count))

            restore = restore.replace( "COMP", component)
            dump = dump.replace( "COMP", component)

            full_text     += restore + dump
            restore_count += 1
            dump_count    += 1

        return full_text


    # Edit the base csm script to match this problem configuration
    def edit_csm_script( self):

        self.file_handeler.read_file( self.my_dir, self.csm_file_name)

        self.file_handeler.replace( "GRASP_NACA_SERIES", 
                                    str( self.settings.naca_series))
        self.file_handeler.replace( "GRASP_RIB_THICKNESS", 
                                    str( self.settings.rib_thickness))
        self.file_handeler.replace( "GRASP_SPAR_THICKNESS", 
                                    str( self.settings.spar_thickness))

        self.file_handeler.replace( "GRASP_NUM_RIBS", str( self.num_ribs))
        self.file_handeler.replace( "GRASP_NUM_SPARS", str( self.num_spars))

        self.file_handeler.replace( "GRASP_NUM_RIBS", str( self.num_ribs))
        self.file_handeler.replace( "GRASP_NUM_SPARS", str( self.num_spars))

        self.file_handeler.replace( "GRASP_CHORD_ROOT", 
                                    str( self.settings.c_root))
        self.file_handeler.replace( "GRASP_SWEEP_LENGTH", 
                                    str( self.settings.sweep_length))
        self.file_handeler.replace( "GRASP_SPAN", 
                                    str( self.settings.span))
        self.file_handeler.replace( "GRASP_CHORD_TIP", 
                                    str( self.settings.c_tip))

        restore_dump_ribs = self.get_restore_dump_text( "ribs")
        restore_dump_spars = self.get_restore_dump_text( "spars")

        self.file_handeler.replace( "GRASP_RESTORE_DUMP_RIBS", restore_dump_ribs)
        self.file_handeler.replace( "GRASP_RESTORE_DUMP_SPARS", restore_dump_spars)

        self.file_handeler.write_file()
        return None


    # Get the text to fragment and union components in the geo script
    def get_frag_union_text( self, component):
        comp_count = self.get_component_count( component)

        
        template_read_text = "COMP_NUM_v() = ShapeFromFile( \"COMP/COMP_NUM.stp\");\n"
        template_frag_text = "frag_COMP_NUM() = BooleanFragments{ Volume{ union()}; Delete; }{ Volume{ COMP_NUM_v()}; Delete; };\n"
        template_union_text = "union() = BooleanUnion{ Volume{ union()}; Delete; }{ Volume{:}; Delete;};\n"

        full_text = ""
        blank_line = "\n"
        for i in range( comp_count):
            read  = template_read_text.replace( "COMP", component)
            frag  = template_frag_text.replace( "COMP", component)
            union = template_union_text.replace( "COMP", component)

            read  = read.replace( "NUM", str( i+1))
            frag  = frag.replace( "NUM", str( i+1))
            union = union.replace( "NUM", str( i+1))

            # Skip the first spar since it's the base of the unions
            if not (i==0 and component=="spars"):
                full_text += read + frag + union + blank_line
        return full_text

    # Get the text to label spar roots in the geo script
    def get_spar_root_label_text( self):
        spar_width = self.settings.spar_thickness
        chord_root = self.settings.c_root

        template_find   = "spar_NUM_root() = Surface In BoundingBox{ XMIN-eps, -1.0-eps, -10.0-eps, XMAX+eps, 0.5+eps, 10.0+eps};\n"
        template_assign = "Physical Surface(\"spar_NUM_root_surface\") = {spar_NUM_root()};\n"
        template_print  = "Printf(\"spar_NUM_root tag = %g\", spar_NUM_root[0]);\n"

        full_text = ""
        spar_spacing = chord_root /( float(self.num_spars) + 1.0)
        for i in range( self.num_spars):
            find   = template_find.replace( "NUM", str(i+1))
            assign = template_assign.replace( "NUM", str(i+1))
            print_ = template_print.replace("NUM", str(i+1))

            xmin = (i+1)*spar_spacing-spar_width
            xmax = (i+1)*spar_spacing+spar_width

            find = find.replace( "XMAX", str( xmax))
            find = find.replace( "XMIN", str( xmin))

            full_text += find
            full_text += assign
            full_text += print_

        return full_text



    # Edit the base geo script for Gmsh
    def edit_geo_script( self):
        self.file_handeler.read_file( self.my_dir, self.geo_file_name)

        frag_union_spars = self.get_frag_union_text( "spars")
        frag_union_ribs  = self.get_frag_union_text( "ribs")
        
        self.file_handeler.replace( "GRASP_FRAG_UNION_SPARS", frag_union_spars)
        self.file_handeler.replace( "GRASP_FRAG_UNION_RIBS", frag_union_ribs)

        self.file_handeler.replace( "GRASP_SPAN", str(self.settings.span))

        label_spar_roots = self.get_spar_root_label_text()
        self.file_handeler.replace( "GRASP_WING_ROOT_SURFACES", label_spar_roots)

        self.file_handeler.write_file()
        return None


    # Edit the base material script for Albany
    def edit_material_script( self):
        self.file_handeler.read_file( self.my_dir, self.mat_file_name)

        self.file_handeler.replace( "GRASP_ELASTIC_MODULUS", str( self.settings.elastic_modulus))
        self.file_handeler.replace( "GRASP_POISSON_RATIO", str( self.settings.poisson_ratio))
        
        tet10_text = ""
        if self.settings.mesh_order > 1:
            tet10_text = "Use Composite Tet 10: true"
        self.file_handeler.replace( "GRASP_TET10", tet10_text )

        self.file_handeler.write_file()
        return None

    # Determine the magnitude of the uniform upward pressure
    # to set the Nuemann Boundary Condition
    def calculate_uniform_pressure( self):
        rib_thickness  = self.settings.rib_thickness
        spar_thickness = self.settings.spar_thickness

        chord_tip  = self.settings.c_tip
        chord_root = self.settings.c_root

        span = self.settings.span

        # FIXME: Area is approxmiated...
        # Assumes: 
        # - all ribs are same length (average chord)
        # - all spars are same length (full span)
        # Should instead interogate the mesh directly

        rib_area  = rib_thickness*(chord_tip+chord_root)/2.0
        spar_area = spar_thickness*span

        total_rib_area  = self.num_ribs  * rib_area
        total_spar_area = self.num_spars * spar_area
        
        area =  total_rib_area + total_spar_area

        # Subtract out the overlapped pieces
        num_overlaps = self.num_ribs * self.num_spars
        overlap_area = rib_thickness * spar_thickness

        area-= overlap_area

        weight = self.settings.total_weight
        pressure = weight/area
        
        return pressure

    # Get the text to set the Strong Dirichlet Boundary Condition
    def get_SDBC_wing_root_text( self):

        # Do not remove leading whitespace, 
        # YAML is white space sensetive
        template_sdbc = "      SDBC on NS BoundaryNodeSet_spar_NUM_root_surface for DOF XYZ: 0.0\n"

        full_text = ""
        for i in range( self.num_spars):
            sdbc = template_sdbc.replace( "NUM", str(i+1))

            sdbc_x = sdbc.replace( "XYZ", "X")
            sdbc_y = sdbc.replace( "XYZ", "Y")
            sdbc_z = sdbc.replace( "XYZ", "Z")

            full_text += sdbc_x
            full_text += sdbc_y
            full_text += sdbc_z
        return full_text

    # Edit the base Albany input script
    def edit_alb_script( self):
        self.edit_material_script()
        self.file_handeler.read_file( self.my_dir, self.alb_file_name)

        pressure = self.calculate_uniform_pressure()
        self.file_handeler.replace( "GRASP_PRESSURE", str(pressure))

        SDBC_wing_roots = self.get_SDBC_wing_root_text()
        self.file_handeler.replace( "GRASP_ASSIGN_SDBC", SDBC_wing_roots)
        

        cubature = 1
        if self.settings.mesh_order > 1:
            cubature = 3
        self.file_handeler.replace( "GRASP_CUBATURE_DEGREE", str(cubature))

        self.file_handeler.write_file()
        return None

    # Edit the input files for this problem configuration
    def edit_inputs( self):
        os.chdir( self.my_dir)
        self.edit_csm_script()
        self.edit_geo_script()
        self.edit_alb_script()
        return None

    # Call ESP as a subprocess
    def call_esp( self):
        print("Calling ESP...")

        spars_dir = self.my_dir + "/spars"
        ribs_dir = self.my_dir + "/ribs"

        os.mkdir( spars_dir)
        os.mkdir( ribs_dir)

        esp_stderr = open( "esp_stderr.txt", "w")
        esp_stdout = open( "esp_stdout.txt", "w")

        args = self.settings.esp_exe + " "
        args+= self.csm_file_name + " "
        args+= "-batch "

        subprocess.call( args, stdout=esp_stdout, stderr=esp_stderr, shell=True)
        self.check_subprocess_errors( "ESP", esp_stderr, True)

        esp_stderr.close()
        esp_stdout.close()
        return None


    # Call Gmsh as a subprocess
    def call_gmsh( self):
        print("Calling GMSH...")
        gmsh_stderr = open( "gmsh_stderr.txt", "w")
        gmsh_stdout = open( "gmsh_stdout.txt", "w")

        args = self.settings.gmsh_exe + " "
        args+= self.geo_file_name + " "
        args+= " -3 "
        if self.settings.mesh_order > 1:
            args+= " -order " + repr( self.settings.mesh_order) + " "

        if self.settings.num_threads > 1:
            args+= "-nt " + repr( self.settings.num_threads) + " "

        subprocess.call( args, stdout=gmsh_stdout, stderr=gmsh_stderr, shell=True)
        self.check_subprocess_errors( "GMSH", gmsh_stderr, False)

        gmsh_stderr.close()
        gmsh_stdout.close()
        return None


    # Call Albany as a subprocess
    def call_albany( self):
        print("Calling Albany...")
        albany_stderr = open( "albany_stderr.txt", "w")
        albany_stdout = open( "albany_stdout.txt", "w")

        args = self.settings.albany_exe + " "
        args+= self.alb_file_name 

        if self.settings.num_threads > 1:
            mpi_args = "mpirun -n " + repr( self.settings.num_threads) + " "
            args = mpi_args + args

        subprocess.call( args, stdout=albany_stdout, stderr=albany_stderr, shell=True)
        self.check_subprocess_errors( "Albany", albany_stderr, True)

        albany_stderr.close()
        albany_stdout.close()

        return None

    # Check a subprocess for errors by measuring the error file size
    def check_subprocess_errors( self, processs_name, stderr, exit_on_errors):
        err_size = os.path.getsize( stderr.name)
        if err_size > 0:
            msg = "Errors were encountered when running: " + processs_name + "\n"

            if exit_on_errors:
                msg+= "Check file: " + stderr.name + "\n"
                msg+= "Exiting..."
                sys.exit( msg)

            else:
                err_file = open( stderr.name)
                file_lines = err_file.readlines()

                msg+= "Continuing on... \n"
                msg+= "  Print out of " + err_file.name + ": \n"
                for line in file_lines:
                    msg+= line
                err_file.close()
                print( msg)
        return None


    # Read the exodus file from the Albany solve;
    # determine the maximum displacement
    def read_exo_file( self):
        print("Reading results...")

        results_file_name = "results.exo"
        if self.settings.num_threads > 1:
            results_file_name += "." + repr( self.settings.num_threads)
            # FIXME
            msg = "meshio cannot handle  parallel exo files!\n"
            msg+= "Exiting..."
            sys.exit( msg)
            

        exo = meshio.read( results_file_name)

        sol_x = exo.point_data[ "solution_x"]
        sol_y = exo.point_data[ "solution_y"]
        sol_z = exo.point_data[ "solution_z"]

        solution_mag_max = 0.0
        for i in range( len( sol_x)):
            x = sol_x[i]
            y = sol_y[i]
            z = sol_z[i]

            mag = math.sqrt(x*x + y*y + z*z)
            if mag > solution_mag_max:
                solution_mag_max = mag
            
        self.max_deflection = solution_mag_max
        return None

    # Solve this problem configuration
    def solve( self):
        print("Solving...")
        self.print_description()

        self.copy_bases_to_my_dir()
        self.edit_inputs()

        self.call_esp()
        self.call_gmsh()
        self.call_albany()

        self.read_exo_file()

        print("Finished solving! \n\n")
        self.is_solved = True
        return None
