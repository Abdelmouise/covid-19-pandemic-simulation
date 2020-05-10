import random
import sys
import time
import json
import os
import streamlit as st
from scenario.example import sc1_simple_lockdown_removal, sc2_yoyo_lockdown_removal, sc0_base_lockdown, \
    scx_base_just_a_flu, sc3_loose_lockdown, sc4_rogue_citizen, sc5_rogue_neighborhood, sc6_travelers
from simulator.constants.keys import scenario_id_key, random_seed_key, draw_graph_key
from simulator.helper.parser import get_parser
from simulator.helper.plot_app import chose_draw_plot
from simulator.helper.simulation import get_default_params
from simulator.helper.environment import get_environment_simulation


def get_parametres(params):
    # Get general parametres

    st.sidebar.markdown("# Paramètres généraux")
    params['N_INDIVIDUALS'] = st.sidebar.slider("Choisissez le nombre de personnes", 100, 35000, 1000)
    params['N_DAYS'] = st.sidebar.slider("Choisissez la durée en jour", 30, 365, 180)
    params['NRUN'] = st.sidebar.slider("N run", 1, 50, 20)

    # Get probablities

    st.sidebar.markdown("# Probabilités d'infection")
    params['PROB_HOUSE_INFECTION'] = st.sidebar.slider("Probability of house infection", 0.0, 1.0, 0.5)
    params['PROB_STORE_INFECTION'] = st.sidebar.slider("Probability of store infection", 0.0, 1.0, 0.02)
    params['PROB_WORK_INFECTION'] = st.sidebar.slider("Probability of workplace infection", 0.0, 1.0, 0.01)
    params['PROB_TRANSPORT_INFECTION'] = st.sidebar.slider("Probability of public transportation infection", 0.0, 1.0,
                                                           0.01)

    # Plot all graphs
    params["DRAW_GRAPH"] = ['exa', 'pop', 'summ', 'lock', 'hos', 'new', 'R0']


def get_description(scenario_id, data):
    for scenario in data:
        if (scenario["scneario_id"] == scenario_id):
            return scenario["description"]


if __name__ == '__main__':
    with open('scenario_desctiption.json', 'r', encoding='utf-8') as json_file:
        data_descrpition = json.load(json_file)
    params = get_default_params()
    random.seed(params[random_seed_key])

    t_start = time.time()

    st.title("Best et worst case scénarios pour un déconfinement de pandémie")
    st.sidebar.title("Scénarios")
    app_mode = st.sidebar.selectbox("choisissez un scénario",
                                    ["Scénario X - Ce n’est qu’une grippe",
                                     "Scénario 0 - Éradication",
                                     "Scénario 1 - Déconfinement one shot",
                                     "Scénario 2 - Déconfinement yo-yo",
                                     "Scénario 3 - Immunité collective",
                                     "Scénario 4 - Incivilités individuelles",
                                     "Scénario 5 - Incivilités sociales",
                                     "Scénario 6 - Les cas importés"])

    get_parametres(params)

    env_dic = get_environment_simulation(params)
    if app_mode == "Scénario X - Ce n’est qu’une grippe":
        params[scenario_id_key] = -1
        st.markdown(get_description(-1 , data_descrpition))
        stats_result = scx_base_just_a_flu.launch_run(params, env_dic)
    elif app_mode == "Scénario 0 - Éradication":  # Total lockdown
        params[scenario_id_key] = 0
        st.markdown(get_description(0, data_descrpition))
        stats_result = sc0_base_lockdown.launch_run(params, env_dic)
    elif app_mode == "Scénario 1 - Déconfinement one shot":  # Lockdown removal after N days
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [14.0]
        params[scenario_id_key] = 1
        stats_result = sc1_simple_lockdown_removal.launch_run(params, env_dic)
    elif app_mode == "Scénario 2 - Déconfinement yo-yo":  # Yoyo lockdown removal
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [7.0, 1.0, 2.0]
        params[scenario_id_key] = 2
        st.markdown(get_description(2, data_descrpition))
        stats_result = sc2_yoyo_lockdown_removal.launch_run(params, env_dic)
    elif app_mode == "Scénario 3 - Immunité collective":  # Yoyo lockdown removal
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [0.0]
        params[scenario_id_key] = 3
        st.markdown(get_description(3, data_descrpition))
        stats_result = sc3_loose_lockdown.launch_run(params, env_dic)
    elif app_mode == "Scénario 4 - Incivilités individuelles":  # Rogue citizen
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [1.0, 10.0]
        params[scenario_id_key] = 4
        st.markdown(get_description(4, data_descrpition))
        stats_result = sc4_rogue_citizen.launch_run(params, env_dic)
    elif app_mode == "Scénario 5 - Incivilités sociales":  # Rogue block
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [4.0, 10.0]
        params[scenario_id_key] = 5
        st.markdown(get_description(5, data_descrpition))
        stats_result = sc5_rogue_neighborhood.launch_run(params, env_dic)
    elif app_mode == "Scénario 6 - Les cas importés":  # Rogue block
        params['ADDITIONAL_SCENARIO_PARAMETERS'] = [5.0]
        params[scenario_id_key] = 6
        st.markdown(get_description(6, data_descrpition))
        stats_result = sc6_travelers.launch_run(params, env_dic)
    else:
        sys.exit(0)
    print("It took : %.2f seconds" % (time.time() - t_start))

    chose_draw_plot(params[draw_graph_key], stats_result)
