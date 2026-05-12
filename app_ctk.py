import customtkinter as ctk
from logica import buscar_estudiantes, ASIGNATURAS, validar_asistencia, calcular_estado, ESTUDIANTES


def buscar():


    doc = entry_doc.get().strip()
    nombre = buscar_estudiantes(doc)
    if not nombre:
        #lbl_resultado.configure(text="Estudiante no encontrado", text_color="red")
        #_habilitar_formulario(false)
        return
    entry_nombre.configure(state="normal")
    entry_nombre.delete(0, "end")
    entry_nombre.insert(0, nombre)
    entry_nombre.configure(state="disabled")
    #lbl_resultado.configure(text="Estudiante encontrado. complete los datos.", text_color="green")
    #_habilitar_formulario(true)



app = ctk.CTk()
app.title("sistema academico - customtkinter")
app.geometry("400x620")


ctk.CTkLabel(app, text="documento:").pack(pady=5)
entry_doc = ctk.CTkEntry(app)
entry_doc.pack()

ctk.CTkButton(app, text="buscar estudiante", command=buscar).pack(pady=8)

ctk.CTkLabel(app, text="nombre estudiantes:").pack(pady=5)
entry_nombre = ctk.CTkEntry(app, state="disabled")
entry_nombre.pack()


ctk.CTkLabel(app, text="materia:").pack(pady=5)
combo_materia = ctk.CTkComboBox(app, values=ASIGNATURAS, state="disabled")
combo_materia.pack()


app.mainloop()


