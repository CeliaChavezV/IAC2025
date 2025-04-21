import os
import numpy as np
from skimage import io, filters, measure, morphology
import pandas as pd
import matplotlib.pyplot as plt
from tifffile import imread

# ========================================
# CONFIGURACIÓN (AJUSTADA A TUS ARCHIVOS)
# ========================================
scale = 30  # Resolución en micras/píxel (ChemCam RMI)
min_grain_size_px = 20  # Área mínima en píxeles
output_csv = "grain_size_results.csv"

# Patrones específicos para tus archivos
PREFIXES = ('cr0_',)  # Tus archivos empiezan con cr0_
EXTENSIONS = ('.tif', '.tiff', '.TIF', '.TIFF', '.tif')  # Covers all case variations

# ========================================
# FUNCIÓN DE PROCESAMIENTO (igual que antes)
# ========================================
def process_image(image_path):
    try:
        image = imread(image_path)
        if image.dtype == np.uint16:
            image = (image / 256).astype(np.uint8)
        blurred = filters.gaussian(image, sigma=1.5)
        thresh = filters.threshold_otsu(blurred)
        binary = blurred > thresh
        cleaned = morphology.remove_small_objects(binary, min_size=min_grain_size_px)
        cleaned = morphology.remove_small_holes(cleaned, area_threshold=min_grain_size_px)
        labels = measure.label(cleaned)
        regions = measure.regionprops(labels)
        return [2 * np.sqrt(r.area / np.pi) * scale for r in regions]
    except Exception as e:
        print(f"Error procesando {os.path.basename(image_path)}: {str(e)}")
        return []

# ========================================
# BÚSQUEDA Y PROCESAMIENTO (AJUSTADO)
# ========================================
results = []
print("=== INICIO DEL PROCESAMIENTO ===")

for folder in sorted(os.listdir()):
    if folder.startswith('sol') and os.path.isdir(folder):
        print(f"\n📂 Procesando {folder}:")
        
        for file in os.listdir(folder):
            # Condición ajustada a tus archivos cr0_*.tif
            if file.lower().startswith('cr0_') and file.lower().endswith(('.tif', '.tiff')):
                image_path = os.path.join(folder, file)
                print(f"  🔍 Procesando: {file}")
                
                grain_sizes = process_image(image_path)
                for size in grain_sizes:
                    results.append({
                        'Sol': folder,
                        'Image': file,
                        'Grain_Size_um': size,
                        'Equivalent_Diameter_px': size / scale
                    })

# ========================================
# RESULTADOS (igual que antes)
# ========================================
if results:
    df = pd.DataFrame(results)
    print(f"\n✅ {len(df)} granos analizados. Guardando resultados...")
    df.to_csv(output_csv, index=False)
    
    plt.figure(figsize=(10, 6))
    plt.hist(df['Grain_Size_um'], bins=30, color='skyblue', edgecolor='black')
    plt.xlabel('Tamaño de grano (µm)')
    plt.ylabel('Frecuencia')
    plt.title('Distribución de Tamaños de Grano')
    plt.savefig('grain_size_distribution.png', dpi=300)
    plt.show()
else:
    print("\n❌ No se encontraron imágenes. Verifica:")
    print("1. Que las imágenes están en carpetas solXXXXX")
    print("2. Que los nombres empiezan con cr0_ y terminan en .tif/.tiff")
    print("3. Ejecuta este comando para verificar:")
    print("   - Windows: dir sol00010\\cr0_* /b")
    print("   - Linux/Mac: ls sol00010/cr0_*")

print("\n=== PROCESO COMPLETADO ===")