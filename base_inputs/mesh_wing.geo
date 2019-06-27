// First load the wing OML, ribs, and spars
SetFactory("OpenCASCADE");
eps = 1e-2;

// Add in each component one at a time, start with the first spar,
// then ribs as they will all intersect the first spar,
// then the spars as they will all intersect the ribs
union() = ShapeFromFile( "spars/spars_1.stp");

GRASP_FRAG_UNION_RIBS

GRASP_FRAG_UNION_SPARS


// Get Wing Bottom Surfaces
wing_bottom_surfaces() = Surface In BoundingBox{  0.0-eps, 0.0-eps,  -10.0-eps,
                                                 10.0+eps, 8.0+eps,    0.0+eps};

// Print out the surfaces that form the bottom of the wing
// Store as physical surface
N = #wing_bottom_surfaces();
If (N < 1)
  Printf("Failed to find lowest surface!");
  Exit;
EndIf

For i In {0:N-1}
  Printf("wing_bottom_surface[%g] tag = %g", i, wing_bottom_surfaces[i]);
EndFor
Physical Surface("wing_underside") = { wing_bottom_surfaces() };

GRASP_WING_ROOT_SURFACES

// Define Mesh Parameters
Mesh.CharacteristicLengthMax = 0.05;
Mesh.SaveAll = 1;
