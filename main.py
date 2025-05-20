import time
from fetch_data import get_sensor_data
from model import AnomalyDetector
import polars as pl

def main():
    print("Iniciando polling...")
    detector = AnomalyDetector()
    last_id = None
    first_run = True

    print("🔄 Carregando dados históricos para treino...")
    treino_df = get_sensor_data(after_id=None)  # ou um endpoint especial sem afterId

    if treino_df.is_empty():
        print("⚠️ Nenhum dado histórico para treinar.")
        exit()

    treino_df = treino_df.with_columns(
        pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.6f")
    )

    print(f"✅ {treino_df.shape[0]} dados carregados para treino.")
    detector = AnomalyDetector()
    detector.fit(treino_df)
    print("✅ Modelo treinado com dados históricos.")

    while True:
        print("Consultando API...")

        try:
            df = get_sensor_data(after_id=last_id)

            if df.is_empty():
                print("Nenhum dado novo.")
            else:
                df = df.with_columns(
                    pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%.6f")
                )

                if first_run:
                    detector.fit(df)
                    first_run = False

                result = detector.predict(df)
                anomalies = result.filter(pl.col("anomaly") == -1)

                if anomalies.height > 0:
                    print("🚨 Anomalias detectadas:")
                    print(anomalies.select(["timestamp", "accelX", "accelY", "accelZ"]))

                last_id = df.select(pl.col("id").max())[0, 0]

        except Exception as e:
            print(f"Erro durante polling: {e}")

        time.sleep(2)

if __name__ == "__main__":
    main()
