def test_egnn():
    from mule.models import EGNNModel
    import torch
    import dgl
    NUM_NODES = 5
    IN_FEATURES = 10
    HIDDEN_FEATURES = 20
    DEPTH = 3
    model = EGNNModel(IN_FEATURES, HIDDEN_FEATURES, DEPTH)
    g = dgl.graph(([0, 1, 2, 3, 4], [1, 2, 3, 4, 0]))
    h = torch.randn(NUM_NODES, IN_FEATURES)
    x = torch.randn(NUM_NODES, IN_FEATURES)
    v = model(g, h, x)
    print(v)


