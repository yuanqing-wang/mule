import abc
import torch
import dgl
from .action import Action

class Model(torch.nn.Module):
    def forward(
        self,
        g: dgl.DGLGraph,
        h: torch.Tensor,
        x: torch.Tensor,
    ) -> torch.Tensor:
        """Compute the loss."""
        return self.layers(g, h, x)
    
class EGNNModel(Model):
    def __init__(
            self,
            in_features: int,
            hidden_features: int,
            depth: int,
    ):
        super().__init__()
        self.layers = dgl.nn.Sequential(
            *[
                dgl.nn.EGNNConv(
                    in_size=in_features if idx == 0 else hidden_features,
                    hidden_size=hidden_features,
                    out_size=hidden_features,
                )
                for idx in range(depth)
            ]
        )
    
    def forward(
        self,
        g: dgl.DGLGraph,
        h: torch.Tensor,
        x: torch.Tensor,
    ) -> torch.Tensor:
        """Compute the loss."""
        _, x = self.layers(g, h, x)
        return x