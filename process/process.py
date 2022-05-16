import typing
from pathlib import Path

import attr

from mixture import Composition, Mixture


@attr.s(auto_attribs=True)
class ProcessModel:
    mixture: Mixture
    membrane_name: str
    isothermal: bool
    feed_temperature: typing.List[float]
    permeate_temperature: typing.List[float]
    feed_composition: typing.List[Composition]
    permeate_composition: typing.List[Composition]
    feed_mass: typing.List[float]
    partial_flux_1: typing.List[float]
    partial_flux_2: typing.List[float]
    time: typing.List[float]
    feed_evaporation_heat: typing.List[float]
    permeate_condensation_heat: typing.List[float]
    comments: typing.Optional[str]

    @property
    def separation_factor(self) -> typing.List[float]:
        return [0]

    @property
    def psi(self) -> typing.List[float]:
        return [0]

    @property
    def permeate_composition(self) -> typing.List[Composition]:
        return []

    @classmethod
    def from_csv(cls, path: typing.Union[str, Path]) -> "DiffusionCurve":
        pass
