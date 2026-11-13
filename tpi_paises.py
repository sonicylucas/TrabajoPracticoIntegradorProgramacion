import csv
import os

RUTA_CSV = os.path.join(os.path.dirname(__file__), "datos", "paises.csv")


# ==============================================================================
# 1. Gestion De Archivos y Datos (Persistencias y Validacion)

def cargar_datos_csv(ruta_archivo):
    """
    Lee el archivo CSV y retorna una lista de diccionarios con los paises.
    Si el archivo no existe, lo crea automaticamente con la estructura base.
    """
    paises = []
    
    # Si el archivo no existe, crea la carpeta y un CSV base con los encabezados
    if not os.path.exists(ruta_archivo):
        print(f" El archivo {ruta_archivo} no se encontro. Creando un archivo base...")
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        try:
            with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['nombre', 'poblacion', 'superficie', 'continente'])
            print("Archivo 'paises.csv' creado exitosamente con la estructura base.")
        except Exception as e:
            print(f"Error al intentar crear el archivo CSV: {e}")
        return paises

    try:
        with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for num_linea, fila in enumerate(lector, start=2):
                try:
                    nombre = fila['nombre'].strip()
                    poblacion = int(fila['poblacion'].strip())
                    superficie = int(fila['superficie'].strip())
                    continente = fila['continente'].strip()

                    if not nombre or not continente or poblacion < 0 or superficie < 0:
                        print(f" Omision por datos invalidos en la linea {num_linea}.")
                        continue

                    paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente
                    })
                except (ValueError, KeyError):
                    print(f" Error de formato en la linea {num_linea}. Se omitira el registro.")
        print(f" Se cargaron {len(paises)} paises correctamente.")
    except Exception as e:
        print(f" Error critico al leer el archivo: {e}")

    return paises


def guardar_datos_csv(ruta_archivo, paises):
    """
    Guarda la lista actual de paises en el archivo CSV especificado.
    """
    try:
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
        with open(ruta_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            campos = ['nombre', 'poblacion', 'superficie', 'continente']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
        print(" Cambios guardados en el archivo CSV exitosamente.")
    except Exception as e:
        print(f" Error al guardar los datos en el CSV: {e}")


# ==============================================================================
# 2. Funcionalidades Operativas (Altas, Modificaciones y Busquedas)

def es_texto_valido(texto):
    """
    Verifica que la cadena no esté vacia ni sea unicamente numérica.
    """
    texto_limpio = texto.replace(" ", "")
    if not texto_limpio or texto_limpio.isdigit():
        return False
    return True


def agregar_pais(paises):
    """
    Agrega un nuevo pais solicitando sus datos por consola,
    validando que no se ingresen respuestas numéricas ni campos vacios.
    """
    print("\n--- AGREGAR NUEVO PAiS ---")
    
    # Validacion del nombre
    nombre = input("Ingrese el nombre del pais: ").strip()
    while not es_texto_valido(nombre):
        nombre = input(" El nombre no puede ser un numero ni estar vacio. Reingrese el nombre: ").strip()

    # Verificar existencia para evitar duplicados
    for p in paises:
        if p['nombre'].lower() == nombre.lower():
            print(f" Error: El pais '{nombre}' ya esta registrado.")
            return

    poblacion = leer_entero_positivo("Ingrese la poblacion: ")
    superficie = leer_entero_positivo("Ingrese la superficie en km²: ")

    # Validacion del continente
    continente = input("Ingrese el continente: ").strip()
    while not es_texto_valido(continente):
        continente = input(" El continente no puede ser un numero ni estar vacio. Reingrese el continente: ").strip()

    nuevo_pais = {
        "nombre": nombre.capitalize(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente.capitalize()
    }
    
    paises.append(nuevo_pais)
    guardar_datos_csv(RUTA_CSV, paises)
    print(f" Pais '{nuevo_pais['nombre']}' agregado con éxito.")


def actualizar_pais(paises):
    """
    Modifica unicamente los datos de Poblacion y Superficie de un pais existente.
    """
    print("\n--- ACTUALIZAR PAiS ---")
    if not paises:
        print(" No hay paises registrados.")
        return

    nombre_buscar = input("Ingrese el nombre del pais a actualizar: ").strip().lower()
    pais_encontrado = None

    for p in paises:
        if p['nombre'].lower() == nombre_buscar:
            pais_encontrado = p
            break

    if not pais_encontrado:
        print(f" No se encontro el pais '{nombre_buscar}'.")
        return

    print(f"Modificando datos de: {pais_encontrado['nombre']}")
    print(f"Poblacion actual: {pais_encontrado['poblacion']} | Superficie actual: {pais_encontrado['superficie']} km²")

    nueva_poblacion = leer_entero_positivo("Ingrese la nueva poblacion: ")
    nueva_superficie = leer_entero_positivo("Ingrese la nueva superficie en km²: ")

    pais_encontrado['poblacion'] = nueva_poblacion
    pais_encontrado['superficie'] = nueva_superficie

    guardar_datos_csv(RUTA_CSV, paises)
    print(f" Datos de '{pais_encontrado['nombre']}' actualizados correctamente.")


def buscar_pais(paises):
    """
    Busca paises por coincidencia exacta o parcial de su nombre.
    """
    print("\n--- Buscar pais ---")
    if not paises:
        print(" No hay paises registrados.")
        return

    termino = input("Ingrese el nombre (o fragmento) a buscar: ").strip().lower()
    if not termino:
        print(" El término de busqueda no puede estar vacio.")
        return

    resultados = [p for p in paises if termino in p['nombre'].lower()]
    mostrar_listado_paises(resultados, f"Resultados de la busqueda para '{termino}'")


# ==============================================================================
# 3. Filtros Y Ordenamiento

def filtrar_paises(paises):
    """
    Submenu de filtrado por continente, rango de poblacion o rango de superficie.
    """
    print("\n--- Filtrar Paises ---")
    print("1. Filtrar por Continente")
    print("2. Filtrar por Rango de Poblacion")
    print("3. Filtrar por Rango de Superficie")
    opcion = input("Seleccione una opcion de filtro (1-3): ").strip()

    if opcion == "1":
        cont = input("Ingrese el continente a buscar: ").strip().lower()
        filtrados = [p for p in paises if p['continente'].lower() == cont]
        mostrar_listado_paises(filtrados, f"Paises del continente '{cont.capitalize()}'")
    elif opcion == "2":
        min_pob = leer_entero_positivo("Poblacion minima: ")
        max_pob = leer_entero_positivo("Poblacion maxima: ")
        if min_pob > max_pob:
            print(" El rango minimo no puede ser mayor que el maximo.")
            return
        filtrados = [p for p in paises if min_pob <= p['poblacion'] <= max_pob]
        mostrar_listado_paises(filtrados, f"Paises con poblacion entre {min_pob} y {max_pob}")
    elif opcion == "3":
        min_sup = leer_entero_positivo("Superficie minima (km²): ")
        max_sup = leer_entero_positivo("Superficie maxima (km²): ")
        if min_sup > max_sup:
            print(" El rango minimo no puede ser mayor que el maximo.")
            return
        filtrados = [p for p in paises if min_sup <= p['superficie'] <= max_sup]
        mostrar_listado_paises(filtrados, f"Paises con superficie entre {min_sup} km² y {max_sup} km²")
    else:
        print(" Opcion de filtro no valida.")


def ordenar_paises(paises):
    """
    Submenu de ordenamiento de paises por Nombre, Poblacion o Superficie.
    """
    print("\n--- Ordenar Paises ---")
    print("1. Ordenar por Nombre")
    print("2. Ordenar por Poblacion")
    print("3. Ordenar por Superficie")
    opcion = input("Seleccione criterio (1-3): ").strip()

    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in criterios:
        print(" Criterio no valido.")
        return

    criterio = criterios[opcion]
    sentido = input("¿Desea orden Ascendente (A) o Descendente (D)?: ").strip().upper()
    reverso = True if sentido == 'D' else False

    paises_ordenados = sorted(paises, key=lambda x: x[criterio], reverse=reverso)
    mostrar_listado_paises(paises_ordenados, f"Paises ordenados por {criterio} ({'Descendente' if reverso else 'Ascendente'})")


# ==============================================================================
# 4. Estadisticas e Indicadores

def mostrar_estadisticas(paises):
    """
    Calcula y muestra métricas clave:
    - Pais con mayor y menor poblacion.
    - Promedio de poblacion y superficie.
    - Cantidad de paises por continente.
    """
    print("\n==============================================")
    print("           Estadisticas Generales            ")
    print("==============================================")
    if not paises:
        print("No hay datos suficientes para calcular estadisticas.")
        return

    max_pob = max(paises, key=lambda p: p['poblacion'])
    min_pob = min(paises, key=lambda p: p['poblacion'])

    total_poblacion = sum(p['poblacion'] for p in paises)
    total_superficie = sum(p['superficie'] for p in paises)
    cant_paises = len(paises)

    promedio_poblacion = total_poblacion / cant_paises
    promedio_superficie = total_superficie / cant_paises

    conteo_continentes = {}
    for p in paises:
        cont = p['continente']
        conteo_continentes[cont] = conteo_continentes.get(cont, 0) + 1

    print(f"• Total de paises registrados: {cant_paises}")
    print(f"• Pais con MAYOR poblacion  : {max_pob['nombre']} ({max_pob['poblacion']:,} hab.)")
    print(f"• Pais con MENOR poblacion  : {min_pob['nombre']} ({min_pob['poblacion']:,} hab.)")
    print(f"• Promedio de Poblacion     : {promedio_poblacion:,.2f} hab.")
    print(f"• Promedio de Superficie    : {promedio_superficie:,.2f} km²")
    print("\n• Cantidad de Paises por Continente:")
    for cont, cant in conteo_continentes.items():
        print(f"   - {cont}: {cant}")
    print("==============================================\n")


# ==============================================================================
# 5. Funciones Auxiliares De Formateo Y Entrada

def mostrar_listado_paises(lista, titulo="Listado de Paises"):
    """
    Imprime una tabla alineada en consola con el contenido de la lista dada.
    """
    print(f"\n--- {titulo.upper()} ---")
    if not lista:
        print("No se encontraron registros.")
        return

    encabezado = f"{'Nombre':<20} | {'Poblacion':<15} | {'Superficie (km²)':<18} | {'Continente':<15}"
    print("-" * len(encabezado))
    print(encabezado)
    print("-" * len(encabezado))

    for p in lista:
        print(f"{p['nombre']:<20} | {p['poblacion']:<15,} | {p['superficie']:<18,} | {p['continente']:<15}")
    print("-" * len(encabezado))


def leer_entero_positivo(mensaje):
    """
    Solicita un entero por consola y reitera la peticion hasta recibir un valor numérico valido >= 0.
    """
    while True:
        valor_str = input(mensaje).strip()
        try:
            val = int(valor_str)
            if val < 0:
                print("El valor debe ser un entero positivo o cero.")
                continue
            return val
        except ValueError:
            print("Entrada no valida. Por favor, ingrese un numero entero.")


# ==============================================================================
# 6. Menu Principal Y Punto De Entrada


def menu_principal():
    """
    Controlador central de la aplicacion mediante menu interactivo.
    """
    paises = cargar_datos_csv(RUTA_CSV)

    while True:
        print("\n==============================================")
        print("    Sistema De Gestion De Datos De Paises    ")
        print("==============================================")
        print("1. Mostrar todos los paises")
        print("2. Agregar un pais")
        print("3. Actualizar poblacion/superficie de un pais")
        print("4. Buscar un pais por nombre")
        print("5. Filtrar paises")
        print("6. Ordenar paises")
        print("7. Mostrar estadisticas generales")
        print("8. Salir")
        print("==============================================")

        opcion = input("Seleccione una opcion (1-8): ").strip()

        if opcion == "1":
            mostrar_listado_paises(paises, "Todos los Paises Registrados")
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_pais(paises)
        elif opcion == "5":
            filtrar_paises(paises)
        elif opcion == "6":
            ordenar_paises(paises)
        elif opcion == "7":
            mostrar_estadisticas(paises)
        elif opcion == "8":
            print("\nGracias por utilizar el sistema")
            break
        else:
            print(" Opcion no valida. Intente nuevamente")


if __name__ == "__main__":
    menu_principal()