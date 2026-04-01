def calcular_vision_haps():
    print("--- CALCULADORA DE VISIÓN ESTRATOSFÉRICA (HAPS) ---")
    
    # --- VARIABLES DE ENTRADA (Puedes cambiar estos valores) ---
    altura_vuelo_m = 20000        # Altura en metros (H)
    focal_lente_mm = 36         # Distancia focal en mm (f)
    pixel_pitch_um = 12         # Tamaño del píxel en micrones (p) - (Ej: RPi HQ es 1.55)
    res_ancho_px = 640        # Resolución del sensor (Ancho)
    res_alto_px = 512            # Resolución del sensor (Alto)
    
    # Objeto que queremos medir en el suelo (ejemplo: un foco de incendio o un auto)
    objeto_suelo_m =50          # Tamaño del objeto en metros
    
    # --- CÁLCULOS TÉCNICOS ---
    
    # 1. GSD (Ground Sample Distance): metros que representa cada píxel
    # Fórmula: (p * H) / (f * 1000)
    gsd = (pixel_pitch_um * altura_vuelo_m) / (focal_lente_mm * 1000)
    
    # 2. Cobertura total (Footprint): Cuánta tierra entra en una foto
    ancho_total_m = gsd * res_ancho_px
    alto_total_m = gsd * res_alto_px
    
    # 3. Representación del objeto en píxeles
    pixeles_objeto = objeto_suelo_m / gsd
    
    # --- RESULTADOS ---
    print(f"\nRESULTADOS PARA {altura_vuelo_m/1000} KM DE ALTURA:")
    print(f"---------------------------------------------")
    print(f"1. Resolución (GSD): 1 píxel = {gsd:.3f} metros ({gsd*100:.1f} cm)")
    print(f"2. Área de una foto: {ancho_total_m/1000:.2f} km x {alto_total_m/1000:.2f} km")
    print(f"3. DETALLE DEL OBJETO:")
    print(f"   Un objeto de {objeto_suelo_m} metros ocupará:")
    print(f"   >>> {pixeles_objeto:.2f} PÍXELES en tu imagen.")
    print(f"---------------------------------------------")

if __name__ == "__main__":
    calcular_vision_haps()