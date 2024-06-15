import openmm as mm
from openmm import unit


class ReversibleVelocityVerletIntegrator(mm.CustomIntegrator):
    reverse = False
    def __init__(self, timestep=1.0 * unit.femtoseconds):
        """Construct a velocity Verlet integrator.

        Parameters
        ----------
        timestep : np.unit.Quantity compatible with femtoseconds, default: 1*unit.femtoseconds
           The integration timestep.

        """

        super().__init__(timestep)
        if self.reverse:
            self._backward()
        else:
            self._forward()
        
    def _forward(self):
        self.addPerDofVariable("x1", 0)
        self.addUpdateContextState()
        self.addComputePerDof("v", "v+0.5*dt*f/m")
        self.addComputePerDof("x", "x+dt*v")
        self.addComputePerDof("x1", "x")
        self.addComputePerDof("v", "v+0.5*dt*f/m+(x-x1)/dt")
        self.addConstrainPositions()
        self.addConstrainVelocities()

    def _backward(self):
        self.addPerDofVariable("x1", 0)
        self.addUpdateContextState()
        self.addComputePerDof("v", "v-0.5*dt*f/m-(x-x1)/dt")
        self.addComputePerDof("x1", "x")
        self.addComputePerDof("x", "x-dt*v")
        self.addComputePerDof("v", "v-0.5*dt*f/m")
        self.addConstrainPositions()
        self.addConstrainVelocities()



