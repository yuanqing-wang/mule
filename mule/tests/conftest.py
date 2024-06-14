import pytest

@pytest.fixture
def caffeine():
    # use openff toolkit to construct a openmm caffeine system
    from openff.toolkit.topology import Molecule
    from openff.toolkit.typing.engines.smirnoff import ForceField
    molecule = Molecule.from_smiles("CN1C=NC2=C1C(=O)N(C(=O)N2C)C")
    forcefield = ForceField("openff-2.0.0.offxml")
    system = forcefield.create_openmm_system(molecule.to_topology())

    # initialzie the simulation object
    from openmm.app import Simulation
    from openmmtools.integrators import DummyIntegrator
    dummy_integrator = DummyIntegrator()
    simulation = Simulation(
        system=system, 
        topology=molecule.to_topology().to_openmm(),
        integrator=dummy_integrator,
    )

    # assign positions
    import openmm
    molecule.generate_conformers(n_conformers=1)
    conformer = molecule.conformers[0].to_openmm()
    simulation.context.setPositions(conformer)

    return simulation


if __name__ == "__main__":
    caffeine()


