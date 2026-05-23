import random
import time
import argparse
from datetime import datetime


def generar_valores_sensores(rangos):
    """Genera un diccionario con valores de sensores simulados usando rangos configurables."""
    return {
        "temperatura_c": round(random.uniform(rangos["temp_min"], rangos["temp_max"]), 2),
        "humedad_pct": round(random.uniform(rangos["hum_min"], rangos["hum_max"]), 2),
        "presion_hpa": round(random.uniform(rangos["pres_min"], rangos["pres_max"]), 2),
        "luminosidad_lux": round(random.uniform(rangos["lum_min"], rangos["lum_max"]), 2),
        "co2_ppm": round(random.uniform(rangos["co2_min"], rangos["co2_max"]), 2),
    }


def imprimir_valores(valores):
    """Imprime los valores de sensores con marca de tiempo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = ", ".join(f"{clave}: {valor}" for clave, valor in valores.items())
    print(f"[{timestamp}] {datos}")


def ejecutar_simulacion(intervalo: float, iteraciones: int, rangos: dict):
    """Ejecuta la simulación de sensores por un número de iteraciones."""
    for i in range(1, iteraciones + 1):
        valores = generar_valores_sensores(rangos)
        imprimir_valores(valores)
        if i < iteraciones:
            time.sleep(intervalo)


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Simula valores de sensores y los muestra en la consola."
    )
    parser.add_argument(
        "-i",
        "--intervalo",
        type=float,
        default=1.0,
        help="Intervalo en segundos entre lecturas de sensores (por defecto: 1.0).",
    )
    parser.add_argument(
        "-n",
        "--iteraciones",
        type=int,
        default=10,
        help="Número de lecturas a generar (por defecto: 10).",
    )
    parser.add_argument("--temp-min", type=float, default=18.0, help="Temperatura mínima en °C.")
    parser.add_argument("--temp-max", type=float, default=30.0, help="Temperatura máxima en °C.")
    parser.add_argument("--hum-min", type=float, default=30.0, help="Humedad mínima en %.")
    parser.add_argument("--hum-max", type=float, default=80.0, help="Humedad máxima en %.")
    parser.add_argument("--pres-min", type=float, default=990.0, help="Presión mínima en hPa.")
    parser.add_argument("--pres-max", type=float, default=1035.0, help="Presión máxima en hPa.")
    parser.add_argument("--lum-min", type=float, default=100.0, help="Luminosidad mínima en lux.")
    parser.add_argument("--lum-max", type=float, default=800.0, help="Luminosidad máxima en lux.")
    parser.add_argument("--co2-min", type=float, default=400.0, help="CO2 mínima en ppm.")
    parser.add_argument("--co2-max", type=float, default=1200.0, help="CO2 máxima en ppm.")
    return parser


def main():
    parser = crear_parser()
    args = parser.parse_args()
    rangos = {
        "temp_min": args.temp_min,
        "temp_max": args.temp_max,
        "hum_min": args.hum_min,
        "hum_max": args.hum_max,
        "pres_min": args.pres_min,
        "pres_max": args.pres_max,
        "lum_min": args.lum_min,
        "lum_max": args.lum_max,
        "co2_min": args.co2_min,
        "co2_max": args.co2_max,
    }

    ejecutar_simulacion(args.intervalo, args.iteraciones, rangos)


if __name__ == "__main__":
    main()
