
def test_lbfgs(caffeine):
    from mule.action import LBFGS
    from mule.simulation import Simulation
    simulation = Simulation(caffeine)
    lbfgs = LBFGS()
    simulation = lbfgs(simulation)