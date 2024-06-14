import torch
import openmm
from dataclasses import dataclass

@dataclass
class State:
    openmm_state: openmm.State

    @property
    def positions(self):
        return torch.tensor(
            self.openmm_state.getPositions()._value
        )
    
    @property
    def velocities(self):
        return torch.tensor(
            self.openmm_state.getVelocities()._value
        )
    
    @property
    def energy(self):
        return torch.tensor(
            self.openmm_state.getPotentialEnergy()._value
        )
