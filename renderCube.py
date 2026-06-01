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
        pointsRotated.append(rotatePoint(i,[rotRadX,rotRadY,rotRadZ],[cubeX,-cubeY,cubeZ]))
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

    # rotate by y-axis
    rad = math.sqrt((x-rx)**2+(z-rz)**2)
    startAngle = math.atan2((z-rz),(x-rx))
    x = rx + rad*math.cos(startAngle+rotRX)
    z = rz + rad*math.sin(startAngle+rotRX)

    # rotate by z-axis
    rad = math.sqrt((y-ry)**2+(x-rx)**2)
    startAngle = math.atan2((x-rx),(y-ry))
    y = ry + rad*math.cos(startAngle+rotRY)
    x = rx + rad*math.sin(startAngle+rotRY)

    # rotate by x-axis
    rad = math.sqrt((z-rz)**2+(y-ry)**2)
    startAngle = math.atan2((y-ry),(z-rz))
    z = rz + rad*math.cos(startAngle+rotRZ)
    y = ry + rad*math.sin(startAngle+rotRZ)

    return [x,y,z]

def facePoint(points,pointTo,rotPoint):
    x = pointTo[0]
    y = pointTo[1]
    z = pointTo[2]

    rx = rotPoint[0]
    ry = -rotPoint[1]
    rz = rotPoint[2]

    dx = x-rx
    dy = y-ry
    dz = z-rz

    new = []

    if (z == rz):
        rotRY = math.atan2(dx,dy)
        for i in points:
            new.append(rotatePoint(i,[0,rotRY,0],[rx,ry,rz]))
        return new

    else:
        rotRX = math.atan2(dx,dz)
        rotRZ = math.atan2(dy,dz)
        for i in points:
            new.append(rotatePoint(i,[rotRX,0,rotRZ],[rx,ry,rz]))
        return new


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

def getMouse():
    mouseX = root.winfo_pointerx() - root.winfo_rootx() - (width/2)
    mouseY = root.winfo_pointery() - root.winfo_rooty() - (height/2)
    return [mouseX,mouseY]

size = 100
dist = [0,0,500]
rots = [0,0,0]
pointTo = [0,0,0]

def render():
    canvas.delete("all")
    cube3D = getCubePoints(size,dist,rots)
    cube3D = facePoint(cube3D,pointTo,dist)
    cube2D = getDots(cube3D)
    drawCube(cube2D,2,"white")
    canvas.pack()

    mouse = getMouse()
    pointTo[0] = mouse[0]
    pointTo[1] = mouse[1]

    root.after(16,render)

render()

root.mainloop()