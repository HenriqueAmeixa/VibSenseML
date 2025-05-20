# 📡 Sensor Anomaly Detection

Projeto em Python para detecção automática de **anomalias em dados de sensores** (aceleração) usando aprendizado de máquina com **Isolation Forest**. Os dados são coletados via API, processados e classificados em tempo real como normais ou anômalos.

---

## 🧠 Funcionalidades

- Coleta contínua de dados de sensores via API REST
- Treinamento inicial com dados históricos
- Detecção em tempo real com atualização incremental
- Processamento com *rolling mean* para suavização de sinais
- Indicação de anomalias nos eixos X, Y e Z

---

## 📁 Estrutura do Projeto

```
.
├── main.py                # Loop principal de polling e detecção
├── fetch_data.py          # Função para buscar dados da API
├── model.py               # Classe com o modelo de detecção (IsolationForest)
├── config.py              # Variáveis de configuração (API, limite, etc.)
└── requirements.txt       # Dependências do projeto
```

---

## ⚙️ Requisitos

- Python 3.10+
- Bibliotecas:

```bash
pip install -r requirements.txt
```

Conteúdo sugerido de `requirements.txt`:

```
polars
scikit-learn
requests
```

---

## 🛠️ Configuração

Crie um arquivo `config.py` com os seguintes parâmetros:

```python
API_URL = "https://sua-api.com/api/SensorReadings/lote"
DEVICE_ID = "seu-id-do-dispositivo"
LIMIT = 500  # número máximo de registros por polling
```

---

## ▶️ Como executar

```bash
python main.py
```

A saída exibirá:

- 🔄 Quando está buscando dados
- ✅ Treino ou reuso do modelo
- 🚨 Quando detectar anomalias com os dados detalhados

---

## 📊 Exemplo de saída

```
Iniciando polling...
🔄 Carregando dados históricos para treino...
✅ 15000 dados carregados para treino.
✅ Modelo treinado com dados históricos.
Consultando API...
🚨 Anomalias detectadas:
┌─────────────────────┬────────┬────────┬────────┐
│ timestamp           │ accelX │ accelY │ accelZ │
├─────────────────────┼────────┼────────┼────────┤
│ 2025-05-20T10:14:32 │ 0.198  │ -0.355 │ 1.234  │
└─────────────────────┴────────┴────────┴────────┘
```

---

## 📌 Observações

- O modelo usa `IsolationForest` com contaminação extremamente baixa (`0.0001`) para capturar apenas comportamentos raros.
- A suavização do sinal é feita com média móvel de 5 amostras.
- A coluna `anomaly = -1` indica uma anomalia.

---

## 📄 Licença

MIT License
