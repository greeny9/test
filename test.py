import numpy as np
import magpylib as magpy
import pandas as pd  # Importieren der Pandas-Bibliothek

##Variablen/Konstanten
versatz_x=0.15

# Create magnet
magnet = magpy.magnet.Cylinder(
    polarization=(-1, 0, 0),
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
num_measurements = 61  # Anzahl der Messpunkte
angles = np.linspace(0, 360, num_measurements)  # Rotationswinkel des Magneten über x Messpunkte
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

############################################
####        Magnetsimulation            ####
############################################

# Get the magnetic field components (Bx, By, Bz) from the sensor
df = sens.getB(magnet, output="dataframe")

# Berechnung von Bxy (Bxy = sqrt(Bx^2 + By^2))
df["Bxy"] = np.sqrt(df["Bx"]**2 + df["By"]**2)

# Berechnung des Winkels (theta) aus Bx und By (in Grad)
df["theta (deg)"] = np.degrees(np.arctan2(df["By"], df["Bx"])) % 360  # Winkel in Grad von 0° bis 360°


############################################
####    Transformation Dataframes       ####
############################################

# Berechnung des Soll-Winkels auf basis der Messpunkte
df["angle (deg)"] = (df["path"]/(num_measurements-1)) * 360  # Berechnet den Winkel basierend auf dem path

# DataFrame aufteilen: Pixel 0 in df1, Pixel 1 in df2
df1 = df[df["pixel"] == 0]  # Daten für Pixel 0
df2 = df[df["pixel"] == 1]  # Daten für Pixel 1

# Suffixe hinzufügen
df1 = df1.add_suffix(' A')  # Fügt "_B" zu allen Spalten von df1 hinzu
df2 = df2.add_suffix(' B')  # Fügt "_B" zu allen Spalten von df2 hinzu


# DataFrames anhand der "angle (deg)"-Spalte zusammenführen
df_filtered = pd.merge(
    df1[["angle (deg) A", "Bx A", "By A", "Bz A", "Bxy A", "theta (deg) A"]],
    df2[["angle (deg) B", "Bx B", "By B", "Bz B", "Bxy B", "theta (deg) B"]],
    left_on="angle (deg) A",  # Gemeinsame Spalte für den Merge
    right_on="angle (deg) B",
    how="inner"  # Nur gemeinsame Werte behalten
)
# Entfernen des Spalte _B da diese sonst doppelt ist
df_filtered.drop(columns=["angle (deg) B"], inplace=True)



############################################
####     PARAMETER im Frame ergänzen    ####
############################################

df_filtered["Versatz X"] = versatz_x



############################################
####            Datenausgabe            ####
############################################

# Nach bedarf die Grafik anzeigen, ACHTUNG: WIRD ERSTELLT FÜR JEDE SCHLEIFE
magpy.show(sens, magnet, animation=True, backend="plotly")

# Excel-Datei speichern
output_filename = "magnetic_field_values_combined1.xlsx"
#df.to_excel(output_filename, index=False)
df_filtered.to_excel(output_filename, index=False)
#df_combined.to_excel(output_filename, index=False)

#magpy.show(sens, magnet, shaft, animation=True, backend="plotly")

print(f"Die Magnetfeldwerte wurden erfolgreich in '{output_filename}' gespeichert.")
