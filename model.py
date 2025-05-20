from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import polars as pl

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(
            contamination=0.0001,
            n_estimators=200,
            max_samples='auto',
            random_state=42
        )
        self.scaler = StandardScaler()

    def _prepare(self, df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns([
            pl.col("accelX").rolling_mean(5).fill_null(strategy="mean").alias("accelX"),
            pl.col("accelY").rolling_mean(5).fill_null(strategy="mean").alias("accelY"),
            pl.col("accelZ").rolling_mean(5).fill_null(strategy="mean").alias("accelZ"),
        ])

    def fit(self, df: pl.DataFrame):
        df = self._prepare(df)
        if df.is_empty():
            raise ValueError("DataFrame de treino ficou vazio após o pré-processamento.")
        X = df.select(["accelX", "accelY", "accelZ"]).to_numpy()
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled)

    def predict(self, df: pl.DataFrame) -> pl.DataFrame:
        df = self._prepare(df)
        if df.is_empty():
            raise ValueError("DataFrame de predição ficou vazio após o pré-processamento.")
        X = df.select(["accelX", "accelY", "accelZ"]).to_numpy()
        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)
        return df.with_columns(pl.Series("anomaly", preds))
