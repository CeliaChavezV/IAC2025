import pandas as pd

# Cargar el archivo CSV con los datos del Curiosity
df = pd.read_csv("localized_interp.csv")

# Mostrar las primeras filas para entender la estructura
print(df.head())

print(df.columns)#verificar que nombres de columnas coinciden

# Convertir la longitud a formato de 0° a 360° (si es necesario)
df["longitude_crism"] = df["longitude"].apply(lambda x: x + 360 if x < 0 else x)

# Mantener la latitud planetocéntrica igual
df["latitude_crism"] = df["planetocentric_latitude"]

# Mostrar las primeras filas para verificar los cambios
print(df[["sol", "latitude_crism", "longitude_crism"]].head())

# Obtener todas las coordenadas para cada sol
df_all_sols = df[["sol", "latitude_crism", "longitude_crism", "elevation"]]

# Guardar el archivo con las coordenadas convertidas
df_all_sols.to_csv("coordenadas_crism_todos_soles.csv", index=False)

# Mostrar las primeras filas
print(df_all_sols.head())


######################################################################################################

# Filtrar por un sol específico, por ejemplo, Sol 100

'''
sol_especifico = 125
df_sol_especifico = df[df["sol"] == sol_especifico][["sol", "latitude_crism", "longitude_crism", "elevation"]]


# Mostrar las coordenadas del sol específico
print(df_sol_especifico)

# Guardar las coordenadas de soles específicos
df_sol_especifico.to_csv(f"coordenadas_crism_sol_{sol_especifico}.csv", index=False)
'''

######################################################################################################

#Filtrar por soles de interes
# Seleccionar los soles de interés (ChemCam, MastCam, APXS, CheMin, CRISM)
#Bradbury Rise (Sol 0 - 55 aprox.)
#Rocknest (Sol 55 - 100 aprox.)
#Yellowknife Bay (Sol 125 - 300 aprox.)
#Kimberley (Sol 580 - 630 aprox.)
#Pahrump Hills (Sol 750 - 950 aprox.)
#Murray Buttes (Sol 1400 - 1500 aprox.)
#Vera Rubin Ridge (Sol 1800 - 2300 aprox.)
#Glen Torridon (Sol 2300 - 2800 aprox.)
#Greenheugh Pediment (Sol 2800 - 3100 aprox.)

# Definir el rango de soles de interés
sol_inicio = 2800
sol_fin = 3100

# Filtrar los datos dentro del rango de soles seleccionado
soles_interes = df[(df['sol'] >= sol_inicio) & (df['sol'] <= sol_fin)]

# Crear un nombre de archivo dinámico basado en el rango de soles
nombre_archivo = f"soles_{sol_inicio}_a_{sol_fin}.csv"

# Guardar el archivo CSV con el nombre generado
soles_interes[['sol', 'planetocentric_latitude', 'longitude', 'elevation']].to_csv(nombre_archivo, index=False)

print(f"Archivo CSV guardado como '{nombre_archivo}'")

######################################################################################################

import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
plt.scatter(df["longitude"], df["planetocentric_latitude"], marker="o", s=10, label="Posiciones del Rover")
plt.xlabel("Longitud")
plt.ylabel("Latitud Planetocéntrica")
plt.title("Ubicaciones del Curiosity en el Gale Crater")
plt.legend()
plt.show()
