"""Punto de entrada: python main.py"""
import tkinter as tk

from controllers.controlador import ControladorFIFO
from models.simulador import SimuladorFIFO
from views.vista_principal import VistaPrincipal


def main():
    root = tk.Tk()
    vista = VistaPrincipal(root)
    modelo = SimuladorFIFO()
    controlador = ControladorFIFO(modelo, vista)
    root.protocol("WM_DELETE_WINDOW", controlador.cerrar)
    root.mainloop()


if __name__ == "__main__":
    main()