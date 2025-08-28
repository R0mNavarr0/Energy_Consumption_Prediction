import bentoml
import pandas as pd
import numpy as np

@bentoml.service
class EnerygyCO2Service:
    def __init__(self) -> None:
        self.energy_runner = bentoml.sklearn.load_model("energy_consumption_model_light:latest")
        self.co2_runner = bentoml.sklearn.load_model("c02_emissions_model:latest")

    @bentoml.api
    def energy_predict(self, data: dict) -> dict:
        data_log = {k: np.log1p(v) for k, v in data.items()}
        df = pd.DataFrame([data_log])
        y_pred_energy = self.energy_runner.predict(df)
        X_energy = pd.DataFrame(y_pred_energy, columns=["SiteEnergyUseWN(kBtu)"])
        y_pred_co2 = self.co2_runner.predict(X_energy)
        return {
        "predicted_energy": float(np.expm1(y_pred_energy[0])),
        "predicted_co2": float(np.expm1(y_pred_co2[0]))
    }