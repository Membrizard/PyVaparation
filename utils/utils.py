import typing

import attr
import numpy
from numpy import ndarray

from ..component import Component

R = 8.314462


@attr.s(auto_attribs=True)
class Composition:
    # TODO: from 2 to n; state in which units the composition is in weight% or in mol% by introducing mol
    p: float = attr.ib(validator=lambda value: 0 <= value <= 1)  # type: ignore
    is_mol: bool

    def __getitem__(self, item: int):
        if item == 0:
            return self.p
        elif item == 1:
            return 1 - self.p
        else:
            raise ValueError("Index %s out of range" % item)

    # Convert molar composition to weight%
    @classmethod
    def to_wt(self, mixture) -> typing.List[float]:
        total = numpy.power(numpy.dot(numpy.transpose(
            [mixture.components.molecular_weight for component in mixture.components]), self), -1)
        self.is_mol = False
        return numpy.dot(numpy.multiply(self,
                                        [mixture.components.molecular_weight for component in mixture.components]),
                         total)
    # Convert weight composition to molar
    def to_mol(self, mixture)-> typing.List[float]:
        mw = [mixture.components.molecular_weight for component in mixture.components]
        self.is_mol = True
        return


@attr.s(auto_attribs=True)
class Conditions:
    membrane_area: float
    feed_temperature: float
    permeate_temperature: float
    feed_amount: float
    feed_composition: Composition
    isothermal: bool = True



@attr.s(auto_attribs=True)
class AntoineConstants:
    a: float = attr.ib(converter=lambda value: float(value))  # type: ignore
    b: float = attr.ib(converter=lambda value: float(value))  # type: ignore
    c: float = attr.ib(converter=lambda value: float(value))  # type: ignore


@attr.s(auto_attribs=True)
class NRTLParameters:
    g12: float
    g21: float
    alpha: float


@attr.s(auto_attribs=True)
class Mixture:
    components: typing.List[Component]
    nrtl_params: NRTLParameters

    def get_nrtl_partial_pressures(self, temperature: float, composition: Composition):
        tau = numpy.array(
            [
                self.nrtl_params.g12 / (R * temperature),
                self.nrtl_params.g21 / (R * temperature),
            ]
        )

        g_exp = numpy.exp(-tau * self.nrtl_params.alpha)

        activity_coefficients = [
            numpy.exp(
                (composition[1] ** 2)
                * (
                        tau[1]
                        * (g_exp[1] / (composition[0] + composition[1] * g_exp[1])) ** 2
                        + tau[0]
                        * g_exp[0]
                        / (composition[1] + composition[0] * g_exp[0]) ** 2
                )
            ),
            numpy.exp(
                (composition[0] ** 2)
                * (
                        tau[0]
                        * (g_exp[0] / (composition[1] + composition[0] * g_exp[0])) ** 2
                        + tau[1]
                        * g_exp[1]
                        / (composition[0] + composition[1] * g_exp[1]) ** 2
                )
            ),
        ]

        return (
            self.components[0].get_antoine_pressure(temperature)
            * activity_coefficients[0]
            * composition[0],
            self.components[1].get_antoine_pressure(temperature)
            * activity_coefficients[1]
            * composition[1],
        )

    # H2O/Ethanol
    @classmethod
    def h2o_etoh(cls) -> 'Mixture':
        return cls(
            components=[Component.h2o(), Component.etoh()],
            nrtl_params=NRTLParameters(
                g12=-633,
                g21=5823,
                alpha=0.3,
            )
        )

    # H2O/Isopropanol TODO: update parameters
    @classmethod
    def h2o_ipoh(cls) -> 'Mixture':
        return cls(
            components=[Component.h2o(), Component.ipoh()],
            nrtl_params=NRTLParameters(
                g12=0,
                g21=0,
                alpha=0.686,
            )
        )

    # EtOH/ETBE
    @classmethod
    def etoh_etbe(cls) -> 'Mixture':
        return cls(
            components=[Component.etoh(), Component.etbe()],
            nrtl_params=NRTLParameters(
                g12=726.34,
                g21=318.22,
                alpha=0.3,
            )
        )

    # MeOH/Toluene
    @classmethod
    def meoh_toluene(cls) -> 'Mixture':
        return cls(
            components=[Component.meoh(), Component.toluene()],
            nrtl_params=NRTLParameters(
                g12=3715.5266,
                g21=3085.3254,
                alpha=0.3,
            )
        )

    # MeOH/Methyl-tertButhyl ether
    @classmethod
    def meoh_mtbe(cls) -> 'Mixture':
        return cls(
            components=[Component.meoh(), Component.mtbe()],
            nrtl_params=NRTLParameters(
                g12=2025.3,
                g21=2133.5,
                alpha=0.6,
            )
        )

    # MeOH/DimethoxyEthane
    @classmethod
    def meoh_dme(cls) -> 'Mixture':
        return cls(
            components=[Component.meoh(), Component.dme()],
            nrtl_params=NRTLParameters(
                g12=782.0202,
                g21=-229.0431,
                alpha=0.2982,
            )
        )

    # MeOH/DimethylCarbonate
    @classmethod
    def meoh_dmc(cls) -> 'Mixture':
        return cls(
            components=[Component.meoh(), Component.dmc()],
            nrtl_params=NRTLParameters(
                g12=1429.444,
                g21=2641.108,
                alpha=0.2,
            )
        )

    # MeOH/Cyclohexane
    @classmethod
    def meoh_cyclohexane(cls) -> 'Mixture':
        return cls(
            components=[Component.meoh(), Component.cyclohexane()],
            nrtl_params=NRTLParameters(
                g12=6415.36,
                g21=5714,
                alpha=0.4199,
            )
        )


# Experiments for Ideal modelling
@attr.s(auto_attribs=True)
class IdealExperiment:
    # TODO: include validation while loading form config
    #  Permeance can't be negative;
    # Temperature can't be negative
    temperature: float
    # Permeance in kg*mcm/(m2*h*kPa)
    permeance: float
    component: Component
    activation_energy: typing.Optional[float] = None


@attr.s(auto_attribs=True)
class Membrane:
    ideal_experiments: typing.List[IdealExperiment]
    DiffusionCurve: typing.List[DiffusionCurve]

    @property
    def ideal_experiments_names(self) -> typing.List[str]:
        return [ie.component.name for ie in self.ideal_experiments]

    # Get all the penetrants the membrane was tested for
    def get_known_penetrants(self) -> typing.List[Component]:
        return numpy.unique([
            ideal_experiment.component for ideal_experiment in self.ideal_experiments
        ])

    # Picking only Experiments related to the chosen component
    def get_penetrant_data(self, component) -> typing.List[IdealExperiment]:
        return list(
            filter(
                lambda value: value.component.name in self.ideal_experiments_names,
                self.ideal_experiments
            )
        )

    # Calculate an apparent activation energy of permeation
    def calculate_activation_energy(self, component, rewrite: bool = True, plot: bool = False) -> float:
        # Validation of the Ideal Experiments
        if len(self.get_penetrant_data()) >= 2:
            # Get all the temperature values corresponding to the permeances for a given penetrant convert to 1/T
            x = numpy.power([ideal_experiment.temperature for ideal_experiment in
                             self.get_penetrant_data(component)], -1)
            # Get all the permeance values for a given Penetrant convert to Ln(permeance)
            y = numpy.log([ideal_experiment.permeance for ideal_experiment in
                           self.get_penetrant_data(component)])
            # Converting Ln(permeance) to the matrix equation form
            A = numpy.vstack([x, numpy.ones(len(x))]).T
            # Calculation of Least-squares Linear Fit of Ln(Permeance) versus 1/T
            activation_energy, c = numpy.linalg.lstsq(A, y, rcond=-1)[0] * R
            if plot:
                # Plotting the graph Ln(Permeance) versus 1/T
                import matplotlib.pyplot as plt
                _ = plt.plot(x, y, 'o', label=component.name + 'Experimental Permeances', markersize=5)
                plt.xlabel("1/T, 1/K")
                plt.ylabel("Ln(Permeance)")
                _ = plt.plot(x, activation_energy * x + c, 'b', label='Fitted line')
                _ = plt.legend()
                plt.show()
                pass
            if rewrite:
                # Rewriting the corresponding activation energy values in Ideal Experiments of the Membrane
                for ideal_experiment in self.get_penetrant_data(component):
                    ideal_experiment.activation_energy = activation_energy
                # TODO: Rewrite in Config Membranes.yml or whatever

                return activation_energy
            else:
                return activation_energy
        else:
            print("At Least Two points are required for the calculation of Apparent Activation Energy")

    def get_permeance(self, temperature, component) -> float:
        # Definition of the corresponding temperatures list
        temperature_list = [ideal_experiment.temperature
                            for ideal_experiment in
                            self.get_penetrant_data(component)]
        # finding the index of the experiment with the closest available temperature
        index = min(range(len(temperature_list)), key=lambda i: abs(temperature_list[i] - temperature))
        # finding the Permeance in the experiment with the found index
        given_permeance = self.get_penetrant_data(component)[index].permeance
        # Trying to calculate the permeance at given temperature;
        # If activation is not specified it is being calculated using calculate_activation_energy function
        try:
            activation_energy = self.get_penetrant_data(component)[index].activation_energy
            return given_permeance * numpy.exp(-activation_energy / R * (1 / temperature - 1 / temperature_list[index]))
        except:
            # print('Provide Apparent Energy of Permeation for the component')
            activation_energy = self.calculate_activation_energy(component, rewrite=False, plot=False)
            return given_permeance * numpy.exp(-activation_energy / R * (1 / temperature - 1 / temperature_list[index]))

    # calculating the selectivity
    def get_ideal_selectivity(self, temperature, component1, component2) -> float:
        return self.get_permeance(temperature, component1) / self.get_permeance(temperature, component2)

# Diffusion curves for non-ideal modelling and output of the results
@attr.s(auto_attribs=True)
class DiffusionCurve:
    feed_temperature: float
    permeate_temperature: typing.Optional[float] = 0
    mixture: Mixture
    composition_range: typing.List[Composition]
    partial_fluxes: typing.List[typing.List[float]]
    total_flux: typing.List[float]
    separation_factor: typing.List[float]
    PSI: typing.List[float]

@attr.s(auto_attribs=True)
class PVProcess:


@attr.s(auto_attribs=True)
class Pervaporation:
    membrane: Membrane
    mixture: Mixture
    conditions: Conditions
    ideal: bool = True

    # Alexey please double check this
    def calculate_partial_fluxes(self, feed_temperature, permeate_temperature, composition, precision: float) -> float:
        # Calculating components' permeances at a given feed temperature:
        permeances = [self.membrane.get_permeance(feed_temperature, component) for component in self.mixture.components]
        # Defining function for saturation pressure calculation
        p_sat = lambda t, x: self.mixture.get_nrtl_partial_pressures(t, x)
        # Defining function for partial fluxes calculation from permeate composition
        partial_fluxes = lambda perm_comp: \
            numpy.matmul(permeances, numpy.substract(p_sat(feed_temperature, composition.to_mol()),
                                                     p_sat(permeate_temperature, perm_comp.to_mol)))
        # Defining function for permeate composition calculation
        permeate_composition = lambda fluxes: Composition(fluxes[0] / numpy.sum(fluxes))
        inital_fluxes = numpy.matmul(permeances, self.mixture.get_nrtl_partial_pressures(feed_temperature, composition))
        p_c = permeate_composition(inital_fluxes)
        d = 1
        # Precision of the permeate composition value - until the precision criteria is reached
        # That is definetly could be implemented in a better algorithmic way
        while d >= precision:
            p_c2 = permeate_composition(partial_fluxes(p_c))
            d = max(numpy.absolute(numpy.subtract(p_c2, p_c)))
            p_c = p_c2
        return partial_fluxes(p_c)

    # Calculate Permeate composition for at the given conditions
    def calculate_permeate_composition(self, feed_temperature, permeate_temperature, composition,
                                       precision: float) -> Composition:
        x = self.calculate_partial_fluxes(feed_temperature, permeate_temperature, composition, precision)
        return Composition(x[0] / numpy.sum(x))
    def calculate_separation_factor(self, feed_temperature, permeate_temperature, composition, precision: float):
        perm_comp = self.calculate_permeate_composition(feed_temperature,permeate_temperature,composition,precision)
        return (composition[1]/(1-composition[1]))/(perm_comp[1]/(1-perm_comp[1]))

    # Calculate Partial, Overall fluxes and other parameters as a function of composition in the given composition range
    def ideal_diffusion_curve(self, feed_temperature, permeate_temperature, composition_range, precision,
                              plot: bool = True) -> DiffusionCurve:
        diff_curv = DiffusionCurve()
        diff_curv.feed_temperature = feed_temperature
        diff_curv.mixture = self.mixture
        diff_curv.permeate_temperature = permeate_temperature
        diff_curv.composition_range_range = composition_range
        diff_curv.partial_fluxes = [self.calculate_partial_fluxes( feed_temperature, permeate_temperature, composition, precision) for
        composition in composition_range]
        diff_curv.separation_factor = [self.calculate_separation_factor( feed_temperature, permeate_temperature, composition, precision) for
        composition in composition_range]
        diff_curv.total_flux=[numpy.sum(diff_curv.partial_fluxes[i]) for i in range(len(diff_curv.partial_fluxes))]
        diff_curv.PSI = numpy.multiply(numpy.subtract(diff_curv.separation_factor, numpy.ones(0, len(composition_range))), diff_curv.total_flux)
        if plot:
            #TODO Plot the curve
            pass
        return diff_curv

    def model_ideal_process(self, conditions):
        pass

    def model_non_ideal_process(self, conditions):
        pass
