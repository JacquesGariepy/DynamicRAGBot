import pandas as pd
from prophet import Prophet

class TrendPredictionService:
    def __init__(self):
        self.model = Prophet()

    def train_model(self, historical_data):
        df = pd.DataFrame(historical_data, columns=['ds', 'y'])
        self.model.fit(df)

    def predict_future(self, periods):
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]