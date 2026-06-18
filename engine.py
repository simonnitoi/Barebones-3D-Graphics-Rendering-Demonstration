import tkinter as tk
import math

from operator import itemgetter

root = tk.Tk()

width = 0
height = 0
degreesFOV = 0
cameraDist = 0

canvas = tk.Canvas(root)

def createEnvironment(wid,hgt,bg,fov):
    global width,height,degreesFOV,cameraDist,canvas,root
    width = wid
    height = hgt
    degreesFOV = fov
    cameraDist = (width/2)/math.tan(math.radians(degreesFOV)/2) # calculating how many units behind (0,0,0) the camera is -> camera located at (0,0,-cameraDist)
    canvas = tk.Canvas(root, width=width, height=height, bg=bg)
    canvas.pack()

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

    def __init__(self,points,center,faces):
        self.center = center
        self.points = points
        self.basePoints = points
        self.faces = faces
        self.rotation = [0,0,0]

        def getEdges(faces):
            edges = []

            for face in faces:
                for i in range(len(face)):
                    edge = sorted([face[i], face[(i + 1) % len(face)]])
                    
                    if edge not in edges:
                        edges.append(edge)
                
            return edges
        
        self.edges = getEdges(faces)
    
    def rotate(self,rotationDegrees,rotationPoint,trueRotation=False):
        if trueRotation:
            rotationRadians = toRads([rotationDegrees[0]-self.rotation[0],rotationDegrees[1]-self.rotation[1],rotationDegrees[2]-self.rotation[2]])
        else:
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

        if trueRotation:
            self.basePoints = pointsRotated
            self.center = rotatePoint(self.center,rotationRadians,rotationPoint)
    
    def facePoint(self,pointTo,rotPoint):
        # collect data
        x = pointTo[0]
        y = pointTo[1]
        z = pointTo[2]
        rx = rotPoint[0]
        ry = rotPoint[1]
        rz = rotPoint[2]
        dx = x-rx
        dy = y-ry
        dz = z-rz

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
    
    def scale(self,scales,scalePoint):
        xScale = scales[0]
        xPoint = scalePoint[0]
        yScale = scales[1]
        yPoint = scalePoint[1]
        zScale = scales[2]
        zPoint = scalePoint[2]

        newPoints = []
        for point in self.points:
            xNew = xPoint+(point[0]-xPoint)*xScale
            yNew = yPoint+(point[1]-yPoint)*yScale
            zNew = zPoint+(point[2]-zPoint)*zScale
            newPoints.append([xNew,yNew,zNew])
        
        newBasePoints = []
        for point in self.basePoints:
            xNew = xPoint+(point[0]-xPoint)*xScale
            yNew = yPoint+(point[1]-yPoint)*yScale
            zNew = zPoint+(point[2]-zPoint)*zScale
            newBasePoints.append([xNew,yNew,zNew])
        
        self.points = newPoints
        self.basePoints = newBasePoints

    
    def draw(self,thickness,colour):

        # << Converting points to 2D plane for tkinter >>
        def getDots():
            centerX = width/2
            centerY = height/2
            dots = []
            for point in self.points:
                x = centerX + point[0]*( cameraDist/(cameraDist+point[2]) )
                y = centerY - point[1]*( cameraDist/(cameraDist+point[2]) )
                dots.append([x,y])
            return dots
    
        dots = getDots()

        # << Getting distances
        def getCenter(points):
            xSum = 0
            xLen = 0
            ySum = 0
            yLen = 0
            zSum = 0
            zLen = 0
            for point in points:
                xSum += point[0]
                ySum += point[1]
                zSum += point[2]

                xLen+=1
                yLen+=1
                zLen+=1
    
            return [xSum/xLen,ySum/yLen,zSum/zLen]

        def getDist(points):

            coords = []

            for point in points:
                coords.append([self.points[point][0],self.points[point][1],self.points[point][2]+cameraDist]) # add the distance of the camera to the Z

            xyz = getCenter(coords)

            x = xyz[0]
            y = xyz[1]
            z = xyz[2]
            return math.sqrt(x**2+y**2+z**2)

        def isVisible(pointIndices):
            for index in pointIndices:
                if (cameraDist + self.points[index][2]) <= 0.1:
                    return False
            return True

        # << Sorting for painter's algorithm >>
        items = []

        for point in range(len(self.points)):
            if isVisible([point]):
                items.append({"type":"point","coords":point,"distance":getDist([point])})
        
        for edge in self.edges:
            if isVisible(edge):
                items.append({"type":"edge","coords":edge,"distance":getDist(edge)})
        
        for face in self.faces:
            if isVisible(face):
                items.append({"type":"face","coords":face,"distance":getDist(face)})

        items.sort(key=itemgetter("distance"),reverse=True)

        def getEdgeDynamic(dots,origEdge,thickness):
            dist1 = getDist([origEdge[0]])
            dist2 = getDist([origEdge[1]])
            thickness1 = thickness*(cameraDist/(cameraDist+dist1))
            thickness2 = thickness*(cameraDist/(cameraDist+dist2))
            center1 = [dots[origEdge[0]][0],dots[origEdge[0]][1]]
            center2 = [dots[origEdge[1]][0],dots[origEdge[1]][1]]
            angle = math.pi/2-math.atan2(abs(center1[1]-center2[1]),abs(center1[0]-center2[0]))
            x1 = (thickness1/2)*math.cos(angle)
            y1 = (thickness1/2)*math.sin(angle)
            dot1_1 = [center1[0]+x1,center1[1]+y1]
            dot1_2 = [center1[0]-x1,center1[1]-y1]
            x2 = (thickness2/2)*math.cos(angle)
            y2 = (thickness2/2)*math.sin(angle)
            dot2_1 = [center2[0]+x2,center2[1]+y2]
            dot2_2 = [center2[0]-x2,center2[1]-y2]
            return [dot1_1,dot1_2,dot2_2,dot2_1]

        for item in items:
            if item["type"] == "face":
                face = item["coords"]
                canvas.create_polygon(dots[face[0]][0], dots[face[0]][1], 
                                      dots[face[1]][0], dots[face[1]][1], 
                                      dots[face[2]][0], dots[face[2]][1], 
                                      dots[face[3]][0], dots[face[3]][1], 
                                      fill=colour[0], width=0, outline="")
            elif item["type"] == "edge":
                origEdge = item["coords"]
                edge = getEdgeDynamic(dots,origEdge,thickness)
                canvas.create_polygon(edge[0][0], edge[0][1], 
                                      edge[1][0], edge[1][1], 
                                      edge[2][0], edge[2][1], 
                                      edge[3][0], edge[3][1], 
                                      fill=colour[1], width=0, outline="")
            else:
                dot = dots[item["coords"]]
                rad = thickness*(cameraDist/(cameraDist+item["distance"]))
                canvas.create_oval(dot[0]-rad, dot[1]-rad, 
                                   dot[0]+rad, dot[1]+rad, 
                                   fill=colour[2], outline="")

class Cube(Object):

    def __init__(self,size,location):
        halfSize = size/2
        cubeX = location[0]
        cubeY = location[1]
        cubeZ = location[2]
        points = [[cubeX+halfSize,cubeY-halfSize,cubeZ-halfSize],
                  [cubeX-halfSize,cubeY-halfSize,cubeZ-halfSize],
                  [cubeX+halfSize,cubeY+halfSize,cubeZ-halfSize],
                  [cubeX-halfSize,cubeY+halfSize,cubeZ-halfSize],
                  [cubeX+halfSize,cubeY-halfSize,cubeZ+halfSize],
                  [cubeX-halfSize,cubeY-halfSize,cubeZ+halfSize],
                  [cubeX+halfSize,cubeY+halfSize,cubeZ+halfSize],
                  [cubeX-halfSize,cubeY+halfSize,cubeZ+halfSize]]
        
        # << POINT MAPPING >>
        #             Left,Right
        # front top =    3,2
        # front bottom = 1,0
        # back top =     7,6
        # back bottom =  5,4
        #           TOP       FRONT    BOTTOM    BACK      RIGHT      LEFT
        faces = [[3,2,6,7],[0,1,3,2],[0,1,5,4],[6,7,5,4],[2,0,4,6],[3,1,5,7]]
        
        super().__init__(points,location,faces)