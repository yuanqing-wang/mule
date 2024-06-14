
def test_graph_from_system():
    from mule.simulation import graph_from_openmm_topology
    import openmm
    from openmm.app import Topology
    import dgl
    import torch
    topology = Topology()
    chain = topology.addChain(id="chain")
    residue = topology.addResidue(name="residue", chain=chain)
    for idx in range(3):
        topology.addAtom(
            name=f"atom{idx}", 
            element=openmm.app.Element.getBySymbol('C'), 
            residue=residue,
        )
    
    topology.addBond(0, 1)
    topology.addBond(1, 2)

    graph = graph_from_openmm_topology(topology)
    assert isinstance(graph, dgl.DGLGraph)
    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2
    assert graph.has_edges_between(0, 1)
    assert graph.has_edges_between(1, 2)

    mass = graph.ndata['mass']
    assert torch.allclose(mass, torch.tensor([12.0108, 12.0108, 12.0108]))



