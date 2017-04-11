#
# Created by Aman LaChapelle on 4/11/17.
#
# pytorch-rwa
# Copyright (c) 2017 Aman LaChapelle
# Full license at pytorch-rwa/LICENSE.txt
#

import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as Funct


class RWA(nn.Module):
    def __init__(self,
                 num_features,
                 num_cells,
                 num_classes,
                 activation=Funct.tanh):

        super(RWA, self).__init__()

        self.num_features = num_features
        self.num_cells = num_cells
        self.num_classes = num_classes
        self.activation = activation

        self.s0 = nn.Parameter(torch.FloatTensor(self.num_cells).normal_(0.0, 1.0))

        self.g = nn.Linear(self.num_features + self.num_cells, self.num_cells)
        self.u = nn.Linear(self.num_features, self.num_cells)
        self.a = nn.Linear(self.num_features + self.num_cells, self.num_cells, bias=False)
        self.o = nn.Linear(self.num_cells, self.num_classes)

    def init_internal(self, batch_size):
        n = Variable(torch.zeros(batch_size, self.num_cells))
        d = Variable(torch.zeros(batch_size, self.num_cells))
        h = Variable(torch.zeros(batch_size, self.num_cells))
        h = h + self.activation(self.s0.repeat(batch_size, 1))
        a_max = Variable(torch.ones(batch_size, self.num_cells) * -1e38)  # start with very negative number
        return n, d, h, a_max

    def forward(self, x, n, d, h, a_max):  # x has shape (batch x steps x num_features)
        for x_t in torch.unbind(x, 1):
            xh_join = torch.cat([x_t, h], 1)
            u_t = self.u(x_t)
            g_t = self.g(xh_join)
            a_t = self.a(xh_join)

            z_t = u_t * Funct.tanh(g_t)

            a_newmax = torch.max(a_max, a_t)
            exp_diff = torch.exp(a_max - a_newmax)
            exp_scaled = torch.exp(a_t - a_newmax)

            n_t = n * exp_diff + z_t * exp_scaled
            d_t = d * exp_diff + exp_scaled

            h = self.activation(n_t / d_t)

        out = self.o(h)
        return out



if __name__ == "__main__":
    rwa = RWA(10, 250, 2)
    n, d, h, a_max = rwa.init_internal(4)
    x = Variable(torch.rand(4, 30, 10))
    rwa(x, n, d, h, a_max)



