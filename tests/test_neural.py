"""Unit tests for zkai.neural primitives."""

import pytest
import torch
from zkai.neural.tensor import Tensor
from zkai.neural.parameter import Parameter, Neuron
from zkai.neural.module import Sequential, NeuralNetwork
from zkai.neural.layers import Linear, Dense, Dropout
from zkai.neural.activations import ReLU, GELU, Sigmoid, Softmax
from zkai.neural.losses import MSELoss, CrossEntropyLoss
from zkai.neural.optimizers import Adam


def test_tensor_ops():
    t1 = Tensor([1.0, 2.0, 3.0])
    t2 = Tensor([4.0, 5.0, 6.0])
    res = t1 + t2
    assert res.shape == (3,)
    assert list(res.numpy()) == [5.0, 7.0, 9.0]


def test_neuron():
    n = Neuron(input_dim=4, activation="sigmoid")
    x = Tensor([[1.0, 2.0, 3.0, 4.0]])
    out = n(x)
    assert out.shape == (1, 1)


def test_linear_layer():
    linear = Linear(in_features=10, out_features=5)
    x = Tensor(torch.randn(2, 10))
    out = linear(x)
    assert out.shape == (2, 5)


def test_sequential_network():
    net = NeuralNetwork([
        Linear(10, 20),
        ReLU(),
        Linear(20, 1),
    ])
    x = Tensor(torch.randn(4, 10))
    out = net(x)
    assert out.shape == (4, 1)


def test_optimizer_and_loss():
    net = NeuralNetwork([Linear(2, 1)])
    optimizer = Adam(net.parameters(), lr=0.01)
    loss_fn = MSELoss()

    x = Tensor([[1.0, 2.0]])
    y = Tensor([[5.0]])

    out = net(x)
    loss = loss_fn(out, y)
    loss.backward()
    optimizer.step()
    assert loss.item() > 0
