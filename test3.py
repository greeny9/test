import numpy as np
import magpylib as magpy
from scipy.spatial.transform import Rotation as R

# Create magnet
magnet = magpy.magnet.Cylinder(
    polarization=(1, 0, 0),
    dimension=(6, 2),
    position=(0, 0, 7),
    style_label="Magnet",
    style_color=".7",
)

# Erstelle eine neue Achse, die um 5° geneigt ist (z.B. um die x-Achse)
rotation_angle = 5  # Neigungswinkel in Grad
rotation_axis = 'x'  # Achse, um die rotiert wird (hier: x-Achse)

# Kippung der Rotationsachse um 5°
new_rotation = R.from_euler(rotation_axis, rotation_angle, degrees=True)

# Wenden wir die Kippung auf die Orientierung des Magneten an
magnet.orientation = new_rotation

# Definiere die Winkel für die Magnetbewegung (für symmetrische Rotation)
angles = np.linspace(0, 360, 72)

# Jetzt den Magneten um seine eigene, geneigte Achse rotieren lassen
magnet.rotate_from_angax(angles, new_rotation.apply([0, 0, 1]), None, "auto", degrees=True)

# Show scene
magpy.show(magnet, animation=True, backend="plotly")
