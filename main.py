import math
import engine

engine.createEnvironment(750,750,"black",90)

# << to get mouse location relative to tkinter window >>
def getMouse():
    mouseX = engine.root.winfo_pointerx() - engine.root.winfo_rootx() - (engine.width/2)
    mouseY = -(engine.root.winfo_pointery() - engine.root.winfo_rooty() - (engine.height/2))
    return [mouseX,mouseY]

# << to store key presses >>
keys = set()

def keyDown(event):
    keys.add(event.keysym)

def keyUp(event):
    keys.discard(event.keysym)

engine.root.bind("<KeyPress>", keyDown)
engine.root.bind("<KeyRelease>", keyUp)



cube = engine.Cube(200,[250,250,250])
fps = 144

# << Part of Changing Size Example >>
increase = True
currentScale = 1
amount = 1.015
bounds = {"lower":0.7,"upper":1.5}

freecamSpeed = 5

def render():

    # << Changing Size Example >>
    # global increase, currentScale, amount, bounds
    # if increase:
    #     cube.scale([amount,amount,amount],cube.center)
    #     currentScale *= amount
    # else:
    #     cube.scale([1/amount,1/amount,1/amount],cube.center)
    #     currentScale /= amount
    # if currentScale > bounds["upper"] or currentScale < bounds["lower"]:
    #     increase = not increase

    # << Moving to the Right and Back Example >>
    # cube.move([2,0,3])

    # << Cube Rotating Example >>
    # cube.rotate([cube.rotation[0]+2,0,0],cube.center,True)

    # << Mouse Tracker Example >>
    # mouse = getMouse()
    # cube.facePoint([mouse[0],mouse[1],0],cube.center)

    # << Simple Viewer Example >>
    # mouse = getMouse()
    # cube.rotate([mouse[0]/3,0,-mouse[1]/3],cube.center)

    # << Freecam Viewer Example >>
    # mouse = getMouse()
    # cube.rotate([mouse[0]/3,0,-mouse[1]/3],[0,0,-engine.cameraDist])
    # if "w" in keys:
    #     cube.move([0,0,-freecamSpeed])
    # if "s" in keys:
    #     cube.move([0,0,freecamSpeed])
    # if "a" in keys:
    #     cube.move([freecamSpeed,0,0])
    # if "d" in keys:
    #     cube.move([-freecamSpeed,0,0])
    # if "space" in keys:
    #     cube.move([0,-freecamSpeed,0])
    # if "c" in keys:
    #     cube.move([0,freecamSpeed,0])

    # << Dynamic Freecam Viewer Example >>
    mouse = getMouse()
    yaw = mouse[0]/3
    pitch = -mouse[1]/3
    radYaw = math.radians(yaw)
    xTravel = 0
    yTravel = 0
    zTravel = 0
    if "w" in keys:
        xTravel -= freecamSpeed*math.sin(radYaw)
        zTravel -= freecamSpeed*math.cos(radYaw)
    if "s" in keys:
        xTravel += freecamSpeed*math.sin(radYaw)
        zTravel += freecamSpeed*math.cos(radYaw)
    if "a" in keys:
        xTravel += freecamSpeed*math.cos(radYaw)
        zTravel -= freecamSpeed*math.sin(radYaw)
    if "d" in keys:
        xTravel -= freecamSpeed*math.cos(radYaw)
        zTravel += freecamSpeed*math.sin(radYaw)
    if "space" in keys:
        yTravel -= freecamSpeed
    if "c" in keys:
        yTravel += freecamSpeed

    cube.move([xTravel, yTravel, zTravel])
    cube.rotate([yaw,0,pitch],[0,0,-engine.cameraDist])




    engine.canvas.delete("all")
    cube.draw(10,["white","blue","red"])

    engine.root.after(round(1000/fps),render)

render()

engine.root.mainloop()
