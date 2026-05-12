# Sistema Académico – Registro de Notas
Aplicación de escritorio para registrar y evaluar el desempeño académico de
estudiantes. Permite buscar un estudiante por documento, ingresar sus notas
y porcentaje de asistencia, y obtener su estado de aprobación o reprobación.
El proyecto ofrece **dos interfaces gráficas independientes** que comparten
la misma lógica de negocio:
| Archivo | Tecnología | Descripción |
|---|---|---|
| `logica.py` | Python puro | Lógica de negocio y validaciones |
| `app_ctk.py` | CustomTkinter | GUI nativa de escritorio |
| `app_flet.py` | Flet | GUI multiplataforma moderna |
---
## Flujo de uso
```
Ingresar documento → Buscar Estudiante
 ↓ (encontrado)
Seleccionar materia, notas y asistencia → Calcular
 ↓
Ver resultado → Ingresar Datos Nuevos (reinicia el formulario)
```
---
## logica.py – Módulo de lógica de negocio
Contiene los datos estáticos y todas las funciones de validación y cálculo.
Es importado por ambas interfaces gráficas.
### Constantes
| Constante | Tipo | Descripción |
|---|---|---|
| `ESTUDIANTES` | `dict` | Mapa de documento → nombre. Base de datos
estática con 5 estudiantes. |
| `ASIGNATURAS` | `list` | Lista de las 4 asignaturas disponibles para
seleccionar. |
### Funciones

#### `buscar_estudiante(documento)`
Busca un estudiante en `ESTUDIANTES` por su número de documento.
- **Parámetro:** `documento` (str) – número de documento.
- **Retorna:** nombre completo del estudiante (str) o `None` si no existe.
#### `validar_nota(valor)`
Verifica que una nota sea un número entre **0 y 5** inclusive.
- **Parámetro:** `valor` – dato a evaluar (str o numérico).
- **Retorna:** `True` si es válido, `False` en caso contrario.
#### `validar_asistencia(valor)`
Verifica que la asistencia sea un número entre **0 y 100** inclusive.
- **Parámetro:** `valor` – dato a evaluar (str o numérico).
- **Retorna:** `True` si es válido, `False` en caso contrario.
#### `calcular_estado(notas, asistencia)`
Calcula el promedio de notas y determina el estado académico aplicando las
siguientes reglas en orden:
1. Asistencia < 80 % → **Reprobó por inasistencia**
2. Promedio ≥ 3.0 → **Aprobado**
3. Promedio < 3.0 → **Reprobó por nota**
- **Parámetros:** `notas` (list[float]), `asistencia` (float).
- **Retorna:** tupla `(promedio, mensaje, color)` donde color es `"green"` o
`"red"`.
---
## app_ctk.py – Interfaz con CustomTkinter
Interfaz de escritorio nativa construida con **CustomTkinter 5.2**, una
extensión moderna de Tkinter que aplica un tema visual contemporáneo con
soporte para modo oscuro/claro.
### Funciones
#### `buscar()`
Disparada por el botón "Buscar Estudiante". Lee el documento de `entry_doc`,
consulta `buscar_estudiante()` y, si el estudiante existe, muestra su nombre
y llama a `_habilitar_formulario(True)`. Si no existe, muestra error y llama
a `_habilitar_formulario(False)`.
#### `_habilitar_formulario(habilitar)`

Activa o desactiva el conjunto de widgets del formulario (`combo_materia`,
`n1`, `n2`, `n3`, `entry_asis`, `btn_calcular`). Cuando deshabilita, retira
`btn_nuevo` del layout con `pack_forget()`.
#### `calcular()`
Disparada por el botón "Calcular". Convierte los valores de los campos de
notas y asistencia a float, valida rangos y llama a `calcular_estado()`.
Muestra el resultado en `lbl_resultado` y añade `btn_nuevo` al layout.
#### `limpiar()`
Disparada por "Ingresar Datos Nuevos". Vacía todos los campos, restablece el
ComboBox a la primera asignatura y llama a `_habilitar_formulario(False)`
para volver al estado inicial.
### Componentes visuales
| Componente | Widget | Descripción |
|---|---|---|
| Etiquetas de sección | `CTkLabel` | Texto descriptivo que identifica cada
campo del formulario (Documento, Nombre, Materia, etc.). No es interactivo.
|
| Campo documento | `CTkEntry` | Caja de texto donde el usuario escribe el
número de documento para buscar al estudiante. |
| Botón buscar | `CTkButton` | Botón principal de la primera fase. Llama a
`buscar()` al hacer clic. |
| Campo nombre | `CTkEntry` | Caja de texto en modo `disabled` que solo
muestra el nombre recuperado automáticamente. El usuario no puede editarlo.
|
| Selector de materia | `CTkComboBox` | Menú desplegable que lista las
asignaturas disponibles. Inicia deshabilitado y se activa tras encontrar al
estudiante. |
| Contenedor de notas | `CTkFrame` | Marco transparente que agrupa los tres
campos de nota en una fila horizontal usando `pack(side="left")`. |
| Campos de notas (N1, N2, N3) | `CTkEntry` | Tres cajas de texto de ancho
reducido (50px) para ingresar cada nota. Inician deshabilitadas. |
| Campo asistencia | `CTkEntry` | Caja de texto para ingresar el porcentaje
de asistencia. Inicia deshabilitado. |
| Botón calcular | `CTkButton` | Dispara el cálculo del estado académico.
Inicia deshabilitado y se activa junto con el formulario. |
| Etiqueta resultado | `CTkLabel` | Muestra el promedio y el veredicto con
color dinámico (verde/rojo/naranja) y fuente en negrita. Usa `wraplength`
para que el texto no se desborde. |
| Botón datos nuevos | `CTkButton` | Aparece en el layout solo tras un
cálculo exitoso. Color gris para diferenciarlo visualmente. Llama a
`limpiar()`. |

---
## app_flet.py – Interfaz con Flet
Interfaz multiplataforma construida con **Flet 0.85**, un framework que
permite crear aplicaciones Flutter desde Python. Toda la lógica de UI vive
dentro de la función `main`, que Flet invoca al iniciar la aplicación.
### Funciones
#### `main(page)`
Punto de entrada. Configura la página, declara todos los componentes, define
las funciones de evento, asigna los callbacks y construye el layout con
`page.add()`.
#### `_habilitar_formulario(habilitar)`
Modifica la propiedad `disabled` de `cmb_materia`, `n1`, `n2`, `n3`,
`txt_asis` y `btn_calcular`. Cuando deshabilita, pone `btn_nuevo.visible =
False`. Llama a `page.update()` para aplicar los cambios en pantalla.
#### `buscar_click(_)`
Disparada por el botón "Buscar Estudiante". Lee `txt_doc.value`, consulta
`buscar_estudiante()` y actualiza `txt_nombre` y `lbl_res`. Habilita o
deshabilita el formulario según el resultado.
#### `calcular(e)`
Disparada por "Procesar Resultado". Convierte los valores de los campos a
float, valida rangos y llama a `calcular_estado()`. Actualiza `lbl_res` con
el resultado y muestra `btn_nuevo`.
#### `limpiar(_)`
Disparada por "Ingresar Datos Nuevos". Vacía todos los campos, resetea el
Dropdown y llama a `_habilitar_formulario(False)` para volver al estado
inicial.
### Componentes visuales
| Componente | Widget | Descripción |
|---|---|---|
| Título | `ft.Text` | Texto estático de encabezado con `size=30`. No es
interactivo. |
| Campo documento | `ft.TextField` | Campo de entrada de texto para el
número de documento. Habilitado desde el inicio. | 

| Botón buscar | `ft.ElevatedButton` | Botón elevado (con sombra Material
Design) que dispara `buscar_click`. |
| Campo nombre | `ft.TextField` | Campo con `read_only=True`: recibe el
nombre automáticamente pero el usuario no puede modificarlo. |
| Selector de materia | `ft.Dropdown` | Lista desplegable construida a
partir de `ASIGNATURAS` usando `ft.dropdown.Option`. Inicia con
`disabled=True`. |
| Fila de notas | `ft.Row` | Contenedor horizontal con `alignment=CENTER`
que agrupa los tres `TextField` de notas en una sola línea. |
| Campos de notas (N1, N2, N3) | `ft.TextField` | Tres campos de ancho fijo
(80px) para cada nota parcial. Inician con `disabled=True`. |
| Campo asistencia | `ft.TextField` | Campo de 120px para el porcentaje de
asistencia. Inicia con `disabled=True`. |
| Botón calcular | `ft.ElevatedButton` | Dispara `calcular`. Inicia con
`disabled=True` y se activa al encontrar al estudiante. Su callback se
asigna con `btn_calcular.on_click = calcular` para evitar referencias
adelantadas. |
| Etiqueta resultado | `ft.Text` | Texto dinámico con `size=20` y
`weight="bold"`. Su propiedad `color` cambia a `"green"`, `"red"` u
`"orange"` según el resultado. |
| Botón datos nuevos | `ft.ElevatedButton` | Inicia con `visible=False` y se
muestra solo tras un cálculo exitoso. Su callback se asigna con
`btn_nuevo.on_click = limpiar`. |
| Página | `ft.Page` | Contenedor raíz de la aplicación. Se configura con
`horizontal_alignment=CENTER` y `scroll=ADAPTIVE` para centrar el contenido
y permitir desplazamiento cuando sea necesario. |
---
## Instalación y ejecución
### Requisitos previos
- Python 3.10 o superior
### Configurar el entorno
```bash
# Crear entorno virtual
python -m venv venv
# Activar (Windows)
.\venv\Scripts\Activate.ps1
# Instalar dependencias
pip install -r requirements.txt

```
### Ejecutar
```bash
# Versión CustomTkinter
python app_ctk.py
# Versión Flet
python app_flet.py
```
---
## Documentos de prueba
| Documento | Nombre |
|---|---|
| 123 | Gabriel Rodríguez |
| 456 | Elena Luna |
| 789 | Carlos Pérez |
| 101 | Ana García |
| 202 | Luis Morales | 