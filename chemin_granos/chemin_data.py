##obtenido de https://pds-geosciences.wustl.edu/msl/msl-m-chemin-4-rdr-v1/mslcmn_1xxx/data/rdr4/

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import os

# =============================================
# 0. CONFIGURACIÓN DE RUTAS
# =============================================
# Obtener la ruta del directorio actual (donde está este script)
SCRIPT_DIR = Path(__file__).parent.absolute()

# Crear subcarpeta para resultados si no existe
RESULTS_DIR = SCRIPT_DIR / "resultados_chemin"
RESULTS_DIR.mkdir(exist_ok=True)

# =============================================
# 1. CARGAR DATOS DESDE ARCHIVO CSV
# =============================================
def cargar_datos_chemin(archivo_csv):
    """Carga datos de difracción desde un CSV."""
    try:
        # Buscar el archivo en la misma carpeta del script
        ruta_archivo = SCRIPT_DIR / archivo_csv
        datos = pd.read_csv(ruta_archivo)
        if '2-THETA' not in datos.columns or 'INTENSITY' not in datos.columns:
            raise ValueError("El CSV debe contener columnas '2-THETA' e 'INTENSITY'")
        return datos
    except Exception as e:
        print(f"Error al cargar {archivo_csv}: {e}")
        return None

# =============================================
# 2. ANALIZAR PICOS (ECUACIÓN DE SCHERRER)
# =============================================
def analizar_picos(datos):
    """Identifica picos de difracción y calcula tamaño de grano."""
    theta = datos['2-THETA'].values
    intensidad = datos['INTENSITY'].values
    
    # Detección de picos
    picos, props = find_peaks(intensidad, prominence=500, width=3)
    anchos_picos = props['widths'] * (theta[1] - theta[0])  # Convertir a grados 2θ
    
    # Calcular tamaño de grano (Scherrer: Kλ/(βcosθ))
    K = 0.9  # Factor de forma
    lambda_co = 1.79026  # Longitud de onda Co Kα (Å)
    tamanos_grano = []
    
    for i, p in enumerate(picos):
        theta_rad = np.radians(theta[p] / 2)  # θ (no 2θ)
        fwhm_rad = anchos_picos[i] * (np.pi / 180)  # FWHM en radianes
        if fwhm_rad > 0:
            tamanos_grano.append(K * lambda_co / (fwhm_rad * np.cos(theta_rad)))
    
    return {
        'posiciones_picos': theta[picos],
        'intensidades_picos': intensidad[picos],
        'anchos_picos': anchos_picos,
        'tamanos_grano': np.array(tamanos_grano) if tamanos_grano else np.array([0]),
        'indices_picos': picos
    }

# =============================================
# 3. FUNCIÓN PARA PROCESAR TODOS LOS ARCHIVOS
# =============================================
def procesar_todos_archivos():
    """Procesa todos los archivos y devuelve DataFrame con resultados."""
    # Lista de archivos con sus soles y regiones
    archivos = [
        {'nombre': 'cma_404470826rda00790050104ch11503p1.csv', 'sol': 79, 'region': 'Rocknest'},
        {'nombre': 'cma_405889312rda00950050104ch11504p1.csv', 'sol': 95, 'region': 'Rocknest'},
        {'nombre': 'cma_405890913re100950050104ch11504p1.csv', 'sol': 95, 'region': 'Rocknest'},
        {'nombre': 'cma_408288091rda01220050926ch11520p1.csv', 'sol': 122, 'region': 'Yellowknife Bay'},
        {'nombre': 'cma_408289557re101220050926ch11520p1.csv', 'sol': 122, 'region': 'Yellowknife Bay'},
        {'nombre': 'cma_410683388rda01490051902ch11521p1.csv', 'sol': 149, 'region': 'Yellowknife Bay'},
        {'nombre': 'cma_410684855re101490051902ch11521p1.csv', 'sol': 149, 'region': 'Yellowknife Bay'},
        {'nombre': 'cma_414856883rda01960060000ch12240p1.csv', 'sol': 196, 'region': 'Murray Buttes'},
        {'nombre': 'cma_414856883rda01960060000ch12240p2.csv', 'sol': 196, 'region': 'Murray Buttes'},
        {'nombre': 'cma_414857616re101960060000ch12240p1.csv', 'sol': 196, 'region': 'Murray Buttes'},
        {'nombre': 'cma_595174954rda22270730550ch00111p1.csv', 'sol': 2227, 'region': 'Glen Torridon'},
        {'nombre': 'cma_595175339re122270730550ch00111p1.csv', 'sol': 2227, 'region': 'Glen Torridon'},
        {'nombre': 'cma_598547494rda22650731206ch00111p1.csv', 'sol': 2265, 'region': 'Glen Torridon'},
        {'nombre': 'cma_598547865re122650731206ch00111p1.csv', 'sol': 2265, 'region': 'Glen Torridon'},
        {'nombre': 'cma_599656708rda22770731206ch00113p1.csv', 'sol': 2277, 'region': 'Glen Torridon'},
        {'nombre': 'cma_599657079re122770731206ch00113p1.csv', 'sol': 2277, 'region': 'Glen Torridon'},
        {'nombre': 'cma_602259727re123070732502ch00113p1.csv', 'sol': 2307, 'region': 'Greenheugh Pediment'}
    ]
    
    resultados_totales = []
    
    for archivo in archivos:
        print(f"\nProcesando {archivo['nombre']} (Sol {archivo['sol']}, {archivo['region']})...")
        
        # Cargar datos
        datos = cargar_datos_chemin(archivo['nombre'])
        if datos is None:
            continue
        
        # Analizar picos
        resultados = analizar_picos(datos)
        
        if len(resultados['tamanos_grano']) > 0:
            tamano_promedio = np.mean(resultados['tamanos_grano'])
            print(f"Tamaño de grano promedio: {tamano_promedio:.1f} Å")
            
            resultados_totales.append({
                'Archivo': archivo['nombre'],
                'Sol': archivo['sol'],
                'Region': archivo['region'],
                'Num_Picos': len(resultados['posiciones_picos']),
                'Tamano_Grano_Promedio_A': tamano_promedio,
                'Tamano_Grano_Min_A': np.min(resultados['tamanos_grano']),
                'Tamano_Grano_Max_A': np.max(resultados['tamanos_grano'])
            })
        else:
            print("No se encontraron picos válidos para calcular tamaño de grano")
    
    # Crear DataFrame con todos los resultados
    df_resultados = pd.DataFrame(resultados_totales)
    return df_resultados

# =============================================
# 4. VISUALIZACIÓN DE RESULTADOS
# =============================================
def graficar_resultados(df_resultados):
    """Genera gráficos de los resultados por región."""
    plt.figure(figsize=(12, 6))
    
    # Gráfico por región
    for region in df_resultados['Region'].unique():
        subset = df_resultados[df_resultados['Region'] == region]
        plt.scatter(
            subset['Sol'],
            subset['Tamano_Grano_Promedio_A'],
            label=region,
            s=100
        )
    
    plt.title("Tamaño de grano promedio por Sol y Región")
    plt.xlabel("Sol (día marciano)")
    plt.ylabel("Tamaño de grano promedio (Å)")
    plt.legend()
    plt.grid(True)
    
    # Guardar el gráfico en la carpeta de resultados
    plot_path = RESULTS_DIR / "tamanos_grano_por_region.png"
    plt.savefig(plot_path)
    print(f"\nGráfico guardado en: {plot_path}")
    plt.show()

# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================
if __name__ == "__main__":
    # Procesar todos los archivos
    df_resultados = procesar_todos_archivos()
    
    # Mostrar tabla de resultados
    print("\nRESULTADOS FINALES:")
    print(df_resultados.to_string(index=False))
    
    # Guardar resultados en CSV dentro de la carpeta de resultados
    output_csv = RESULTS_DIR / "resultados_tamanos_grano.csv"
    df_resultados.to_csv(output_csv, index=False)
    print(f"\nResultados guardados en: {output_csv}")
    
    # Generar gráficos
    graficar_resultados(df_resultados)