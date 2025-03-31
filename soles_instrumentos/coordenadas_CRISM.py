import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================
# CONFIGURACIÓN DE RUTAS
# =============================================
# Obtener la ruta del directorio actual (donde está este script)
SCRIPT_DIR = Path(__file__).parent.absolute()

# Crear subcarpeta para resultados si no existe
RESULTS_DIR = SCRIPT_DIR / "resultados_CRISM"
RESULTS_DIR.mkdir(exist_ok=True)

# =============================================
# 1. CARGAR Y PROCESAR DATOS
# =============================================
# Cargar el archivo CSV con los datos del Curiosity (desde la misma carpeta)
df = pd.read_csv(SCRIPT_DIR / "localized_interp.csv")

# Mostrar las primeras filas para entender la estructura
print("Primeras filas del dataset:")
print(df.head())

# Verificar nombres de columnas
print("\nColumnas disponibles:")
print(df.columns)

# Convertir la longitud a formato de 0° a 360° (si es necesario)
df["longitude_crism"] = df["longitude"].apply(lambda x: x + 360 if x < 0 else x)

# Mantener la latitud planetocéntrica igual
df["latitude_crism"] = df["planetocentric_latitude"]

# Mostrar las primeras filas para verificar los cambios
print("\nCoordenadas convertidas:")
print(df[["sol", "latitude_crism", "longitude_crism"]].head())

# =============================================
# 2. GUARDAR COORDENADAS COMPLETAS
# =============================================
# Obtener todas las coordenadas para cada sol
df_all_sols = df[["sol", "latitude_crism", "longitude_crism", "elevation"]]

# Guardar en la carpeta de resultados
output_all = RESULTS_DIR / "coordenadas_crism_todos_soles.csv"
df_all_sols.to_csv(output_all, index=False)
print(f"\nArchivo con todos los soles guardado en: {output_all}")

# =============================================
# 3. FILTRAR POR SOLES DE INTERÉS
# =============================================
# Rangos de interés definidos por instrumentos/regiones
rangos_soles = {
    "Bradbury_Rise": (0, 55),
    "Rocknest": (55, 100),
    "Yellowknife_Bay": (125, 300),
    "Kimberley": (580, 630),
    "Pahrump_Hills": (750, 950),
    "Murray_Buttes": (1400, 1500),
    "Vera_Rubin_Ridge": (1800, 2300),
    "Glen_Torridon": (2300, 2800),
    "Greenheugh_Pediment": (2800, 3100)
}

# Procesar cada rango
for region, (sol_inicio, sol_fin) in rangos_soles.items():
    # Filtrar los datos
    soles_interes = df[(df['sol'] >= sol_inicio) & (df['sol'] <= sol_fin)]
    
    if not soles_interes.empty:
        # Crear nombre de archivo
        nombre_archivo = f"coordenadas_{region}_sol_{sol_inicio}_a_{sol_fin}.csv"
        ruta_archivo = RESULTS_DIR / nombre_archivo
        
        # Guardar el archivo
        soles_interes[['sol', 'planetocentric_latitude', 'longitude', 'elevation']].to_csv(ruta_archivo, index=False)
        print(f"{region} (soles {sol_inicio}-{sol_fin}) guardado en: {ruta_archivo}")

# =============================================
# 4. VISUALIZACIÓN
# =============================================
plt.figure(figsize=(10, 8))
plt.scatter(df["longitude"], df["planetocentric_latitude"], 
            c=df["sol"], cmap='viridis', marker="o", s=10, 
            label="Posiciones del Rover")
plt.colorbar(label="Sol (día marciano)")
plt.xlabel("Longitud")
plt.ylabel("Latitud Planetocéntrica")
plt.title("Trayectoria del Curiosity en el Gale Crater")

# Guardar el gráfico en la carpeta de resultados
plot_path = RESULTS_DIR / "trayectoria_curiosity.png"
plt.savefig(plot_path, dpi=300)
print(f"\nGráfico de trayectoria guardado en: {plot_path}")
plt.show()