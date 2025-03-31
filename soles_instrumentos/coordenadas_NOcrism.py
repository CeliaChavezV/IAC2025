import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================
# CONFIGURACIÓN DE RUTAS
# =============================================
# Obtener la ruta del directorio actual del script
SCRIPT_DIR = Path(__file__).parent.absolute()

# Crear subcarpeta para resultados si no existe
RESULTS_DIR = SCRIPT_DIR / "resultados_NOcrism"
RESULTS_DIR.mkdir(exist_ok=True)

# =============================================
# 1. CARGAR DATOS
# =============================================
# Cargar el archivo CSV desde la misma carpeta
try:
    df = pd.read_csv(SCRIPT_DIR / "localized_interp.csv")
    print("\nArchivo cargado correctamente")
    print("\nPrimeras filas del dataset:")
    print(df.head())
    
    print("\nColumnas disponibles:")
    print(df.columns)
except FileNotFoundError:
    print("\nError: No se encontró el archivo 'localized_interp.csv'")
    exit()

# =============================================
# 2. FUNCIÓN PARA OBTENER COORDENADAS
# =============================================
def obtener_coordenadas(sol=None):
    """
    Obtiene las coordenadas de todos los soles o de un sol específico.
    
    Parámetros:
    - sol: Número de sol (int) o None para obtener todas las coordenadas.
    
    Retorna:
    - DataFrame con latitud planetocéntrica, latitud planetodésica, longitud y elevación.
    """
    columnas_interes = ["sol", "planetocentric_latitude", "planetodetic_latitude", 
                        "longitude", "elevation"]
    
    # Filtrar por el sol si se especifica, o devolver todos los datos
    if sol is not None:
        df_filtrado = df[df["sol"] == sol][columnas_interes]
        print(f"\nDatos para el sol {sol}:")
        print(df_filtrado)
    else:
        df_filtrado = df[columnas_interes]
        print("\nDatos para todos los soles:")
        print(df_filtrado.head())  # Mostrar solo primeras filas para no saturar la consola

    return df_filtrado

# =============================================
# 3. PROCESAMIENTO DE DATOS
# =============================================
# Obtener coordenadas de todos los soles
coordenadas_todos = obtener_coordenadas()

# Obtener coordenadas de soles específicos (ejemplos)
soles_especificos = [125, 500, 1000, 2000, 3000]  # Puedes modificar esta lista
for sol in soles_especificos:
    if sol in df['sol'].values:
        obtener_coordenadas(sol)

# =============================================
# 4. GUARDAR RESULTADOS
# =============================================
# Guardar coordenadas de todos los soles
ruta_todos = RESULTS_DIR / "coordenadas_todos_los_soles.csv"
coordenadas_todos.to_csv(ruta_todos, index=False)
print(f"\nDatos de todos los soles guardados en: {ruta_todos}")

# Guardar coordenadas de soles específicos
for sol in soles_especificos:
    if sol in df['sol'].values:
        coordenadas_sol = obtener_coordenadas(sol)
        ruta_sol = RESULTS_DIR / f"coordenadas_sol_{sol}.csv"
        coordenadas_sol.to_csv(ruta_sol, index=False)
        print(f"Datos del sol {sol} guardados en: {ruta_sol}")

# =============================================
# 5. VISUALIZACIÓN
# =============================================
plt.figure(figsize=(10, 8))
plt.scatter(df["longitude"], df["planetocentric_latitude"], 
            c=df["sol"], cmap='viridis', marker="o", s=10, 
            alpha=0.7, label="Posiciones del Rover")
plt.colorbar(label="Sol (día marciano)")
plt.xlabel("Longitud", fontsize=12)
plt.ylabel("Latitud Planetocéntrica", fontsize=12)
plt.title("Trayectoria del Curiosity en el Gale Crater", fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()

# Guardar el gráfico
ruta_grafico = RESULTS_DIR / "trayectoria_curiosity.png"
plt.savefig(ruta_grafico, dpi=300, bbox_inches='tight')
print(f"\nGráfico de trayectoria guardado en: {ruta_grafico}")
plt.show()