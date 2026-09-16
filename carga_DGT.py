import pandas as pd
from pathlib import Path

# ---------------------------------------------------------
# 1. CONFIGURACIÓN
# ---------------------------------------------------------

# Carpeta donde están los Excel
carpeta1 = Path(r"C:\Users\U000000\Desktop\varios\ThePower\PROYECTO_FINAL\datos\datos_generales")
carpeta2 = Path(r"C:\Users\U000000\Desktop\varios\ThePower\PROYECTO_FINAL\datos\datos_sanciones")
carpeta3 = Path(r"C:\Users\U000000\Desktop\varios\ThePower\PROYECTO_FINAL\datos\datos_siniestralidad")
carpeta = Path(r"C:\Users\U000000\Desktop\varios\ThePower\PROYECTO_FINAL\datos")


# Años que queremos procesar
anios = range(2014, 2025) # Coge los años de 2014 a 2024, no coge 2025.


# ---------------------------------------------------------
# 2. LOCALIZAR LOS FICHEROS
# ---------------------------------------------------------

ficheros1 = {}
ficheros2 = {}
ficheros3 = {}

for anio in anios:
    # Ejemplo esperado: DatosMunicipalesGeneral_2014.xlsx
    fichero1 = carpeta1 / f"DatosMunicipalesGeneral_{anio}.xlsx"
    fichero2 = carpeta2 / f"DatosMunicipalesSancionesPuntos_{anio}.xlsx"
    fichero3 = carpeta3 / f"DatosMunicipalesSiniestralidad_{anio}.xlsx"

    if not fichero1.exists():
        print(f"No encontrado: {fichero1.name}")
    else:
        ficheros1[anio] = fichero1
        
    if not fichero2.exists():
            print(f"No encontrado: {fichero2.name}")
    else:
        ficheros2[anio] = fichero2
        
    if not fichero3.exists():
            print(f"No encontrado: {fichero3.name}")
    else:
        ficheros3[anio] = fichero3

print(f"\nSe han encontrado {len(ficheros1)} de {len(list(anios))} ficheros de datos generales.")
print(f"\nSe han encontrado {len(ficheros2)} de {len(list(anios))} ficheros de datos de sanciones.")
print(f"\nSe han encontrado {len(ficheros3)} de {len(list(anios))} ficheros de datos de siniestralidad.")


# ---------------------------------------------------------
# 3. COMPROBAR QUE TODOS TIENEN LAS MISMAS COLUMNAS (DETENER EL PROCESO SI HAY PROBLEMAS)
# ---------------------------------------------------------

ficheros = {
    "generales": ficheros1,
    "sanciones": ficheros2,
    "siniestros": ficheros3
}

for tipo, ficheros_tipo in ficheros.items():

    columnas_referencia = None
    problemas = []

    print(f"\n{'=' * 60}")
    print(f"COMPROBANDO: {tipo.upper()}")
    print(f"{'=' * 60}")

    for anio, fichero in ficheros_tipo.items():

        df = pd.read_excel(fichero, nrows=0)
        columnas = list(df.columns)

        if columnas_referencia is None:

            columnas_referencia = columnas

            print(f"\nColumnas de referencia ({anio}):")
            print(columnas)

        elif columnas != columnas_referencia:

            problemas.append(anio)

            print(f"\nLas columnas del año {anio} NO coinciden.")

            faltan = [
                c for c in columnas_referencia
                if c not in columnas
            ]

            sobran = [
                c for c in columnas
                if c not in columnas_referencia
            ]

            if faltan:
                print("   Faltan:", faltan)

            if sobran:
                print("   Sobran:", sobran)

            if len(columnas) == len(columnas_referencia):
                for posicion, (c1, c2) in enumerate(
                    zip(columnas_referencia, columnas)
                ):
                    if c1 != c2:
                        print(
                            f"   Posición {posicion}: "
                            f"esperada '{c1}', encontrada '{c2}'"
                        )

    if problemas:
        print(f"\nPROBLEMAS EN {tipo.upper()}")
        print("Años con columnas diferentes:", problemas)

    else:
        print(
            f"\nTodos los ficheros de {tipo} tienen las mismas columnas."
        )





# -----------------------------------------------------
# 4. LEER LOS FICHEROS Y AÑADIR LA COLUMNA AÑO
# -----------------------------------------------------

        
dataframes_finales = {}

for tipo, ficheros_tipo in ficheros.items():

    dataframes = []

    print(f"\n{'=' * 60}")
    print(f"PROCESANDO: {tipo.upper()}")
    print(f"{'=' * 60}")

    for anio, fichero in ficheros_tipo.items():

        print(f"Leyendo {fichero.name}...")

        df = pd.read_excel(fichero)

        # Añadir Año como primera columna
        df.insert(0, "Año", anio)

        dataframes.append(df)


    # -----------------------------------------------------
    # 5. UNIFICAR POR FILAS
    # # -----------------------------------------------------

        # seguimos dentro del for
        
        df_final = pd.concat(
            dataframes,
            axis=0,
            ignore_index=True
        )

    # -----------------------------------------------------
    # 6. GUARDAR EL RESULTADO
    # -----------------------------------------------------
        
        # Nombre del Excel de salida según el tipo
        fichero_salida = carpeta / f"{tipo}_2014_2024.xlsx"

        # Guardamos el DataFrame final asociado a su tipo
        dataframes_finales[tipo] = df_final

    print(f"\n{tipo.upper()} unificado correctamente.")
    print(f"Filas totales: {len(df_final):,}")
    print(f"Columnas totales: {len(df_final.columns)}")

    df_final.to_excel(
        fichero_salida,
        index=False
    )

    print("\nProceso terminado correctamente.")
    print(f"Fichero creado: {fichero_salida}")
    print(f"Filas totales: {len(df_final):,}")
    print(f"Columnas totales: {len(df_final.columns)}")
    
    

# -----------------------------------------------------
# 7. LEER LOS TRES FICHEROS CREADOS
# -----------------------------------------------------

fichero_generales = carpeta / "generales_2014_2024.xlsx"
fichero_sanciones = carpeta / "sanciones_2014_2024.xlsx"
fichero_siniestros = carpeta / "siniestros_2014_2024.xlsx"

fichero_salida = carpeta / "data_complete_DGT_2014_2024.xlsx"

print("Leyendo ficheros...")

df_generales = pd.read_excel(fichero_generales)
df_sanciones = pd.read_excel(fichero_sanciones)
df_siniestros = pd.read_excel(fichero_siniestros)


# -----------------------------------------------------
# 8. COMPROBAR LAS CLAVES
# -----------------------------------------------------

claves = ["Año", "Código INE"]

for nombre, df in [
    ("Generales", df_generales),
    ("Sanciones", df_sanciones),
    ("Siniestros", df_siniestros)
]:

    faltan = [col for col in claves if col not in df.columns]

    if faltan:
        raise ValueError(
            f"En {nombre} faltan las columnas: {faltan}"
        )




# -----------------------------------------------------
# 9. COMPARAR CÓDIGOS INE (año 2024)
# -----------------------------------------------------

df1 = pd.read_excel(fichero_generales)
df2 = pd.read_excel(fichero_sanciones)
df3 = pd.read_excel(fichero_siniestros)

df1_2024 = df1[df1["Año"] == 2024]
df2_2024 = df2[df2["Año"] == 2024]
df3_2024 = df3[df3["Año"] == 2024]

codigos1 = set(df1_2024["Código INE"].dropna())
codigos2 = set(df2_2024["Código INE"].dropna())
codigos3 = set(df3_2024["Código INE"].dropna())


# Códigos que están en fichero 1 pero NO en fichero 2 NI en fichero 3
solo_fichero1 = codigos1 - codigos2 - codigos3
# Códigos que están en fichero 2 pero NO en fichero 1
solo_fichero2 = codigos2 - codigos1
# Códigos que están en fichero 3 pero NO en fichero 1
solo_fichero3 = codigos3 - codigos1


print(
    f"\nCódigos únicos fichero 1: {len(codigos1):,}"
)
print("Códigos que están en fichero 1 pero NO en fichero 2 NI fichero 3:")
print(len(solo_fichero1))
print(sorted(solo_fichero1))


print(
    f"\nCódigos únicos fichero 2: {len(codigos2):,}"
)
print("Códigos que están en fichero 2 pero no en fichero 1:")
print(len(solo_fichero2))
print(sorted(solo_fichero2))

print(
    f"\nCódigos únicos fichero 3: {len(codigos3):,}"
)
print("Códigos que están en fichero 3 pero no en fichero 1:")
print(len(solo_fichero3))
print(sorted(solo_fichero3))



# -----------------------------------------------------
# 10. UNIR SANCIONES y SINIESTROS A GENERALES
# -----------------------------------------------------

for nombre, df in [
    ("Generales", df_generales),
    ("Sanciones", df_sanciones),
    ("Siniestros", df_siniestros)
]:

    duplicados = df.duplicated(
        subset=["Año", "Código INE"],
        keep=False
    )

    print(
        f"{nombre}: "
        f"{duplicados.sum():,} filas duplicadas por clave"
    )
    
    
df_final = df_generales.merge(
    df_sanciones,
    on=claves,
    how="left",
    suffixes=("", "_sanciones")
)


df_final = df_final.merge(
    df_siniestros,
    on=claves,
    how="left",
    suffixes=("", "_siniestros")
)


# -----------------------------------------------------
# 11. GUARDAR
# -----------------------------------------------------

df_final.to_excel(
    fichero_salida,
    index=False
)


print("\nFichero final creado correctamente.")
print(f"Fichero: {fichero_salida}")
print(f"Filas: {len(df_final):,}")
print(f"Columnas: {len(df_final.columns)}")