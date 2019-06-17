import meshio

exo = meshio.read("results.exo")

for data_name in exo.point_data:
    if data_name == "solution_x":
        print("have solution_x")
        print exo.point_data[ data_name]
        print len(exo.point_data[ data_name])

sol_x = exo.point_data[ "solution_x"]
for i in range( len( sol_x)):
    msg = "sol_x[" + repr(i) + "] = " 
    msg+= repr( sol_x[i])
    print( msg)

points = exo.points
count = 0
for point in points:    
    msg = "point[" + repr( count) + "] is: " + repr( point)
    print( msg)
    count += 1

x_min = 0
first_time = True
for point in points:
    x_coord = point[0]
    if x_coord < x_min or first_time:
        x_min = x_coord
        first_time = False

msg = "x_min = " + repr( x_min)
print( msg)
