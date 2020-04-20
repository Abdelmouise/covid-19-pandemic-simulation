import numpy as np

from scenario.scenario_helper import tighten_lockdown, soften_lockdown, measure_lockdown_strength
from simulator.dynamic_helper import propagate_to_stores, propagate_to_houses, propagate_to_workplaces, \
    increment_pandemic_1_day, is_weekend, get_pandemic_statistics, propagate_to_transportation
from simulator.parameters import *
from simulator.plot_helper import print_progress_bar
from simulator.simulation_helper import get_environment_simulation, get_virus_simulation_t0


# This scenario is a lockdown loosening every DAYS_WAIT_FOR_LOCKDOWN_REMOVAL after the last new case
def launch_run():
    print('Preparing environment...')
    env_dic = get_environment_simulation(params[nindividual_key], params[store_per_house_key],
                                         params[store_preference_key], params[nb_1d_block_key], params[remote_work_key])

    stats = np.zeros((params[nrun_key], params[nday_key], 7))
    print_progress_bar(0, params[nrun_key] * params[nday_key], prefix='Progress:', suffix='Complete', length=50)
    for r in range(params[nrun_key]):

        params[store_preference_key] = 0.95
        params[remote_work_key] = 0.98
        params[house_infect_key] = 0.5
        params[work_infection_key] = 0.001
        params[store_infection_key] = 0.002
        params[transport_infection_key] = 0.001

        lockdown_min_delay = 0

        virus_dic = get_virus_simulation_t0(params[nindividual_key], params[innoculation_number_key],
                                            params[contagion_bounds_key], params[hospitalization_bounds_key],
                                            params[death_bounds_key], params[immunity_bounds_key])
        for i in range(params[nday_key]):
            print_progress_bar(r * params[nday_key] + i + 1, params[nrun_key] * params[nday_key],
                               prefix='Progress:', suffix='Complete', length=50)
            propagate_to_houses(env_dic, virus_dic, params[house_infect_key])
            if not is_weekend(i):
                propagate_to_transportation(env_dic, virus_dic, params[transport_infection_key])
                propagate_to_workplaces(env_dic, virus_dic, params[work_infection_key])
            if is_weekend(i):
                propagate_to_stores(env_dic, virus_dic, params[store_infection_key])
            increment_pandemic_1_day(env_dic, virus_dic)
            stats[r][i][0], stats[r][i][1], stats[r][i][2], stats[r][i][3], stats[r][i][4], stats[r][i][5] = \
                get_pandemic_statistics(virus_dic)
            stats[r][i][6] = measure_lockdown_strength(params)

            lockdown_min_delay += 1
            if stats[r][i][5] == 0 and lockdown_min_delay >= 7:
                lockdown_min_delay = 0
                soften_lockdown(params)
                soften_lockdown(params)
            elif stats[r][i][5] >= 5 and lockdown_min_delay >= 7:
                lockdown_min_delay = 0
                tighten_lockdown(params)
                tighten_lockdown(params)

    return stats
