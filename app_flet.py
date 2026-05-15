"""
app_flet.py – Interfaz gráfica del Sistema Académico construida con Flet.

Flujo de uso:
    1. Ingresar el número de documento y presionar "Buscar Estudiante".
    2. Si el estudiante existe, se habilitan los campos del formulario.
    3. Completar materia, notas y asistencia, luego presionar "Procesar Resultado".
    4. Presionar "Ingresar Datos Nuevos" para reiniciar el formulario.
"""

import flet as ft
from logica import buscar_estudiante, ASIGNATURAS, validar_nota, validar_asistencia, calcular_estado


def main(page: ft.Page):
    """Punto de entrada de la aplicación Flet. Construye y gestiona toda la UI.

    Inicializa la página, declara todos los componentes visuales, define las
    funciones de manejo de eventos y agrega los controles a la página.

    Args:
        page (ft.Page): Objeto de página proporcionado automáticamente por el runtime de Flet.
                        Representa la ventana de la aplicación y contiene métodos
                        como page.add() y page.update() para modificar la interfaz.
    """
    page.title = "Sistema Académico - Flet"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # ---------------------------------------------------------------------------
    # Declaración de componentes
    # ---------------------------------------------------------------------------
    txt_doc = ft.TextField(label="Documento")
    txt_nombre = ft.TextField(label="Nombre", read_only=True)
    cmb_materia = ft.Dropdown(
        label="Materia",
        options=[ft.dropdown.Option(m) for m in ASIGNATURAS],
        disabled=True
    )
    n1 = ft.TextField(label="N1", width=80, disabled=True)
    n2 = ft.TextField(label="N2", width=80, disabled=True)
    n3 = ft.TextField(label="N3", width=80, disabled=True)
    txt_asis = ft.TextField(label="Asistencia %", width=120, disabled=True)
    lbl_res = ft.Text(size=20, weight="bold")
    btn_calcular = ft.ElevatedButton("Procesar Resultado", disabled=True)
    btn_nuevo = ft.ElevatedButton("Ingresar Datos Nuevos", visible=False)

    # ---------------------------------------------------------------------------
    # Funciones de manejo de eventos
    # ---------------------------------------------------------------------------

    def _habilitar_formulario(habilitar):
        """Habilita o deshabilita todos los campos del formulario de notas.

        Cambia la propiedad disabled de cmb_materia, n1, n2, n3, txt_asis y
        btn_calcular según el valor de habilitar. Cuando se deshabilita, también
        oculta btn_nuevo asignando visible=False. Llama a page.update() al final
        para reflejar los cambios en pantalla.

        Args:
            habilitar (bool): True para activar los campos, False para desactivarlos.
        """
        cmb_materia.disabled = not habilitar
        n1.disabled = not habilitar
        n2.disabled = not habilitar
        n3.disabled = not habilitar
        txt_asis.disabled = not habilitar
        btn_calcular.disabled = not habilitar
        if not habilitar:
            btn_nuevo.visible = False
        page.update()

    def buscar_click(_):
        """Busca al estudiante por documento y habilita el formulario si es encontrado.

        Lee el valor de txt_doc y consulta la base de datos mediante buscar_estudiante().
        Si el estudiante existe, muestra su nombre en txt_nombre y activa los campos
        llamando a _habilitar_formulario(True). Si no existe, limpia txt_nombre,
        muestra un mensaje de error en lbl_res y deshabilita el formulario.
        Llama a page.update() a través de _habilitar_formulario() para actualizar la UI.
        """
        nombre = buscar_estudiante(txt_doc.value.strip())
        if not nombre:
            txt_nombre.value = ""
            lbl_res.value = "Estudiante no encontrado"
            lbl_res.color = "red"
            _habilitar_formulario(False)
            return
        txt_nombre.value = nombre
        lbl_res.value = "Estudiante encontrado. Complete los datos."
        lbl_res.color = "green"
        _habilitar_formulario(True)

    def calcular(e):
        """Valida los datos del formulario y calcula el estado académico del estudiante.

        Convierte los valores de n1, n2, n3 y txt_asis a float y los valida con
        validar_nota() y validar_asistencia(). Si los rangos son correctos, llama a
        calcular_estado() y muestra el promedio y el veredicto en lbl_res.
        Al finalizar con éxito, hace visible btn_nuevo. Si algún campo no es numérico
        o está vacío, muestra un mensaje de error genérico. Llama a page.update()
        al final para reflejar los cambios en pantalla.

        Args:
            e: Evento de clic proporcionado por Flet (no utilizado directamente).
        """
        try:
            notas = [float(n1.value), float(n2.value), float(n3.value)]
            asis = float(txt_asis.value)
            if not all(validar_nota(n) for n in notas) or not validar_asistencia(asis):
                lbl_res.value = "Error en rangos de valores"
                lbl_res.color = "orange"
            else:
                prom, msg, color = calcular_estado(notas, asis)
                lbl_res.value = f"Promedio: {prom:.2f}\n{msg}"
                lbl_res.color = color
                btn_nuevo.visible = True
        except:
            lbl_res.value = "Llena todos los campos"
            lbl_res.color = "orange"
        page.update()

    def limpiar(_):
        """Reinicia todos los campos del formulario a su estado inicial vacío.

        Borra el documento, el nombre, las tres notas, el porcentaje de asistencia,
        el valor del Dropdown y el mensaje de resultado. Luego llama a
        _habilitar_formulario(False) para deshabilitar los campos y ocultar btn_nuevo.
        """
        txt_doc.value = ""
        txt_nombre.value = ""
        n1.value = ""; n2.value = ""; n3.value = ""
        txt_asis.value = ""
        cmb_materia.value = None
        lbl_res.value = ""
        lbl_res.color = None
        _habilitar_formulario(False)

    # Asignación de callbacks a botones declarados antes que sus manejadores
    btn_calcular.on_click = calcular
    btn_nuevo.on_click = limpiar

    # ---------------------------------------------------------------------------
    # Construcción del layout
    # ---------------------------------------------------------------------------
    page.add(
        ft.Text("Registro de Notas", size=30),
        txt_doc,
        ft.ElevatedButton("Buscar Estudiante", on_click=buscar_click),
        txt_nombre,
        cmb_materia,
        ft.Row([n1, n2, n3], alignment=ft.MainAxisAlignment.CENTER),
        txt_asis,
        btn_calcular,
        lbl_res,
        btn_nuevo,
    )


ft.run(main)
