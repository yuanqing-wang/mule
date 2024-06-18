def test_invertibility():
    # use openff toolkit to construct a openmm caffeine system
    from openff.toolkit.topology import Molecule
    from openff.toolkit.typing.engines.smirnoff import ForceField
    molecule = Molecule.from_smiles("CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
    forcefield = ForceField("openff-2.0.0.offxml")
    system = forcefield.create_openmm_system(molecule.to_topology())

    # initialzie the simulation object
    from openmm.app import Simulation
    from openmmtools.integrators import VelocityVerletIntegrator
    from mule.integrators import ReversedVelocityVerletIntegrator
    integrator = VelocityVerletIntegrator()
    simulation = Simulation(
        system=system, 
        topology=molecule.to_topology().to_openmm(),
        integrator=integrator,
    )

    # assign positions
    import openmm
    molecule.generate_conformers(n_conformers=1)
    conformer = molecule.conformers[0].to_openmm()
    simulation.context.setPositions(conformer)
    simulation.minimizeEnergy()

    # assign velocities
    simulation.context.setVelocitiesToTemperature(350)
    state = simulation.context.getState(
        getVelocities=True,
        getPositions=True,
    )
    x0 = state.getPositions()
    v0 = state.getVelocities()

    integrator.step(100)
    state = simulation.context.getState(
        getVelocities=True,
        getPositions=True,
    )

    x1 = state.getPositions()
    v1 = state.getVelocities()

    integrator = ReversedVelocityVerletIntegrator()
    simulation = Simulation(
        system=system, 
        topology=molecule.to_topology().to_openmm(),
        integrator=integrator,
    )
    simulation.context.setPositions(x1)
    simulation.context.setVelocities(v1)
    simulation.step(100)

    state = simulation.context.getState(
        getVelocities=True,
        getPositions=True,
    )
    x2 = state.getPositions()
    v2 = state.getVelocities()

    import numpy as np
    x0 = np.array(x0._value)
    x2 = np.array(x2._value)
    v0 = np.array(v0._value)
    v2 = np.array(v2._value)
    assert np.allclose(x0, x2, rtol=1e-2, atol=1e-2)
    assert np.allclose(v0, v2, rtol=1e-2, atol=1e-2)







