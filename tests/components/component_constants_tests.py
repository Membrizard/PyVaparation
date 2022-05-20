from component import AllComponents, Component
from utils import AntoineConstants, HeatCapacityConstants
from experiments import IdealExperiments
from mixture import AllMixtures

all_components = AllComponents.load("components.yml")


def test_constants_h2o():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1115/1.3687121

    assert abs(all_components.h2o.get_antoine_pressure(313) - 7.31934) < 1e-4
    assert abs(all_components.h2o.get_antoine_pressure(323) - 12.24821) < 1e-4
    assert abs(all_components.h2o.get_antoine_pressure(333) - 19.78961) < 1e-4

    # Specific Heat Constants Calculated from http://dx.doi.org/10.1021/je900208n

    assert abs(all_components.h2o.get_specific_heat(313) - 33.725516) < 1e-4
    assert abs(all_components.h2o.get_specific_heat(323) - 33.800943) < 1e-4
    assert abs(all_components.h2o.get_specific_heat(333) - 33.877785) < 1e-4


def test_constants_meoh():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1016/0021-9614(75)90267-0

    assert abs(all_components.meoh.get_antoine_pressure(313) - 35.1986) < 1e-4
    assert abs(all_components.meoh.get_antoine_pressure(323) - 55.2130) < 1e-4
    assert abs(all_components.meoh.get_antoine_pressure(333) - 84.0491) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.meoh.get_specific_heat(313) - 35.1986) < 1e-4
    assert abs(all_components.meoh.get_specific_heat(323) - 55.2130) < 1e-4
    assert abs(all_components.meoh.get_specific_heat(333) - 84.0491) < 1e-4


def test_constants_etoh():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1016/0021-9614(75)90267-0

    assert abs(all_components.etoh.get_antoine_pressure(313) - 17.7708) < 1e-4
    assert abs(all_components.etoh.get_antoine_pressure(323) - 29.2779) < 1e-4
    assert abs(all_components.etoh.get_antoine_pressure(333) - 46.5843) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.etoh.get_specific_heat(313) - 17.7708) < 1e-4
    assert abs(all_components.etoh.get_specific_heat(323) - 29.2779) < 1e-4
    assert abs(all_components.etoh.get_specific_heat(333) - 46.5843) < 1e-4


def test_constants_ipoh():

    # Antoine Pressure Constants Calculated from https://doi.org/10.1016/j.fluid.2015.09.052

    assert abs(all_components.ipoh.get_antoine_pressure(313) - 13.7388) < 1e-4
    assert abs(all_components.ipoh.get_antoine_pressure(323) - 23.4142) < 1e-4
    assert abs(all_components.ipoh.get_antoine_pressure(333) - 38.2827) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.ipoh.get_specific_heat(313) - 13.7388) < 1e-4
    assert abs(all_components.ipoh.get_specific_heat(323) - 23.4142) < 1e-4
    assert abs(all_components.ipoh.get_specific_heat(333) - 38.2827) < 1e-4


def test_constants_dme():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1021/ie50448a022

    assert abs(all_components.dme.get_antoine_pressure(313) - 18.4210) < 1e-4
    assert abs(all_components.dme.get_antoine_pressure(323) - 26.6299) < 1e-4
    assert abs(all_components.dme.get_antoine_pressure(333) - 37.5490) < 1e-4

    # Specific Heat Constants Calculated from http://doi.org/10.1021/acs.jced.1c00229

    assert abs(all_components.dme.get_specific_heat(313) - 193.95434) < 1e-4
    assert abs(all_components.dme.get_specific_heat(323) - 195.75853) < 1e-4
    assert abs(all_components.dme.get_specific_heat(333) - 197.73868) < 1e-4


def test_constants_dmc():

    # Antoine Pressure Constants Calculated from https://doi.org/10.1016/j.fluid.2011.08.007

    assert abs(all_components.dmc.get_antoine_pressure(313) - 14.6761) < 1e-4
    assert abs(all_components.dmc.get_antoine_pressure(323) - 22.9947) < 1e-4
    assert abs(all_components.dmc.get_antoine_pressure(333) - 34.7419) < 1e-4

    # Specific Heat Constants Calculated from http://doi.org/10.1021/acs.jced.7b00295

    assert abs(all_components.dmc.get_specific_heat(313) - 167.09697) < 1e-4
    assert abs(all_components.dmc.get_specific_heat(323) - 168.69313) < 1e-4
    assert abs(all_components.dmc.get_specific_heat(333) - 170.46484) < 1e-4


def test_constants_mtbe():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1135/cccc19691317

    assert abs(all_components.mtbe.get_antoine_pressure(313) - 60.1905) < 1e-4
    assert abs(all_components.mtbe.get_antoine_pressure(323) - 85.8647) < 1e-4
    assert abs(all_components.mtbe.get_antoine_pressure(333) - 119.4935) < 1e-4

    # Specific Heat Constants Calculated

    assert abs(all_components.mtbe.get_specific_heat(313) - 60.1905) < 1e-4
    assert abs(all_components.mtbe.get_specific_heat(323) - 85.8647) < 1e-4
    assert abs(all_components.mtbe.get_specific_heat(333) - 119.4935) < 1e-4


def test_constants_etbe():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1135/cccc19691317

    assert abs(all_components.etbe.get_antoine_pressure(313) - 31.2979) < 1e-4
    assert abs(all_components.etbe.get_antoine_pressure(323) - 45.9826) < 1e-4
    assert abs(all_components.etbe.get_antoine_pressure(333) - 65.7505) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.etbe.get_specific_heat(313) - 31.2979) < 1e-4
    assert abs(all_components.etbe.get_specific_heat(323) - 45.9826) < 1e-4
    assert abs(all_components.etbe.get_specific_heat(333) - 65.7505) < 1e-4


def test_constants_cyclohexane():

    # Antoine Pressure Constants Calculated from https://dx.doi.org/10.1039/tf9686400637

    assert abs(all_components.cyclohexane.get_antoine_pressure(313) - 24.6260) < 1e-4
    assert abs(all_components.cyclohexane.get_antoine_pressure(323) - 36.2458) < 1e-4
    assert abs(all_components.cyclohexane.get_antoine_pressure(333) - 51.9116) < 1e-4

    # Specific Heat Constants Calculated from Safir, L.I., Experimental determination
    # of the isobaric heat capacity of cyclohexane at atmospheric pressure,
    # Izv. Vyssh. Uchebn. Zaved. Neft. Gaz 21, 1978, (12), 81-82.

    assert abs(all_components.cyclohexane.get_specific_heat(313) - 24.6260) < 1e-4
    assert abs(all_components.cyclohexane.get_specific_heat(323) - 36.2458) < 1e-4
    assert abs(all_components.cyclohexane.get_specific_heat(333) - 51.9116) < 1e-4


def test_constants_benzene():

    # Antoine Pressure Constants Calculated from https://doi.org/10.1002/9781118477304.app2

    assert abs(all_components.benzene.get_antoine_pressure(313) - 24.3752) < 1e-4
    assert abs(all_components.benzene.get_antoine_pressure(323) - 36.1835) < 1e-4
    assert abs(all_components.benzene.get_antoine_pressure(333) - 52.2136) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.benzene.get_specific_heat(313) - 24.3752) < 1e-4
    assert abs(all_components.benzene.get_specific_heat(323) - 36.1835) < 1e-4
    assert abs(all_components.benzene.get_specific_heat(333) - 52.2136) < 1e-4


def test_constants_toluene():

    # Antoine Pressure Constants Calculated from https://doi.org/10.1002/9781118477304.app2

    assert abs(all_components.toluene.get_antoine_pressure(313) - 7.8949) < 1e-4
    assert abs(all_components.toluene.get_antoine_pressure(323) - 12.2889) < 1e-4
    assert abs(all_components.toluene.get_antoine_pressure(333) - 18.5332) < 1e-4

    # Specific Heat Constants Calculated from

    assert abs(all_components.toluene.get_specific_heat(313) - 7.8949) < 1e-4
    assert abs(all_components.toluene.get_specific_heat(323) - 12.2889) < 1e-4
    assert abs(all_components.toluene.get_specific_heat(333) - 18.5332) < 1e-4
