# Barebones 3D Graphics Rendering Demonstration
Renders a 3D object from scratch using just native python. I made it my mission to do this by formulating all the math myself as a personal project. As such, there may be formula inefficiencies, but what I've made here myself works.

## How It Works
- Uses trigonometry to render 3d objects from scratch in a simple python-native script with `tkinter`. Understanding it is a good way to get a grasp on how 3d graphics work under the hood, at a very basic level.
- Only cubes have been integrated as a preset object via the `Cube` class, which you can use to conviniently create cubes, since crafting models otherwise requires plotting each individual point and face yourself (very tedious).
- Points, edges, and faces (“items”) are simply rendered via averaging the (x,y,z) of involved points for the estimated center point of each item, and then drawing in order of painter's algorithm (farthest to closest). As such, be aware of possible rendering limitations that may arise.
- The camera is defaulted to 90 degrees of FOV. Objects will experience some degree of FOV warping from the camera (more fov = more distortion), this is normal.

## Setup
1. Clone the repository.
2. Set up the `render()` function as desired.
3. Run python `main.py`.

![Tracking Cube Render](assets/demoCubeRender.gif)