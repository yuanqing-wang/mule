from abc import abstractmethod
from typing import Tuple
from .simulation import Simulation
import torch

class Action:
    def _analyaze_simulation(self, simulation):
        """Get the positions and velocities of the simulation."""
        # grab the current state
        state = simulation.simulation.context.getState(
            getPositions=True,
            getVelocities=True,
            getEnergy=True,
        )

        positions, velocities, energy = (
            state.getPositions(), 
            state.getVelocities(),
            state.getPotentialEnergy(),
        )
        positions = torch.tensor(positions._value)
        velocities = torch.tensor(velocities._value)
        energy = torch.tensor(state.getPotentialEnergy()._value)
        return positions, velocities, energy
    
    @abstractmethod
    def _call(
            self,
            simulation: Simulation,
    ) -> Simulation:
        """Perform the action."""
        raise NotImplementedError
    
    def __call__(
            self,
            simulation: Simulation,
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Perform the action and record the state."""
        simulation = self._call(simulation)
        positions, velocities, energy = self._analyaze_simulation(simulation)
        simulation.restore()
        return positions, velocities, energy
    
class LBFGS(Action):    
    def _call(
        self,
        simulation: Simulation,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        simulation.simulation.minimizeEnergy()
        return simulation