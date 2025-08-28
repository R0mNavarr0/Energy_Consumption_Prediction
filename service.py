import bentoml
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field, validator

class EnergyInput(BaseModel):
    PropertyGFATotal: float = Field(..., example=10000)
    PropertyGFABuilding_s: float = Field(..., example=8000)
    LargestPropertyUseTypeGFA: float = Field(..., example=6000)
    Electricity_Part: float = Field(..., example=70)
    NaturalGas_Part: float = Field(..., example=30)
    BuildingAge: float = Field(..., example=20)

    @validator('Electricity_Part', 'NaturalGas_Part')
    def check_percentage(cls, v):
        if not (0 <= v <= 100):
            raise ValueError('Must be between 0 and 100')
        return v

@bentoml.service
class EnerygyCO2Service:
    def __init__(self) -> None:
        self.energy_runner = bentoml.sklearn.load_model("energy_consumption_model_light:latest")
        self.co2_runner = bentoml.sklearn.load_model("c02_emissions_model:latest")

    @bentoml.api
    def energy_predict(self, data: dict) -> dict:
        validated_data = EnergyInput(**data).dict()
        data_log = {k: np.log1p(v) for k, v in validated_data.items()}
        df = pd.DataFrame([data_log])
        y_pred_energy = self.energy_runner.predict(df)
        X_energy = pd.DataFrame(y_pred_energy, columns=["SiteEnergyUseWN(kBtu)"])
        y_pred_co2 = self.co2_runner.predict(X_energy)
        return {
        "predicted_energy": float(np.expm1(y_pred_energy[0])),
        "predicted_co2": float(np.expm1(y_pred_co2[0]))
    }