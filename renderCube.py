import tkinter as tk
import math

width = 750
height = 750

root = tk.Tk()

canvas = tk.Canvas(root, width=width, height=height, bg="black")


def getCubePoints(halfCubeDim,coords,rotsDeg):
    cubeX = coords[0]
    cubeY = coords[1]
    cubeZ = coords[2]
    rotRadX = rotsDeg[0] * (math.pi/180)
    rotRadY = rotsDeg[1] * (math.pi/180)
    rotRadZ = rotsDeg[2] * (math.pi/180)
    pointsUnrotated = [[cubeX+halfCubeDim,-cubeY+halfCubeDim,cubeZ-halfCubeDim],
              [cubeX-halfCubeDim,-cubeY+halfCubeDim,cubeZ-halfCubeDim],
              [cubeX+halfCubeDim,-cubeY-halfCubeDim,cubeZ-halfCubeDim],
              [cubeX-halfCubeDim,-cubeY-halfCubeDim,cubeZ-halfCubeDim],
              [cubeX+halfCubeDim,-cubeY+halfCubeDim,cubeZ+halfCubeDim],
              [cubeX-halfCubeDim,-cubeY+halfCubeDim,cubeZ+halfCubeDim],
              [cubeX+halfCubeDim,-cubeY-halfCubeDim,cubeZ+halfCubeDim],
              [cubeX-halfCubeDim,-cubeY-halfCubeDim,cubeZ+halfCubeDim]]
    pointsRotated = []
    for i in pointsUnrotated:
        pointsRotated.append(rotatePoint(i,[rotRadX,rotRadY,rotRadZ],[cubeX,cubeY,cubeZ]))
    return pointsRotated

def rotatePoint(point,rots,rotPoint):

    # collect data
    x = point[0]
    y = point[1]
    z = point[2]

    rx = rotPoint[0]
    ry = rotPoint[1]
    rz = rotPoint[2]

    rotRX = rots[0]
    rotRY = rots[1]
    rotRZ = rots[2]

    # rotate by x-axis
    if z-rz == 0:
        origRX = math.atan((x-rx)/(z-rz+(10**-20)))
    else:
        origRX = math.atan((x-rx)/(z-rz))

    x = x*(math.sin(origRX-rotRX)/math.sin(origRX))
    z = z*(math.cos(origRX-rotRX)/math.cos(origRX))

    # rotate by y-axis
    if x-rx == 0:
        origRY = math.atan((y-ry)/(x-rx+(10**-20)))
    else:
        origRY = math.atan((y-ry)/(x-rx))

    y = y*(math.sin(origRY-rotRY)/math.sin(origRY))
    x = x*(math.cos(origRY-rotRY)/math.cos(origRY))

    # # # rotate by z-axis
    if y-ry == 0:
        origRZ = math.atan((z-rz)/(y-ry+(10**-20)))
    else:
        origRZ = math.atan((z-rz)/(y-ry))

    z = z*(math.sin(origRZ-rotRZ)/math.sin(origRZ))
    y = y*(math.cos(origRZ-rotRZ)/math.cos(origRZ))

    return [x,y,z]

def getDots(points):
    centerX = width/2
    centerY = height/2
    out = []
    for point in points:
        x = centerX + point[0]*( centerX/(centerX+point[2]) )
        y = centerY + point[1]*( centerX/(centerX+point[2]) )
        out.append([x,y])
    return out


def drawDots(dots,radius,colour):
    for dot in dots:
        canvas.create_oval(dot[0]-radius, dot[1]-radius, dot[0]+radius, dot[1]+radius, fill=colour, outline="")

def drawCube(cube,thickness,colour):
    x = 0
    y = 1

    # FRONT SIDE
    froLefTop = 3
    froRigTop = 2
    froLefBot = 1
    froRigBot = 0
    canvas.create_line(cube[froRigTop][x], cube[froRigTop][y], cube[froRigBot][x], cube[froRigBot][y], fill=colour, width=thickness)
    canvas.create_line(cube[froLefTop][x], cube[froLefTop][y], cube[froLefBot][x], cube[froLefBot][y], fill=colour, width=thickness)
    canvas.create_line(cube[froLefTop][x], cube[froLefTop][y], cube[froRigTop][x], cube[froRigTop][y], fill=colour, width=thickness)
    canvas.create_line(cube[froLefBot][x], cube[froLefBot][y], cube[froRigBot][x], cube[froRigBot][y], fill=colour, width=thickness)

    # REAR SIDE
    reaLefTop = 7
    reaRigTop = 6
    reaLefBot = 5
    reaRigBot = 4
    canvas.create_line(cube[reaRigTop][x], cube[reaRigTop][y], cube[reaRigBot][x], cube[reaRigBot][y], fill=colour, width=thickness)
    canvas.create_line(cube[reaLefTop][x], cube[reaLefTop][y], cube[reaLefBot][x], cube[reaLefBot][y], fill=colour, width=thickness)
    canvas.create_line(cube[reaLefTop][x], cube[reaLefTop][y], cube[reaRigTop][x], cube[reaRigTop][y], fill=colour, width=thickness)
    canvas.create_line(cube[reaLefBot][x], cube[reaLefBot][y], cube[reaRigBot][x], cube[reaRigBot][y], fill=colour, width=thickness)

    # MIDDLE CONNECTIONS
    canvas.create_line(cube[froLefTop][x], cube[froLefTop][y], cube[reaLefTop][x], cube[reaLefTop][y], fill=colour, width=thickness)
    canvas.create_line(cube[froRigTop][x], cube[froRigTop][y], cube[reaRigTop][x], cube[reaRigTop][y], fill=colour, width=thickness)
    canvas.create_line(cube[froLefBot][x], cube[froLefBot][y], cube[reaLefBot][x], cube[reaLefBot][y], fill=colour, width=thickness)
    canvas.create_line(cube[froRigBot][x], cube[froRigBot][y], cube[reaRigBot][x], cube[reaRigBot][y], fill=colour, width=thickness)

    drawDots(cube,thickness,colour)



size = 100
dist = [0,0,0]
rots = [0,0,0]

# cube3D = getCubePoints(100,[0,0,50],[0,0,0])
# cube2D = getDots(cube3D)
# drawCube(cube2D,2,"white")
# canvas.pack()

def render():
    canvas.delete("all")
    cube3D = getCubePoints(size,dist,rots)
    cube2D = getDots(cube3D)
    drawCube(cube2D,2,"white")
    canvas.pack()

    rots[0] += 1

    root.after(8,render)

render()

root.mainloop()