from abc import abstractmethod
from .simulation import Simulation

class Action:
    @abstractmethod
    def __call__(
        self,
        simulation: Simulation,
    ) -> Simulation:
        raise NotImplementedError
    
class LBFGS(Action):    
    def __call__(
        self,
        simulation: Simulation,
    ) -> Simulation:
        simulation.simulation.minimizeEnergy()
        return simulation