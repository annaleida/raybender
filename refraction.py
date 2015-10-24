import vtk
from pylab import *

def ComputeRefraction(n0, n1, p1_pointInPlane, p2_pointInPlane, rayVector, pointOfIntersection):
	print '* * *ComputeRefraction'
	print 'OBS: Take care of norm = 0'
	print 'OBS: Take care of reflection'
	print 'rayVector: ', rayVector
	rayVector = rayVector/norm(rayVector)
	print 'rayVector: ', rayVector
	planeVector1 = p1_pointInPlane - pointOfIntersection
	print 'planeVector1: ', planeVector1
	planeVector2 = p2_pointInPlane - pointOfIntersection
	print 'planeVector2: ', planeVector2
	normal = cross(planeVector1, planeVector2)
	print 'normal: ', normal
	normal = normal/norm(normal)
	print 'normal: ', normal
	flip = cross(rayVector, normal)
	sin_teta0 = norm(flip)
	flip = flip/norm(flip)
	print 'flip: ', flip
	projection = cross(normal, flip)
	projection = projection/norm(projection)
	print 'projection: ', projection
	transformation = array([projection, normal, flip])
	print 'transformation: ', transformation
	print 'sin_teta0: ', sin_teta0
	sin_teta1 = (n0/n1)*sin_teta0
	print 'sin_teta1: ', sin_teta1
	teta1 = arcsin(sin_teta1)
	print 'teta1: ', teta1
	teta0 = arcsin(sin_teta0)
	print 'teta0: ', teta0
	teta = teta0-teta1 #Negative sign for rotation toward normal
	print 'teta: ', teta
	rot_pnf = array([[cos(teta), -sin(teta), 0.0], 
		[sin(teta), cos(teta), 0.0],
		[0.0,0.0,1.0]])
	print 'rot_pnf: ', rot_pnf
	A_pnf = dot(transformation, rayVector)
	print 'A_pnf: ', A_pnf
	B_pnf = dot(rot_pnf, A_pnf)
	print 'B_pnf: ', B_pnf
	transformation_inverse = inv(transformation)
	print 'transformation_inverse: ', transformation_inverse
	new_RayVector = dot(transformation_inverse, B_pnf)
	print 'new_RayVector: ', new_RayVector
	return new_RayVector

	
def ComputeIntersection(triangle, line, tolerance):
	print '* * *ComputeIntersection'
	# print tri
	# print line

	# Create a square in the x-y plane.
	points = vtk.vtkPoints()
	points.InsertNextPoint(triangle[0])
	points.InsertNextPoint(triangle[1])
	# points.InsertNextPoint(1.0, 1.0, 0.0)
	points.InsertNextPoint(triangle[2])

	# Create the polygon
	polygon = vtk.vtkPolygon()
	polygon.GetPoints().DeepCopy(points)
	polygon.GetPointIds().SetNumberOfIds(3)
	for i in range(3):
    		polygon.GetPointIds().SetId(i, i)

	# Outputs
	t = vtk.mutable(0) # Parametric coordinate of intersection (0 (corresponding to p1) to 1 (corresponding to p2))
	x = [0.0, 0.0, 0.0]
	pcoords = [0.0, 0.0, 0.0]
	subId = vtk.mutable(0)
	iD = polygon.IntersectWithLine(line[0], line[1], tolerance, t, x, pcoords, subId);
 
	
	if iD == 1:
		print "intersection: ", x
		return x
	else:
		print "No intersection"
		return 0
