#!/bin/bash

# Modify the below to match your system
GRASP_ROOT=/home/jlclough/research/grasp
GRASP_ALBANY_EXE=/home/jlclough/research/Albany/build/src/Albany
GRASP_ESP_EXE=/home/jlclough/research/EngSketchPad/bin/serveCSM
GRASP_GMSH_EXE=/home/pogo/gmsh-4.2.0-Linux64/bin/gmsh

# Modify the below to match your problem
# Using material properties of Ti6Al4V 
# Pressures in units of MPa
MAX_DEFLECTION=0.01
WEIGHT=3.2706540        # MN
ELASTIC_MODULUS=68900.0 # MPa
POISSON_RATIO=0.33
TEST_TYPE=DEFLECTION
MAXIMUM_TREE_LEVELS=20
NUM_THREADS=1
MESH_ORDER=2
RIB_THICKNESS=5.0  #mm
SPAR_THICKNESS=30.0 #mm
NACA_SERIES=9615
SPAN=26570.0   # mm
C_ROOT=13347.0 # mm
C_TIP=3790.6   # mm
SWEEP_LENGTH=20400.0 #mm


## Do not modify below ##

# Create build dir, destroy previous one if it exists
BUILD_DIR=${GRASP_ROOT}/build
if [ -d "$BUILD_DIR" ]; then
  echo ""
  rm -vr $BUILD_DIR
  echo ""
fi
mkdir $BUILD_DIR
echo "Destroyed old $BUILD_DIR, Created new one."
echo ""

# Move to build directory to create settings.txt file
cd $BUILD_DIR
touch settings.txt

# Add additional info
echo "GRASP_ROOT=${GRASP_ROOT}"                   >> settings.txt
echo "GRASP_ALBANY_EXE=${GRASP_ALBANY_EXE}"       >> settings.txt
echo "GRASP_ESP_EXE=${GRASP_ESP_EXE}"             >> settings.txt
echo "GRASP_GMSH_EXE=${GRASP_GMSH_EXE}"           >> settings.txt
echo "GRASP_BUILD_DIR=${GRASP_ROOT}/build"        >> settings.txt
echo "GRASP_BASE_DIR=${GRASP_ROOT}/base_inputs"   >> settings.txt
echo "MAX_DEFLECTION=${MAX_DEFLECTION}"           >> settings.txt
echo "WEIGHT=${WEIGHT}"                           >> settings.txt
echo "ELASTIC_MODULUS=${ELASTIC_MODULUS}"         >> settings.txt
echo "POISSON_RATIO=${POISSON_RATIO}"             >> settings.txt
echo "TEST_TYPE=${TEST_TYPE}"                     >> settings.txt
echo "MAXIMUM_TREE_LEVELS=${MAXIMUM_TREE_LEVELS}" >> settings.txt
echo "NUM_THREADS=${NUM_THREADS}"                 >> settings.txt
echo "MESH_ORDER=${MESH_ORDER}"                   >> settings.txt
echo "RIB_THICKNESS=${RIB_THICKNESS}"             >> settings.txt
echo "SPAR_THICKNESS=${SPAR_THICKNESS}"           >> settings.txt
echo "NACA_SERIES=${NACA_SERIES}"                 >> settings.txt
echo "SPAN=${SPAN}"                               >> settings.txt
echo "C_ROOT=${C_ROOT}"                           >> settings.txt
echo "C_TIP=${C_TIP}"                             >> settings.txt
echo "SWEEP_LENGTH=${SWEEP_LENGTH}"               >> settings.txt

echo "Created settings.txt file."

cd $BUILD_DIR

