import torch
import openmm
import dgl

def graph_from_openmm_system(
        system: openmm.System,
):
    """Convert an OpenMM system to a graph."""
    graph = dgl.DGLGraph()
    graph.add_nodes(system.getNumParticles())
    for i in range(system.getNumParticles()):
        for j in range(i+1, system.getNumParticles()):
            if system.isVirtualSite(i) or system.isVirtualSite(j):
                continue
            graph.add_edge(i, j)
    return graph


class System(torch.nn.Module):
    def __init__(
            self,
            system: openmm.System,
    ):
        super().__init__()
        self.system = system
