import numpy as np
import magpylib as magpy
import pandas as pd  # Importieren der Pandas-Bibliothek

# Create magnet
magnet = magpy.magnet.Cylinder(
    polarization=(1, 0, 0),
    dimension=(6, 2),
    position=(0, 0, 1.5),
    style_label="Magnet",
    style_color=".7",
)

# Create shaft dummy with 3D model
shaft = magpy.misc.CustomSource(
    position=(0, 0, 7),
    style_color=".7",
    style_model3d_showdefault=False,
    style_label="Shaft",
)
shaft_trace = magpy.graphics.model3d.make_Prism(
    base=20,
    diameter=1,
    height=1,
    opacity=0.3,
)
shaft.style.model3d.add_trace(shaft_trace)

# Shaft rotation / magnet wobble motion
displacement = 1
num_measurements = 72  # Anzahl der Messpunkte
angles = np.linspace(0, 360, num_measurements)  # Rotationswinkel des Magneten über 72 Messpunkte
coll = magnet + shaft
magnet.move((displacement, 0, 0))
coll.rotate_from_angax(angles, "z", anchor=0, start=0)

# Create sensor
gap = .03
sens = magpy.Sensor(
    position=(0, 0, -gap),
    pixel=[(1, 0, 0), (-1, 0, 0)],
    style_pixel_size=0.5,
    style_size=1.5,
)

# Get the magnetic field components (Bx, By, Bz) from the sensor
df = sens.getB(magnet, output="dataframe")

# Berechnung des Rotationswinkels (angle)
# Formel: angle = (360° / Anzahl der Messpunkte) * path
df["angle (deg)"] = (360 / num_measurements) * df["path"]  # Berechnet den Winkel basierend auf dem path

# Berechnung von Bxy (Bxy = sqrt(Bx^2 + By^2))
df["Bxy"] = np.sqrt(df["Bx"]**2 + df["By"]**2)

# Berechnung des Winkels (theta) aus Bx und By (in Grad)
df["theta (deg)"] = np.degrees(np.arctan2(df["By"], df["Bx"]))  # Umrechnung von rad in grad

# DataFrame aufteilen: ungerade Werte in df1, gerade Werte in df2
#df1 = df[df["path"] % 2 != 0]  # Ungerade Pfade (path)
#df2 = df[df["path"] % 2 == 0]  # Gerade Pfade (path)

# Suffix "_B" zu den Spalten von df2 hinzufügen
#df1 = df1.add_suffix('_A')  # Fügt "_B" zu allen Spalten von df1 hinzu
#df2 = df2.add_suffix('_B')  # Fügt "_B" zu allen Spalten von df2 hinzu

# DataFrames zusammenführen: Spalten aus df1 und df2 zusammenfügen
#df_combined = pd.concat([df1.reset_index(drop=True), df2.reset_index(drop=True)], axis=1)

df_filtered = df[["angle (deg)", "Bx", "By", "Bz", "Bxy", "theta (deg)"]]

# Excel-Datei speichern
output_filename = "magnetic_field_values_combined.xlsx"
#df.to_excel(output_filename, index=False)
df_filtered.to_excel(output_filename, index=False)
#df_combined.to_excel(output_filename, index=False)

print(f"Die Magnetfeldwerte wurden erfolgreich in '{output_filename}' gespeichert.")
