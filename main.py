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



cube = engine.Cube(200,[0,0,250])
fps = 60

# << Part of Changing Size Example >>
increase = True
currentScale = 1
amount = 1.015
bounds = {"lower":0.7,"upper":1.5}

freecamSpeed = 3

def render():
    engine.canvas.delete("all")
    cube.draw(10,["white","blue","red"])

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
    # cube.rotate([cube.rotation[0]+2,0,0],cube.center)

    # << Mouse Tracker Example >>
    # mouse = getMouse()
    # cube.facePoint([mouse[0],mouse[1],0],cube.center)

    # << Simple Viewer Example >>
    # mouse = getMouse()
    # cube.rotate([mouse[0]/3,0,-mouse[1]/3],cube.center)

    # << Very Simple Freecam Viewer Example >>
    mouse = getMouse()
    cube.rotate([mouse[0]/3,0,-mouse[1]/3],[0,0,-engine.cameraDist])
    if "w" in keys:
        cube.move([0,0,-freecamSpeed])
    if "s" in keys:
        cube.move([0,0,freecamSpeed])
    if "a" in keys:
        cube.move([freecamSpeed,0,0])
    if "d" in keys:
        cube.move([-freecamSpeed,0,0])
    if "space" in keys:
        cube.move([0,-freecamSpeed,0])
    if "c" in keys:
        cube.move([0,freecamSpeed,0])

    engine.root.after(round(1000/fps),render)

render()

engine.root.mainloop()
