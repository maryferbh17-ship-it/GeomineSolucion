import argparse
import random
import tkinter as tk
from dataclasses import dataclass, field


@dataclass
class SensorConfig:
    nombre: str
    clave: str
    unidad: str
    minimo: float
    maximo: float
    label_valor: tk.Label = field(default=None, repr=False)
    label_rango: tk.Label = field(default=None, repr=False)


SENSORES = [
    SensorConfig("Temperatura", "temperatura_c", "°C", 18.0, 30.0),
    SensorConfig("Humedad", "humedad_pct", "%", 30.0, 80.0),
    SensorConfig("Presión", "presion_hpa", "hPa", 990.0, 1035.0),
    SensorConfig("Luminosidad", "luminosidad_lux", "lux", 100.0, 800.0),
    SensorConfig("CO2", "co2_ppm", "ppm", 400.0, 1200.0),
]


def generar_valor_sensor(sensor: SensorConfig) -> float:
    rango_extendido = (sensor.minimo - abs(sensor.minimo) * 0.1, sensor.maximo + abs(sensor.maximo) * 0.1)
    return round(random.uniform(*rango_extendido), 2)


def actualizar_valores(sensores, intervalo_ms):
    for sensor in sensores:
        valor = generar_valor_sensor(sensor)
        fuera_parametro = valor < sensor.minimo or valor > sensor.maximo
        color = "#ff7f7f" if fuera_parametro else "#d0ffd0"
        sensor.label_valor.config(text=f"{valor} {sensor.unidad}", bg=color)

    root.after(intervalo_ms, lambda: actualizar_valores(sensores, intervalo_ms))


def crear_dashboard(sensores, intervalo_ms):
    global root
    root = tk.Tk()
    root.title("Dashboard de Sensores")
    root.geometry("420x300")
    root.resizable(False, False)

    titulo = tk.Label(root, text="Lecturas de Sensores", font=("Arial", 16, "bold"))
    titulo.pack(pady=12)

    contenedor = tk.Frame(root)
    contenedor.pack(fill="both", expand=True, padx=12, pady=4)

    for sensor in sensores:
        fila = tk.Frame(contenedor)
        fila.pack(fill="x", pady=4)

        label_nombre = tk.Label(fila, text=f"{sensor.nombre}:", font=("Arial", 12), width=14, anchor="w")
        label_nombre.pack(side="left")

        sensor.label_valor = tk.Label(
            fila,
            text="---",
            font=("Arial", 12, "bold"),
            width=16,
            relief="solid",
            bd=1,
            bg="#ffffff",
        )
        sensor.label_valor.pack(side="left", padx=(0, 12))

        sensor.label_rango = tk.Label(
            fila,
            text=f"Rango: {sensor.minimo}-{sensor.maximo} {sensor.unidad}",
            font=("Arial", 10),
            fg="#333333",
        )
        sensor.label_rango.pack(side="left")

    info = tk.Label(root, text="Fondo rojo = fuera de parámetros", fg="#990000", font=("Arial", 10, "italic"))
    info.pack(pady=8)

    actualizar_valores(sensores, intervalo_ms)
    root.mainloop()


def crear_parser():
    parser = argparse.ArgumentParser(description="Dashboard en tiempo real para valores de sensores.")
    parser.add_argument(
        "-t",
        "--intervalo",
        type=float,
        default=1.0,
        help="Intervalo en segundos entre actualizaciones (por defecto: 1.0).",
    )
    parser.add_argument("--temp-min", type=float, default=18.0, help="Temperatura mínima aceptable.")
    parser.add_argument("--temp-max", type=float, default=30.0, help="Temperatura máxima aceptable.")
    parser.add_argument("--hum-min", type=float, default=30.0, help="Humedad mínima aceptable.")
    parser.add_argument("--hum-max", type=float, default=80.0, help="Humedad máxima aceptable.")
    parser.add_argument("--pres-min", type=float, default=990.0, help="Presión mínima aceptable.")
    parser.add_argument("--pres-max", type=float, default=1035.0, help="Presión máxima aceptable.")
    parser.add_argument("--lum-min", type=float, default=100.0, help="Luminosidad mínima aceptable.")
    parser.add_argument("--lum-max", type=float, default=800.0, help="Luminosidad máxima aceptable.")
    parser.add_argument("--co2-min", type=float, default=400.0, help="CO2 mínima aceptable.")
    parser.add_argument("--co2-max", type=float, default=1200.0, help="CO2 máxima aceptable.")
    return parser


def main():
    parser = crear_parser()
    args = parser.parse_args()

    for sensor in SENSORES:
        if sensor.clave == "temperatura_c":
            sensor.minimo = args.temp_min
            sensor.maximo = args.temp_max
        elif sensor.clave == "humedad_pct":
            sensor.minimo = args.hum_min
            sensor.maximo = args.hum_max
        elif sensor.clave == "presion_hpa":
            sensor.minimo = args.pres_min
            sensor.maximo = args.pres_max
        elif sensor.clave == "luminosidad_lux":
            sensor.minimo = args.lum_min
            sensor.maximo = args.lum_max
        elif sensor.clave == "co2_ppm":
            sensor.minimo = args.co2_min
            sensor.maximo = args.co2_max

    crear_dashboard(SENSORES, int(args.intervalo * 1000))


if __name__ == "__main__":
    main()
