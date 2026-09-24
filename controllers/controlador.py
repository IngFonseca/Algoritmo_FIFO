"""Controlador: conecta la vista con el modelo y maneja el temporizador."""
import config


class ControladorFIFO:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista
        self._job = None
        self.vista.vincular(self.iniciar, self.detener, self.reiniciar)
        self._refrescar()

    def iniciar(self):
        if self._job is not None:
            return
        self.vista.establecer_simulando(True)
        self._programar()

    def detener(self):
        self._cancelar()
        self.vista.establecer_simulando(False)
        self.vista.mostrar_estadisticas(self.modelo.estadisticas())

    def reiniciar(self):
        self._cancelar()
        self.modelo.reiniciar()
        self.vista.limpiar()
        self.vista.establecer_simulando(False)
        self._refrescar()

    def cerrar(self):
        self._cancelar()
        self.vista.winfo_toplevel().destroy()

    # ---------- internos ----------
    def _tick(self):
        self.modelo.tick()
        self._refrescar()
        self._programar()

    def _programar(self):
        retraso = max(1, config.MS_POR_SEGUNDO_SIMULADO // self.vista.velocidad())
        self._job = self.vista.after(retraso, self._tick)

    def _cancelar(self):
        if self._job is not None:
            self.vista.after_cancel(self._job)
            self._job = None

    def _refrescar(self):
        self.vista.actualizar(self.modelo.todos(), self.modelo.estadisticas())