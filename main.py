import tkinter as tk
import math

width = 750
height = 750

root = tk.Tk()

canvas = tk.Canvas(root, width=width, height=height, bg="black")

def toRads(degrees):
    radians = []
    for degree in degrees:
        radians.append(degree*(math.pi/180))
    return radians

def toDegs(radians):
    degrees = []
    for radian in radians:
        degrees.append(radian*(180/math.pi))
    return degrees

class Object():

    def __init__(self,points,center,edges):
        self.center = center
        self.points = points
        self.basePoints = points
        self.edges = edges
        self.rotation = [0,0,0]
    
    def rotate(self,rotationDegrees,rotationPoint):
        rotationRadians = toRads(rotationDegrees)

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

        pointsRotated = []
        for point in self.basePoints:
            pointsRotated.append(rotatePoint(point,rotationRadians,rotationPoint))

        # TRACKING ROTATION STATUS
        self.rotation[0] = rotationDegrees[0]
        self.rotation[1] = rotationDegrees[1]
        self.rotation[2] = rotationDegrees[2]

        self.points = pointsRotated
    
    def facePoint(self,pointTo):
        # collect data
        x = pointTo[0]
        y = pointTo[1]
        z = pointTo[2]
        rx = self.center[0]
        ry = self.center[1]
        rz = self.center[2]
        dx = x-rx
        dy = y-ry
        dz = z-rz

        if (z == rz):
            rotRY = math.atan2(dx,dy)
            self.rotate(toDegs([0,rotRY,0]),self.center)

        else:
            rotRX = math.atan2(dx,dz)
            rotRZ = math.atan2(dy,dz)
            self.rotate(toDegs([rotRX,0,rotRZ]),self.center)

    def move(self,distances):
        def movePoint(point,distances):
            x = point[0]+distances[0]
            y = point[1]+distances[1]
            z = point[2]+distances[2]
            return [x,y,z]

        pointsMoved = []
        for point in self.points:
            pointsMoved.append(movePoint(point,distances))
        pointsMovedBase = []
        for point in self.basePoints:
            pointsMovedBase.append(movePoint(point,distances))
        self.points = pointsMoved
        self.basePoints = pointsMovedBase
        self.center = movePoint(self.center,distances)

    
    def draw(self,thickness,colour):
        def getDots():
            centerX = width/2
            centerY = height/2
            dots = []
            for point in self.points:
                x = centerX + point[0]*( centerX/(centerX+point[2]) )
                y = centerY + point[1]*( centerX/(centerX+point[2]) )
                dots.append([x,y])
            return dots
    
        dots = getDots()
        for dot in dots:
            canvas.create_oval(dot[0]-thickness, dot[1]-thickness, dot[0]+thickness, dot[1]+thickness, fill=colour, outline="")
        
        for edge in self.edges:
            canvas.create_line(dots[edge[0]][0], dots[edge[0]][1], dots[edge[1]][0], dots[edge[1]][1], fill=colour, width=thickness)

class Cube(Object):

    def __init__(self,size,center):
        halfSize = size/2
        cubeX = center[0]
        cubeY = center[1]
        cubeZ = center[2]
        points = [[cubeX+halfSize,-cubeY+halfSize,cubeZ-halfSize],
                  [cubeX-halfSize,-cubeY+halfSize,cubeZ-halfSize],
                  [cubeX+halfSize,-cubeY-halfSize,cubeZ-halfSize],
                  [cubeX-halfSize,-cubeY-halfSize,cubeZ-halfSize],
                  [cubeX+halfSize,-cubeY+halfSize,cubeZ+halfSize],
                  [cubeX-halfSize,-cubeY+halfSize,cubeZ+halfSize],
                  [cubeX+halfSize,-cubeY-halfSize,cubeZ+halfSize],
                  [cubeX-halfSize,-cubeY-halfSize,cubeZ+halfSize]]
        edges = [[0,1],[0,2],[3,1],[3,2],
                 [0,4],[1,5],[2,6],[3,7],
                 [4,5],[4,6],[7,5],[7,6]]
        
        super().__init__(points,center,edges)


def getMouse():
    mouseX = root.winfo_pointerx() - root.winfo_rootx() - (width/2)
    mouseY = root.winfo_pointery() - root.winfo_rooty() - (height/2)
    return [mouseX,mouseY]

cube = Cube(200,[0,0,250])
fps = 60

def render():
    canvas.delete("all")
    cube.draw(2,"white")
    canvas.pack()

    # << Cube Moving Backwards Example >>
    # cube.move([0,0,2])

    # << Cube Rotating Example >>
    # cube.rotate([cube.rotation[0]+1,0,0],cube.center)

    # << Mouse Tracker Example >>
    mouse = getMouse()
    cube.facePoint([mouse[0],mouse[1],0])

    root.after(round(1000/fps),render)

render()

root.mainloop()