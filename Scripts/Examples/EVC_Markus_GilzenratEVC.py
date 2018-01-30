import numpy as np
import psyneulink as pnl

# baseSaliency = 2.75;
# % base reward
# baseReward = 5;
#
# % other parameters
# T0 = 0.2;
# c = 0.8;
# thresh = 1.0;
# costParam1 = 0.75;
# reconfCostParam1 = 0;
#
# % set number of trials
# EVCSim.nTrials = 92;


# Control Parameters
signalSearchRange = np.arange(0.8, 2.0, 0.2)


# test_mech = pnl.TransferMechanism(size=3)

# Stimulus Mechanisms
Target_Stim = pnl.TransferMechanism(name='Target Stimulus', function=pnl.Linear)
Flanker_Stim = pnl.TransferMechanism(name='Flanker Stimulus', function=pnl.Linear)

# Processing Mechanisms (Control)
Target_Rep = pnl.TransferMechanism(name='Target Representation',
                                   function=pnl.Linear(
                                       slope=(1.0, pnl.ControlProjection(
                                           control_signal_params={
                                               pnl.ALLOCATION_SAMPLES: signalSearchRange}))))
Target_Rep.set_log_conditions('value') # Log Target_Rep

Flanker_Rep = pnl.TransferMechanism(name='Flanker Representation',
                                    function=pnl.Linear(
                                        slope=(1.0, pnl.ControlProjection(
                                            control_signal_params={
                                                pnl.ALLOCATION_SAMPLES: signalSearchRange}))))
Flanker_Rep.set_log_conditions('value') # Log Flanker_Rep

# Processing Mechanism (Automatic)
Automatic_Component = pnl.TransferMechanism(name='Automatic Component',function=pnl.Linear)

# Decision Mechanisms
Decision = pnl.DDM(function=pnl.BogaczEtAl(
        drift_rate=(1.0),
        threshold=(1.0),
        noise=(0.8),
        starting_point=(0),
        t0=0.2
    ),name='Decision',
    output_states=[
        pnl.DECISION_VARIABLE,
        pnl.RESPONSE_TIME,
        pnl.PROBABILITY_UPPER_THRESHOLD,
        {
            pnl.NAME: 'OFFSET RT',
            pnl.INDEX: 2,
            pnl.CALCULATE: pnl.Linear(0, slope=0.3, intercept=1).function
        }
    ],) #drift_rate=(1.0),threshold=(0.2645),noise=(0.5),starting_point=(0), t0=0.15
Decision.set_log_conditions('DECISION_VARIABLE')
# Decision.loggable_items

# Outcome Mechanisms:
Reward = pnl.TransferMechanism(name='Reward')

# Processes:
TargetControlProcess = pnl.Process(
    default_variable=[0],
    pathway=[Target_Stim, Target_Rep, Decision],
    name='Target Control Process'
)

FlankerControlProcess = pnl.Process(
    default_variable=[0],
    pathway=[Flanker_Stim, Flanker_Rep, Decision],
    name='Flanker Control Process'
)

TargetAutomaticProcess = pnl.Process(
    default_variable=[0],
    pathway=[Target_Stim, Automatic_Component, Decision],
    name='Target Automatic Process'
)

FlankerAutomaticProcess = pnl.Process(
    default_variable=[0],
    pathway=[Flanker_Stim, Automatic_Component, Decision],
    name='Flanker1 Automatic Process'
)

RewardProcess = pnl.Process(
    default_variable=[0],
    pathway=[Reward, test_mech],
    name='RewardProcess'
)


# System:
mySystem = pnl.System(processes=[
        TargetControlProcess,
        FlankerControlProcess,
        TargetAutomaticProcess,
        FlankerAutomaticProcess,
        RewardProcess
    ],
    controller=pnl.EVCControlMechanism,
    enable_controller=True,
    monitor_for_control=[
        # (test_mech, None, None, np.ones((3,1))),
        Reward,
        Decision.PROBABILITY_UPPER_THRESHOLD,
        ('OFFSET RT', 1, -1),
    ],
    name='EVC Markus System'
)

# Show characteristics of system:
mySystem.show()
# mySystem.controller.show()

# Show graph of system
mySystem.show_graph(show_control=True,
                    show_dimensions=True)




#Markus: incongruent trial weights:

# f = np.array([1,1])
# W_inc = np.array([[1.0, 0.0],[0.0, 1.5]])
# W_con = np.array([[1.0, 0.0],[1.5, 0.0]])


# generate stimulus environment
nTrials = 5
targetFeatures = [1.5]
flankerFeatures_inc = [-1.5]
# flankerFeatures_con = [1.5, 0]
reward = [100, 100, 100]


targetInputList = targetFeatures
flankerInputList = flankerFeatures_inc
rewardList = reward



stim_list_dict = {
    Target_Stim: targetInputList,
    Flanker_Stim: flankerInputList,
    Reward: rewardList

}

mySystem.run(num_trials=nTrials,inputs=stim_list_dict)

# Flanker_Rep.log.print_entries()
# Target_Rep.log.print_entries()
Decision.log.print_entries()

