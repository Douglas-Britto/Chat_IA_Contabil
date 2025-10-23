import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# === 1. Diretórios ===
base_dir = r"C:\Users\britt\Downloads\Projeto_Final_IA2A"
painel_dir = os.path.join(base_dir, "output", "painel_final")
os.makedirs(base_dir, exist_ok=True)

# === 2. Carregar dados ===
# Matriz de produtos
df_produtos = pd.read_csv(os.path.join(painel_dir, "matriz_produtos.csv"))

# Indicadores econômicos
df_economia = pd.read_csv(os.path.join(painel_dir, "dados_economia.csv"))

# === 3. Gráfico 1: Margem por Produto ===
plt.figure(figsize=(10, 6))
plt.bar(df_produtos["Produto"], df_produtos["Margem (%)"], color="#5CB85C")
plt.title("Margem por Produto")
plt.ylabel("Margem (%)")
plt.ylim(0, df_produtos["Margem (%)"].max() + 10)

for i, valor in enumerate(df_produtos["Margem (%)"]):
    plt.text(i, valor + 0.5, f"{valor:.1f}%", ha="center", fontsize=10)

plt.tight_layout()
nome1 = f"grafico_margem_produto_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
plt.savefig(os.path.join(base_dir, nome1))
plt.close()

# === 4. Gráfico 2: Crescimento por Produto ===
plt.figure(figsize=(10, 6))
plt.bar(df_produtos["Produto"], df_produtos["Crescimento (%)"], color="#337AB7")
plt.title("Crescimento Setorial por Produto")
plt.ylabel("Crescimento (%)")
plt.ylim(0, df_produtos["Crescimento (%)"].max() + 10)

for i, valor in enumerate(df_produtos["Crescimento (%)"]):
    plt.text(i, valor + 0.5, f"{valor:.1f}%", ha="center", fontsize=10)

plt.tight_layout()
nome2 = f"grafico_crescimento_produto_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
plt.savefig(os.path.join(base_dir, nome2))
plt.close()

# === 5. Gráfico 3: Indicadores Econômicos ===
plt.figure(figsize=(10, 6))
plt.bar(df_economia["Indicador"], df_economia["Valor"], color="#F39C12")
plt.title("Indicadores Econômicos – Outubro 2025")
plt.ylabel("Valor")
plt.ylim(0, df_economia["Valor"].max() * 1.2)

for i, valor in enumerate(df_economia["Valor"]):
    plt.text(i, valor + (df_economia["Valor"].max() * 0.02), f"{valor:.2f}", ha="center", fontsize=10)

plt.tight_layout()
nome3 = f"grafico_indicadores_economicos_{datetime.now().strftime('%Y%m%d_%H%M')}.png"
plt.savefig(os.path.join(base_dir, nome3))
plt.close()

# === 6. Confirmação ===
print("✅ Gráficos gerados com sucesso:")
print(f"- {nome1}")
print(f"- {nome2}")
print(f"- {nome3}")
