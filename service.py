import bentoml
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field

class EnergyInput(BaseModel):
    PropertyGFATotal: float = Field(..., example=10000)
    PropertyGFABuilding_s: float = Field(..., example=8000, alias="PropertyGFABuilding(s)")
    LargestPropertyUseTypeGFA: float = Field(..., example=6000)
    Electricity_Part: float = Field(..., example=70, le=100, ge=0)
    NaturalGas_Part: float = Field(..., example=30, le=100, ge=0)
    BuildingAge: float = Field(..., example=20)

@bentoml.service
class EnergyCO2Service:
    def __init__(self) -> None:
        self.energy_runner = bentoml.sklearn.load_model("energy_consumption_model_light:epy5jnmee2j44aav")
        self.co2_runner = bentoml.sklearn.load_model("c02_emissions_model:aom7at4csoiheaav")

    @bentoml.api
    def energy_predict(self, data: dict) -> dict:
        validated_data = EnergyInput(**data).dict(by_alias=True)
        data_log = {k: np.log1p(v) for k, v in validated_data.items()}
        df = pd.DataFrame([data_log])
        y_pred_energy = self.energy_runner.predict(df)
        X_energy = pd.DataFrame(y_pred_energy, columns=["SiteEnergyUseWN(kBtu)"])
        y_pred_co2 = self.co2_runner.predict(X_energy)
        return {
        "Energy consumption (Kbtu)": float(np.expm1(y_pred_energy[0])),
        "CO2 emissions (Metric tons)": float(np.expm1(y_pred_co2[0]))
    }