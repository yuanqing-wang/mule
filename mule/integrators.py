import openmm as mm
from openmm import unit


class ReversedVelocityVerletIntegrator(mm.CustomIntegrator):
    def __init__(self, timestep=1.0 * unit.femtoseconds):
        """Construct a velocity Verlet integrator.

        Parameters
        ----------
        timestep : np.unit.Quantity compatible with femtoseconds, default: 1*unit.femtoseconds
           The integration timestep.

        """

        super().__init__(timestep)
        self.addPerDofVariable("x1", 0)
        self.addUpdateContextState()
        self.addComputePerDof("x1", "x")
        self.addConstrainPositions()

        self.addComputePerDof("v", "v-0.5*dt*f/m-(x-x1)/dt")
        self.addComputePerDof("x1", "x")
        self.addComputePerDof("x", "x-dt*v")
        self.addComputePerDof("v", "v-0.5*dt*f/m")
        self.addConstrainVelocities()



