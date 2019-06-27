# GRASP: Guided Rib And Spar Placement

_GRASP_ automatically creates frame layouts for user specified
wing Outer Mold Lines (OMLs) base on material properties
and expected aircraft weight.

## Dependencies
_GRASP_ immediately requires the follow software packages to be installed
and available:
 - [ESP](https://acdl.mit.edu/ESP/) for the geometric modeler.
 - [Gmsh](http://gmsh.info) for the geometric manager and mesher.
 - [Albany](https://github.com/SNLComputation/Albany) for the Finite Element solve.
 - [meshio](https://github.com/nschloe/meshio) to read the results files.
 
Once the above are installed, adjust the `aux/setup.sh` file to point
to the executables. Also install the `*.udc` files into ESP's
`udc/` directory.

