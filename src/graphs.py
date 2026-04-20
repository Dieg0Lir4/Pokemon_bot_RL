import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("resultados/metricas.csv")

plt.figure(figsize=(10, 5))
plt.plot(df["batalla"], df["winrate_vs_heuristics"], marker="o")
plt.xlabel("Batalla")
plt.ylabel("Winrate (%)")
plt.title("Winrate vs SimpleHeuristicsPlayer")
plt.grid(True)
plt.savefig("resultados/winrate.png")
plt.show()
print("Gráfica guardada en resultados/winrate.png")