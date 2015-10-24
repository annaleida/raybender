#!/usr/bin/env python
 
import vtk
from refraction import *

def RenderRay(start, end, rayNumber):
	print '* * * RenderRay: ', rayNumber
	print 'ray coords start: ', start
	print 'ray coords end: ', end
	p_rays.InsertNextPoint(start)
	p_rays.InsertNextPoint(end)
	ray = vtk.vtkLine()
	ray.GetPointIds().SetId(0,(rayNumber -1)*2)
	ray.GetPointIds().SetId(1,(rayNumber-1)*2+1)
	rays.InsertNextCell(ray)

def RenderTriangleAsPolygon(points, triangleNumber):
	print '* * * RenderTriangle: ', triangleNumber
	print 'Triangle points: ', tri
	p_triangles.InsertNextPoint(points[0])
	p_triangles.InsertNextPoint(points[1])
	p_triangles.InsertNextPoint(points[2])
	triangle = vtk.vtkTriangle();
	triangle.GetPointIds().SetId(0, 0+(triangleNumber-1)*3);
	triangle.GetPointIds().SetId(1, 1+(triangleNumber-1)*3);
	triangle.GetPointIds().SetId(2, 2+(triangleNumber-1)*3);
	triangles.InsertNextCell(triangle);

def RenderTriangleAsLine(points, triangleNumber):
	print '* * * RenderTriangle: ', triangleNumber
	print 'Triangle points: ', tri
	print (triangleNumber-1)*3
	p_triangles.InsertNextPoint(points[0])
	p_triangles.InsertNextPoint(points[1])
	p_triangles.InsertNextPoint(points[2])
	
	line1 = vtk.vtkLine();
	line1.GetPointIds().SetId(0, 0+(triangleNumber-1)*3);
	line1.GetPointIds().SetId(1, 1+(triangleNumber-1)*3);
	line2 = vtk.vtkLine();
	line2.GetPointIds().SetId(0, 0+(triangleNumber-1)*3);
	line2.GetPointIds().SetId(1, 2+(triangleNumber-1)*3);
	line3 = vtk.vtkLine();
	line3.GetPointIds().SetId(0, 1+(triangleNumber-1)*3);
	line3.GetPointIds().SetId(1, 2+(triangleNumber-1)*3);
	triangles.InsertNextCell(line1);
	triangles.InsertNextCell(line2);
	triangles.InsertNextCell(line3);



p_coordinates = vtk.vtkPoints()
p_rays = vtk.vtkPoints()
p_triangles = vtk.vtkPoints()
points = vtk.vtkPoints()
coordinateSystem = vtk.vtkCellArray()
rays = vtk.vtkCellArray()
triangles  = vtk.vtkCellArray()

nbrOfTriangles = 3
space = float(1) ## space between triangles/size
nbrOfRays = nbrOfTriangles + 1
tolerance = 0.001;

# for i in range(nbrOfTriangles):
	
print '\n***Original ray'
#Original ray
start = [0.1,0.1,1.0]
direction = [0.0,0.2,-1.0*space]
end = [0.0,0.0,0.0] #Will be rewritten
for i in range(len(start)):
			end[i] = start[i] + direction[i]

rendered1 = 0
for i in range(nbrOfTriangles):

	print '***Triangle'
	c = float(-i)
	p0 = [0.01, 0.0, 1.0*c]
	p1 = [0.02, 1.0, 1.0*c]
	p2 = [1.0, 0.0, 1.0*c]
	tri = [p0,p1,p2]
	RenderTriangleAsLine(tri, i+1)

	ray = [start, end]
	n0 = 1.5 #Hittepa for now
	n1 = 1.0

	ret = ComputeIntersection(tri, ray, tolerance)
	if ret != 0:
		end = ret[:] #Stop rendering at intersection
		RenderRay(start, end, i+1)

		newRay = ComputeRefraction(n0,n1, array(p1), array(p2), (array(end)-array(start)), array(ret))
		#New ray
		if ret != 0:
			start = ret[:] #Rewrite new ray beginning at last end
			for j in range(len(start)):
				# direction[j] = direction[j]+0.25*(i+1) #bogus
				end[j] = start[j] + 5.0*newRay[j]*space
			
		if i == nbrOfTriangles -1: #Last line
			RenderRay(start, end, i+2)	
	elif rendered1 == 0: #Only one ray
		RenderRay(start, end, i+1)
		rendered1 = 1


# p_rays.InsertNextPoint([2.0,2.0,2.0])
# p_rays.InsertNextPoint([4.0,4.0,4.0])
# ray = vtk.vtkLine()
# ray.GetPointIds().SetId(0,0+i*2)
# ray.GetPointIds().SetId(1,1+i*2)
# rays.InsertNextCell(ray)

#Coordinate system
# print '\n***Coordinate system'
origo = [0.0,0.0,0.0]
ex = [1.0,0.0,0.0]
ey = [0.0,1.0,0.0]
ez = [0.0,0.0,-1.0]
coordSystemLength = 1.0*space*nbrOfTriangles
for i in range(3):
	ex[i] = coordSystemLength*ex[i]
	ey[i] = coordSystemLength*ey[i]
	ez[i] = coordSystemLength*ez[i]
p_coordinates.InsertNextPoint(origo)
p_coordinates.InsertNextPoint(ex)
p_coordinates.InsertNextPoint(ey)
p_coordinates.InsertNextPoint(ez)
linex = vtk.vtkLine()
linex.GetPointIds().SetId(0,0) # the second 0 is the index of the Origin in the vtkPoints
linex.GetPointIds().SetId(1,1) # the second 1 is the index of P0 in the vtkPoints
liney = vtk.vtkLine()
liney.GetPointIds().SetId(0,0)
liney.GetPointIds().SetId(1,2)
linez = vtk.vtkLine()
linez.GetPointIds().SetId(0,0)
linez.GetPointIds().SetId(1,3)
coordinateSystem.InsertNextCell(linex)
coordinateSystem.InsertNextCell(liney)
coordinateSystem.InsertNextCell(linez)

# Create a polydata
# print '\n***Create polydata'
coordinatesPolyData = vtk.vtkPolyData()
coordinatesPolyData.SetPoints(p_coordinates)
coordinatesPolyData.SetLines(coordinateSystem)
raysPolyData = vtk.vtkPolyData()
raysPolyData.SetPoints(p_rays)
raysPolyData.SetLines(rays)
trianglesPolyData = vtk.vtkPolyData()
trianglesPolyData.SetPoints(p_triangles)
trianglesPolyData.SetLines(triangles)



#Coloring
# print '\n***Coloring'
red = [255, 0, 0]
green = [0, 255, 0]
blue = [0,0,255]
white = [255,255,255]
yellow = [255,255,0]
turqois = [0,255,255]
colors_coord = vtk.vtkUnsignedCharArray()
colors_triangles = vtk.vtkUnsignedCharArray()
colors_rays = vtk.vtkUnsignedCharArray()
colors_triangles.SetNumberOfComponents(3)
colors_coord.SetNumberOfComponents(3)
colors_rays.SetNumberOfComponents(3)
# colors.SetName("Colors")
for i in range(3):
	colors_coord.InsertNextTupleValue(red)
for i in range(nbrOfTriangles*3):
	colors_triangles.InsertNextTupleValue(white)
for i in range(nbrOfRays):
	color_index = mod(i,5)
	if color_index == 0:
		colors_rays.InsertNextTupleValue(blue)
	elif color_index == 1:
		colors_rays.InsertNextTupleValue(green)
	elif color_index == 2:
		colors_rays.InsertNextTupleValue(yellow)
	elif color_index == 3:
		colors_rays.InsertNextTupleValue(white)
	elif color_index == 4:
		colors_rays.InsertNextTupleValue(turqois)
# colors.InsertNextTupleValue(green)
# colors.InsertNextTupleValue(blue)
# colors.InsertNextTupleValue(blue)
raysPolyData.GetCellData().SetScalars(colors_rays)
coordinatesPolyData.GetCellData().SetScalars(colors_coord)
trianglesPolyData.GetCellData().SetScalars(colors_triangles)

# Visualize
# print '\n***Visualize'
mapper_rays = vtk.vtkPolyDataMapper()
mapper_triangles = vtk.vtkPolyDataMapper()
mapper_coord = vtk.vtkPolyDataMapper()
if vtk.VTK_MAJOR_VERSION <= 5:
    mapper_rays.SetInput(raysPolyData)
    mapper_triangles.SetInput(trianglesPolyData)
    mapper_coord.SetInput(coordinatesPolyData)
else:
    print 'VTK_MAJOR_VERSION too high'
actor_triangles= vtk.vtkActor()
actor_rays = vtk.vtkActor()
actor_coord = vtk.vtkActor()
actor_coord.SetMapper(mapper_coord)
actor_rays.SetMapper(mapper_rays)
actor_triangles.SetMapper(mapper_triangles)
renderer = vtk.vtkRenderer()
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderer.AddActor(actor_rays)
renderer.AddActor(actor_triangles)
renderer.AddActor(actor_coord)
renderWindow.Render()
renderWindowInteractor.Start()

 
