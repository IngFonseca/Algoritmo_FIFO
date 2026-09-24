"""Vista: solo widgets Tkinter. No contiene lógica de la simulación."""
import tkinter as tk
from tkinter import messagebox, ttk

import config

COLORES_ESTADO = {
    "Espera": "#fff3cd",
    "Ejecución": "#cfe2ff",
    "Terminado": "#d1e7dd",
    "Rechazado": "#f8d7da",
}


class VistaPrincipal(ttk.Frame):
    COLUMNAS = (
        ("id", "ID", 60),
        ("tamano", "Tamaño", 80),
        ("tiempo", "Tiempo (s)", 90),
        ("restante", "Restante (s)", 100),
        ("llegada", "Llegada (s)", 90),
        ("estado", "Estado", 110),
    )

    def __init__(self, root: tk.Tk):
        super().__init__(root, padding=10)
        root.title("Simulador FIFO de Procesos")
        root.geometry("900x560")
        root.minsize(760, 420)
        self.pack(fill=tk.BOTH, expand=True)

        self._var_reloj = tk.StringVar(value="Reloj: 0 s")
        self._var_cola = tk.StringVar(value=f"Cola: 0/{config.CAPACIDAD_COLA}")
        self._var_cpu = tk.StringVar(value="CPU: libre")
        self._var_velocidad = tk.StringVar(value=f"{config.VELOCIDADES[0]}x")

        self._crear_resumen()
        self._crear_tabla()
        self._crear_controles()

    # ---------- construcción ----------
    def _crear_resumen(self):
        barra = ttk.Frame(self)
        barra.pack(fill=tk.X)
        for var in (self._var_reloj, self._var_cola, self._var_cpu):
            ttk.Label(barra, textvariable=var, font=("Segoe UI", 11, "bold")).pack(
                side=tk.LEFT, padx=(0, 25)
            )

    def _crear_tabla(self):
        marco = ttk.Frame(self)
        marco.pack(fill=tk.BOTH, expand=True, pady=8)

        self.tabla = ttk.Treeview(
            marco, columns=[c[0] for c in self.COLUMNAS], show="headings"
        )
        for clave, titulo, ancho in self.COLUMNAS:
            self.tabla.heading(clave, text=titulo)
            self.tabla.column(clave, width=ancho, anchor=tk.CENTER)
        for estado, color in COLORES_ESTADO.items():
            self.tabla.tag_configure(estado, background=color)

        scroll = ttk.Scrollbar(marco, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def _crear_controles(self):
        barra = ttk.Frame(self)
        barra.pack(fill=tk.X)

        self.btn_iniciar = ttk.Button(barra, text="Iniciar / Reanudar")
        self.btn_detener = ttk.Button(barra, text="Detener", state=tk.DISABLED)
        self.btn_reiniciar = ttk.Button(barra, text="Reiniciar")
        for boton in (self.btn_iniciar, self.btn_detener, self.btn_reiniciar):
            boton.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(barra, text="Velocidad:").pack(side=tk.LEFT, padx=(20, 5))
        ttk.Combobox(
            barra,
            textvariable=self._var_velocidad,
            values=[f"{v}x" for v in config.VELOCIDADES],
            state="readonly",
            width=5,
        ).pack(side=tk.LEFT)

    # ---------- API pública para el controlador ----------
    def vincular(self, on_iniciar, on_detener, on_reiniciar):
        self.btn_iniciar.config(command=on_iniciar)
        self.btn_detener.config(command=on_detener)
        self.btn_reiniciar.config(command=on_reiniciar)

    def velocidad(self) -> int:
        try:
            return int(self._var_velocidad.get().rstrip("x"))
        except ValueError:
            return 1

    def establecer_simulando(self, simulando: bool):
        self.btn_iniciar.config(state=tk.DISABLED if simulando else tk.NORMAL)
        self.btn_detener.config(state=tk.NORMAL if simulando else tk.DISABLED)

    def limpiar(self):
        self.tabla.delete(*self.tabla.get_children())

    def actualizar(self, procesos, datos: dict):
        self._var_reloj.set(f"Reloj: {datos['reloj']} s")
        self._var_cola.set(f"Cola: {datos['en_cola']}/{datos['capacidad']}")
        cpu = datos["cpu_id"]
        self._var_cpu.set("CPU: libre" if cpu is None else f"CPU: P{cpu}")

        for p in procesos:
            estado = p.estado.value
            restante = "-" if estado == "Rechazado" else p.restante
            valores = (p.id, p.tamano, p.tiempo, restante, p.llegada, estado)
            iid = str(p.id)
            if self.tabla.exists(iid):
                self.tabla.item(iid, values=valores, tags=(estado,))
            else:
                self.tabla.insert("", tk.END, iid=iid, values=valores, tags=(estado,))
        if cpu is not None:
            self.tabla.see(str(cpu))

    def mostrar_estadisticas(self, d: dict):
        messagebox.showinfo(
            "Estadísticas",
            "📊 Estadísticas del sistema\n\n"
            f"Tiempo simulado: {d['reloj']} s\n"
            f"Procesos creados: {d['creados']}\n"
            f"Procesos atendidos: {d['atendidos']}\n"
            f"Procesos finalizados: {d['finalizados']}\n"
            f"Procesos rechazados: {d['rechazados']}\n"
            f"Tiempo promedio de ejecución: {d['prom_ejecucion']:.2f} s\n"
            f"Tiempo promedio de espera: {d['prom_espera']:.2f} s\n"
            f"Tiempo promedio de retorno: {d['prom_retorno']:.2f} s\n"
            f"Uso de CPU: {d['uso_cpu']:.1f} %",
            parent=self,
        )