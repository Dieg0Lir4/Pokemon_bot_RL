from scipy import stats
import pandas as pd

df = pd.read_csv("resultados/metricas.csv")

# Total de victorias y batallas de validación
total_batallas = len(df) * 50  # 50 batallas por validación
total_victorias = (df["winrate_vs_heuristics"] / 100 * 50).sum().astype(int)

# Prueba binomial
result = stats.binomtest(total_victorias, total_batallas, p=0.5, alternative='greater')
print(f"Victorias: {total_victorias} de {total_batallas}")
print(f"Winrate promedio: {total_victorias/total_batallas*100:.1f}%")
print(f"P-value: {result.pvalue:.4f}")

if result.pvalue < 0.05:
    print("Resultado significativo — el agente gana más del 50%")
else:
    print("No hay evidencia suficiente de que gane más del 50%")