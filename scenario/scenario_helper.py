import math
import numpy as np

from simulator.parameters import *


def get_zero_stats():
    return {
        "hea": np.zeros((params[nrun_key], params[nday_key])),
        "inf": np.zeros((params[nrun_key], params[nday_key])),
        "hos": np.zeros((params[nrun_key], params[nday_key])),
        "dea": np.zeros((params[nrun_key], params[nday_key])),
        "imm": np.zeros((params[nrun_key], params[nday_key])),
        "iso": np.zeros((params[nrun_key], params[nday_key])),
        "R0": np.zeros((params[nrun_key], params[nday_key])),
        "new": np.zeros((params[nrun_key], params[nday_key])),
        "loc": np.zeros((params[nrun_key], params[nday_key]))
    }


def soften_full_lockdown(params_arg):
    params_arg[store_preference_key] = math.pow(params_arg[store_preference_key], 2)
    params_arg[remote_work_key] = math.pow(params_arg[remote_work_key], 2)
    soften_propagation_lockdown(params_arg)


def tighten_full_lockdown(params_arg):
    params_arg[store_preference_key] = math.sqrt(params_arg[store_preference_key])
    params_arg[remote_work_key] = math.sqrt(params_arg[remote_work_key])
    tighten_propagation_lockdown(params_arg)


def soften_propagation_lockdown(params_arg):
    params_arg[house_infect_key] = math.sqrt(params_arg[house_infect_key])
    params_arg[transport_infection_key] = math.sqrt(params_arg[transport_infection_key])
    params_arg[work_infection_key] = math.sqrt(params_arg[work_infection_key])
    params_arg[store_infection_key] = math.sqrt(params_arg[store_infection_key])


def tighten_propagation_lockdown(params_arg):
    params_arg[house_infect_key] = math.pow(params_arg[house_infect_key], 2)
    params_arg[transport_infection_key] = math.pow(params_arg[transport_infection_key], 2)
    params_arg[work_infection_key] = math.pow(params_arg[work_infection_key], 2)
    params_arg[store_infection_key] = math.pow(params_arg[store_infection_key], 2)


def measure_lockdown_strength(params_arg):
    return 1/(math.log(1+params_arg[house_infect_key]) + math.log(1+params_arg[transport_infection_key]) +
              math.log(1+params_arg[work_infection_key]) + math.log(1+params_arg[store_infection_key]) +
              math.log(2-params_arg[store_preference_key]) + math.log(2-params_arg[remote_work_key]))
