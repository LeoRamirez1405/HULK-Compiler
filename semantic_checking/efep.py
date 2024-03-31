# Supongamos que esta es tu lista de diccionarios
lista_de_diccionarios = [
    {'nombre': 'Juan', 'edad': 30},
    {'nombre': 'Ana', 'edad': 25},
    {'nombre': 'Carlos', 'edad': 35}
]

# Utilizamos una comprensión de lista para obtener el valor de la primera clave de cada diccionario
valores_primer_objeto = [list(diccionario.values())[0] for diccionario in lista_de_diccionarios]

print(valores_primer_objeto)
