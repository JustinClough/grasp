#!/bin/bash

# Grab esp essentials
export ESP_ROOT=/home/jlclough/research/EngSketchPad
export ESP_START="/usr/bin/firefox $ESP_ROOT/ESP/ESP.html"
source $ESP_ROOT/ESPenv.sh
ESP_EXEC=${ESP_ROOT}/bin/serveCSM

# Point to GMSH exec
GMSH_4_2_EXEC=/home/pogo/gmsh-4.2.0-Linux64/bin/gmsh

# Point to Albany exec (using dev not base)
ALBANY_EXEC=/home/jlclough/research/Albany/build/src/AlbanyT

echo 
echo "Starting ESP."
echo

# Run ESP: use `-batch` flag to supress GUI
${ESP_EXEC} box.csm -batch

echo 
echo "Finish ESP"
echo
echo "Starting Gmsh"
echo

# Run GMSH: use `-3` to create 3D mesh, `-order 2` to create tet10 instead of tet4
${GMSH_4_2_EXEC} box.geo -3 -order 2

echo 
echo "Finish Gmsh"
echo 
echo "Starting Albany"
echo

${ALBANY_EXEC} albany_gmsh.yaml

echo 
echo "Finish Albany"
echo 
