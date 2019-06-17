
// Set the geometry kernel
SetFactory("OpenCASCADE");

// Set the precision
eps = 1e-4;

// Load in the geometries from stp files
copper_box() = ShapeFromFile( "copper_box.stp");
tin_box()    = ShapeFromFile( "tin_box.stp");

BooleanFragments{ Volume{copper_box()}; Delete;}{ Volume{tin_box()}; Delete; }

// Label Surfaces to assign Boundary Conditions in FE problem
x_min_surface() = Surface In BoundingBox{ 0.0-eps, 0.0-eps, 0.0-eps,
                                          0.0+eps, 1.0+eps, 1.0+eps};
x_max_surface() = Surface In BoundingBox{ 2.0-eps, 0.0-eps, 0.0-eps,
                                          2.0+eps, 1.0+eps, 1.0+eps};

Physical Surface( "x_min") = { x_min_surface()};
Physical Surface( "x_max") = { x_max_surface()};

// Label Volume to assign Material Properties in FE problem
Physical Volume( "copper") = { copper_box()};
Physical Volume( "tin")    = { tin_box()};

Mesh.SaveAll=1;
Mesh.Format=1;
