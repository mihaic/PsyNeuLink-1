import numpy as np
import pytest

from psyneulink.components.functions.function import SimpleIntegrator, Linear, NormalDist
from psyneulink.components.mechanisms.processing.transfermechanism import TransferMechanism
from psyneulink.components.mechanisms.processing.integratormechanism import IntegratorMechanism
from psyneulink.library.mechanisms.processing.transfer.recurrenttransfermechanism import RecurrentTransferMechanism
from psyneulink.components.mechanisms.adaptive.control.controlmechanism import ControlMechanism
from psyneulink.components.mechanisms.processing.objectivemechanism import ObjectiveMechanism
from psyneulink.components.process import Process
from psyneulink.components.system import System

class TestOutputStateAfterInitializationRun:

    def test_transfer_mech_non_zero_defaults(self):
        T = TransferMechanism(
            name='T',
            default_variable=[1, 2, 3, 4],
            integrator_mode=False
        )

        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(T.output_state.value, [1.0,2.0,3.0,4.0], atol=1e-08)

    def test_transfer_mech_noise(self):
        T = TransferMechanism(
            name='T',
            default_variable=[0, 0, 0, 0],
            noise=NormalDist().function,
            integrator_mode=False
        )
        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(T.output_state.value, [0.40015721, 0.97873798, 2.2408932, 1.86755799], atol=1e-08)

    def test_transfer_mech_noise_process_system(self):
        T = TransferMechanism(
            name='T',
            default_variable=[0, 0, 0, 0],
            noise=NormalDist().function,
            integrator_mode=False
        )

        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(T.output_state.value, [0.40015721, 0.97873798, 2.2408932, 1.86755799], atol=1e-08)

        # Confirming that the output state value does not change when a process is created
        P = Process(pathway=[T])
        np.testing.assert_allclose(T.output_state.value, [0.40015721, 0.97873798, 2.2408932, 1.86755799], atol=1e-08)

        # Confirming that the output state value does not change when a system is created
        S = System(processes=[P])
        np.testing.assert_allclose(T.output_state.value, [0.40015721, 0.97873798, 2.2408932, 1.86755799], atol=1e-08)

    def test_transfer_mech_intercept(self):
        T = TransferMechanism(
            name='T',
            default_variable=[0,0,0,0],
            integrator_mode=False,
            function=Linear(slope=2.0, intercept=5.0)
        )
        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(T.output_state.value, [5.0,5.0,5.0,5.0], atol=1e-08)

    def test_integrator_mech_accumulator(self):

        I = IntegratorMechanism(
            function=SimpleIntegrator(
                initializer=10.0,
                rate=5.0,
                offset=10,
            )
        )

        # returns:
        # (previous_value + (new_value * rate) + noise) + offset
        # (10.0 + (0.0*5.0) + 0.0) + 10.0 = 20.0

        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(I.output_state.value, [20.0], atol=1e-08)

    def test_overwrite_output_state_value(self):

        I = IntegratorMechanism(
            function=SimpleIntegrator(
                initializer=10.0,
                rate=5.0,
                offset=10,
            )
        )

        # returns:
        # (previous_value + (new_value * rate) + noise) + offset
        # (10.0 + (0.0*5.0) + 0.0) + 10.0 = 20.0

        # FIX: The output state value after construction is the output of the function on the default_variable
        np.testing.assert_allclose(I.output_state.value, [20.0], atol=1e-08)

        I.output_state.value = [10.0]
        np.testing.assert_allclose(I.output_state.value, [10.0], atol=1e-08)

    def test_recurrent_transfer_mech_non_zero_defaults(self):

        R = RecurrentTransferMechanism(
            name='R',
            default_variable=[1, 2, 3, 4],
            integrator_mode=False,
            function=Linear(slope=1.0, intercept=0.0)
        )

        P = Process(pathway=[R])
        S = System(processes=[P])

        # value of output state before execution
        np.testing.assert_allclose(R.output_state.value, [1.0, 2.0, 3.0, 4.0], atol=1e-08)

        S.run(inputs={R: [[1.0, 2.0, 3.0, 4.0]]})

        # R's recurrent proj sends R's previous output_state value (in this case, the val it returns on initialization)
        # When R goes to execute for the first time, its variable is:
        # recurrent + input = sum(1,2,3,4) + [1,2,3,4] = 10 + [1,2,3,4] = [11,12,13,14]
        # returns function([11,12,13,14]) = 1.0 * [11,12,13,14]  = [11,12,13,14]

        # value of output state after execution
        np.testing.assert_allclose(R.output_state.value, [11.0, 12.0, 13.0, 14.0], atol=1e-08)

    def test_recurrent_transfer_mech_non_zero_defaults_with_overwrite(self):

        R = RecurrentTransferMechanism(
            name='R',
            default_variable=[1, 2, 3, 4],
            integrator_mode=False,
            function=Linear(slope=1.0, intercept=0.0)
        )

        P = Process(pathway=[R])
        S = System(processes=[P])

        # value of output state before execution
        np.testing.assert_allclose(R.output_state.value, [1.0, 2.0, 3.0, 4.0], atol=1e-08)
        R.output_state.value = [0.0, 0.0, 0.0, 0.0]
        S.run(inputs={R: [[1.0, 2.0, 3.0, 4.0]]})

        # R's recurrent proj sends R's previous output_state value (in this case, we overwrote it to be all zeros)
        # When R goes to execute for the first time, its variable is:
        # recurrent + input = sum(0,0,0,0) + [1,2,3,4] = 0 + [1,2,3,4] = [1,2,3,4]
        # returns function([1,2,3,4]) = 1.0 * [1,2,3,4]  = [1,2,3,4]

        # value of output state after execution
        np.testing.assert_allclose(R.output_state.value, [1.0, 2.0, 3.0, 4.0], atol=1e-08)


    def test_control(self):
        A = TransferMechanism()
        B = TransferMechanism()
        C = ControlMechanism(
                objective_mechanism=ObjectiveMechanism(
                function=Linear,
                monitored_output_states=[(A, None, None, np.array([[0.3], [0.0]]))],
                input_states=[[0]],
                name='ObjectiveMechanism'
            ),

            # modulated_mechanisms=[B],
            name='ControlMech')

        P = Process(pathway=[A, B, C])
        S = System(processes=[P])

        # value of output state before execution
        # np.testing.assert_allclose(C.output_state.value, [1.0, 2.0, 3.0, 4.0], atol=1e-08)
        #
        # S.run(inputs={S: [[1.0, 2.0, 3.0, 4.0]]})

