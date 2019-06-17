SetFactory("OpenCASCADE");

esp_box() = ShapeFromFile( "box.stp");

// Phys Surface 5 is back of cube
// Phys Surface 6 is front of cube
Physical Surface("back") = {5};
Physical Surface("front") = {6};

Physical Volume("esp_box") = { esp_box()};

Mesh.SaveAll=1;
// Mesh.Format=16;
