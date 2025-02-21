import pandas as pd

#Cargar el archivo CSV con los datos del Curiosity
df = pd.read_csv("localized_interp.csv")

#Mostrar las primeras filas para entender la estructura
print(df.head())

print(df.columns)#verificar que nombres de columnas coinciden


#Extrae coordenadas
def obtener_coordenadas(sol=None):
    """
    Obtiene las coordenadas de todos los soles o de un sol específico.

    Parámetros:
    - sol: Número de sol (int) o None para obtener todas las coordenadas.

    Retorna:
    - DataFrame con latitud planetocéntrica, latitud planetodésica, longitud y elevación.
    """
    columnas_interes = ["sol", "planetocentric_latitude", "planetodetic_latitude", "longitude", "elevation"]
    
    # Filtrar por el sol si se especifica, o devolver todos los datos
    if sol is not None:
        df_filtrado = df[df["sol"] == sol][columnas_interes]
    else:
        df_filtrado = df[columnas_interes]

    return df_filtrado

#Obtener coordenadas de todos los soles
coordenadas_todos = obtener_coordenadas()
print(coordenadas_todos)

#Obtener coordenadas de un sol específico (ejemplo: sol 125)
coordenadas_sol_125 = obtener_coordenadas(125)
print(coordenadas_sol_125)


#Guardar datos en un csv
coordenadas_todos.to_csv("coordenadas_todos_los_soles.csv", index=False)
coordenadas_sol_125.to_csv("coordenadas_sol_125.csv", index=False)


#Ver mapa trayectoria curiosity
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
plt.scatter(df["longitude"], df["planetocentric_latitude"], marker="o", s=10, label="Posiciones del Rover")
plt.xlabel("Longitud")
plt.ylabel("Latitud Planetocéntrica")
plt.title("Ubicaciones del Curiosity en el Gale Crater")
plt.legend()
plt.show()