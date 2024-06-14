from dataclasses import dataclass
import torch
import openmm
import dgl
from openmm.app.topology import Topology

def graph_from_openmm_topology(
        topology: Topology,
):
    """Convert an OpenMM system to a graph."""
    # initialize a graph
    graph = dgl.DGLGraph()

    # make the particles into nodes
    graph.add_nodes(topology.getNumAtoms())
    
    # write masses into the graph
    masses = torch.tensor(
        [
            atom.element._mass._value for atom in topology.atoms()
        ]
    )
    graph.ndata['mass'] = masses

    # make the bonds into edges
    for bond in topology.bonds():
        graph.add_edges(
            bond.atom1.index,
            bond.atom2.index,
        )

    return graph

@dataclass
class Simulation:
    simulation: openmm.app.Simulation

    def __post_init__(self):
        self.graph = graph_from_openmm_topology(
            self.simulation.topology,
        )



