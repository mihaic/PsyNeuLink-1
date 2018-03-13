import ray

from typing import Dict, List, Union

import numpy as np

import psyneulink as pnl

__all__ = [
    "RayTransferMechanismWrapper",
]


@ray.remote
class RayTransferMechanismWrapper():
    def __init__(self, function: pnl.Function = None,
                 function_params: Dict = None
                 ) -> None:
        self._mechanism = pnl.TransferMechanism(function=function,
                                                params={pnl.FUNCTION_PARAMS:
                                                        function_params})

    def mechanism(self) -> str:
        return str(self._mechanism)

    def execute(self, input: Union[List, np.ndarray]) -> List:
        return self._mechanism.execute()
