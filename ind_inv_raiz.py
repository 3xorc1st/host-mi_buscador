import re
from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

# Función para procesar la raíz de una palabra
def raiz(palabra):
    return re.sub(r'\W+', '', palabra.lower())

# Leyendo el archivo de urls
with open('urls.txt', 'r') as file:
    urls = file.readlines()

# Inicializando el diccionario invertido
raiz_ind_inv = defaultdict(list)

# Procesando cada url de manera concurrente
def procesar_url(url):
    frecuencia_palabras = []
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features="lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        words = re.findall(r'\w+', text)
        for word in words:
            frecuencia_palabras.append([raiz(word), url])
    except:
        print(f"Error al acceder a {url}")

    return frecuencia_palabras

num_hilos = 8  # Ajusta el número de hilos según sea necesario

with ThreadPoolExecutor(max_workers=num_hilos) as executor:
    futures = [executor.submit(procesar_url, url.strip()) for url in urls]

    for future in concurrent.futures.as_completed(futures):
        resultados = future.result()
        for raiz_word, url in resultados:
            raiz_ind_inv[raiz_word].append((url, 1))

# Escritura del nuevo diccionario en un archivo de texto
with open('raiz_ind_inv.txt', 'w', encoding='utf-8') as file:
    for root, urls in raiz_ind_inv.items():
        file.write(f"{root}: {urls}\n")
