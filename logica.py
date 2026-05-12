ESTUDIANTES = {
    "123": "alejandra mandanga",
    "456": "alejandro petrovic",
    "789": "meridel aguala",
    "101": "jose roberto",
    "202": "tatiana locala",
}

ASIGNATURAS = [
    "logica computacional"
    "introduccion a la ingenieria de datos"
    "calculo diferencial"
    "algebra lineal"
]


def buscar_estudiantes(documento):
    return ESTUDIANTES.get(documento, None)


def validar_nota(valor):
    try:
        nota = float(valor)
        return 0 <= nota <= 5
    except ValueError:
        return False
    
def validar_asistencia(valor):
    try:
        nota = float(valor)
        return 0 <= nota <= 100
    except ValueError:
        return False
    
def calcular_estado(notas, asistencia):
    promedio = sum(notas) / len(notas)

    if asistencia < 80:
        return promedio, "reprobo por inasistencia", "red"
    elif promedio >= 3.0:
        return promedio, "aprobado", "green"
    else:
        return promedio, "reprobo por nota", "red"

                       
    