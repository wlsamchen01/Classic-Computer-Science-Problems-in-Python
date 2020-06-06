from __future__ import annotations
from typing import List, Callable, TypeVar, Tuple
from functools import reduce
from layer import Layer
from util import sigmoid, derivatie_sigmoid

T = TypeVar("T")  # output type of interpretation of neural network


class Network:
    def __init__(
        self,
        layer_structure: List[int],
        learning_rate: float,
        activation_function: Callable[[float], float] = sigmoid,
        derivative_activation_function: Callable[[float], float] = derivatie_sigmoid,
    ) -> None:
        if len(layer_structure) < 3:
            raise ValueError(
                "Error: Should be at least 3 layers (1 input, \
                1 hidden, 1 output"
            )
        # create a list to add layers
        self.layers: List[Layer] = []
        # input layer
        # it has None previous layer, layer_structure[0] neurons etc
        input_layer: Layer = Layer(
            None,
            layer_structure[0],
            learning_rate,
            activation_function,
            derivative_activation_function,
        )
        self.layers.append(input_layer)

        # hidden layers and output layer
        # we use enumerate to get the index of the previous layer
        for previous, num_neurons in enumerate(layer_structure[1::]):
            next_layer = Layer(
                self.layers[previous],
                num_neurons,
                learning_rate,
                activation_function,
                derivative_activation_function,
            )
            self.layers.append(next_layer)

    # We use reduce() in output() to pass signals from one layer to the next repeatedly
    # through the whole network
    def outputs(self, input: List[float]) -> List[float]:
        return reduce(lambda inputs, layer: layer.outputs(inputs), self.layers, input)

    # The backpropagate() method is responsible for computing deltas for every neuron.
    # Figure out each neuron's changes based on the errors of the output
    # versus the expected outcome
    def backpropagate(self, expected: List[float]) -> None:
        # calculate delta for output layer neurons
        last_layer: int = len(self.layers) - 1
        # The .calculate_deltas_for_output_layer method takes the expected
        # (final) output as input
        self.layers[last_layer].calculate_deltas_for_output_layer(expected)
        # calculated delta for hiddern layers in reverse order
        for l in range(last_layer - 1, 0, -1):
            # The .calculate_deltas_for_hidden_layer method takes the next
            # layer as input
            self.layers[l].calculate_deltas_for_hidden_layer(self.layers[l + 1])

    # backpropagate() doesn't actually change any weights
    # this function uses the deltas calculated in backpropagate() to
    # actually make changes to the weights
    def update_weights(self) -> None:
        for layer in self.layers[1:]:  # skip input layer
            for neuron in layer.neurons:
                for w in range(len(neuron.weights)):
                    neuron.weights[w] = neuron.weights[w] + (
                        neuron.learning_rate
                        * (layer.previous_layer.output_cache[w])
                        * neuron.delta
                    )

    # train() uses the results of outputs() run over many inputs and compared
    # against expected outputs to feed backpropagate() and update_weights()
    def train(self, inputs: List[List[float]], expecteds: List[List[float]]) -> None:
        for location, xs in enumerate(inputs):
            # expected output list
            ys: List[float] = expecteds[location]
            # calculate expected output
            outs: List[float] = self.outputs(xs)  # unused variable?
            self.backpropagate(ys)
            self.update_weights()

    # for generalised results that require classification
    # this function will return the correct number of trials
    # and the percentage correct number of trials
    # interpret_output() must take the floating-point numbers it gets as
    # output from the network and convert them into something comparable to
    # the expected outputs. It is a custom function specific to a data set.
    def validate(
        self,
        inputs: List[[List[float]]],
        expecteds: List[T],
        interpret_output: Callable[[List[float]], T],
    ) -> Tuple[int, int, float]:
        # count of corrects, initialised to 0
        correct: int = 0
        for input, expected in zip(inputs, expecteds):
            result: T = interpret_output(self.outputs(input))
            if result == expected:
                correct += 1
        percentage: float = correct / len(inputs)
        return correct, len(inputs), percentage
