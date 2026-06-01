# Barebones 3D Graphics Rendering Demonstration
Renders a 3D object from scratch using just native python.

## How It Works
- Use trigonometry to render 3d objects from scratch in a simple python-native script with `tkinter`. Understanding it is a good way to get a grasp on how advanced visual renders work under the hood, at a very primitive level.
- Only basic wireframe cubes have been integrated as a conventient creation funtion `getCubePoints()`. You can change their size, rotation, location, colour, etc.
- You can make objects face points via the `facePoint()` function. By default, it is set to track your mouse cursor.
- The camera is at 90 degrees of FOV. Objects will experience some degree of FOV warping from the camera, this is normal.

## Setup
1. Clone the repository.
2. Set up the `render` function as desired.
3. Run python `main.py`.