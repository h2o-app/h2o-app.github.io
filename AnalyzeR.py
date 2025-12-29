from random import randrange, uniform
from time import time
from math import exp


def run(data: list, inputs: list):
    # Run a neural network
    # Network is given via the [data] input
    # Inputs are given via the [inputs] input

    nodes: list = [[]]
    for i in inputs:
        nodes[0].append(i)
    for i in data[1]:
        nodes.append([0] * len(i))
    layerNum: int = 0
    for layer in data[1]:
        layerNum += 1
        nodeNum: int = -1
        for node in layer:
            nodeNum += 1
            nodeValue: float = node[0]
            weightNum: int = -1
            for weight in node[1:]:
                weightNum += 1
                nodeValue += nodes[layerNum - 1][weightNum] * weight
            nodes[layerNum][nodeNum] = _applyActFunc(nodeValue, data[0])
    return nodes[-1]


def _applyActFunc(value: float, func: str):
    # apply activation function to a node output
    match func:
        case "linear":
            return value

        case "relu":
            return max(0, value)
        case "leaky relu":
            return max(0.1 * value, value)

        case "binary":
            return 1 if value > 0 else 0
        case "sigmoid":
            return 1 / (1 + exp(-value))

        case _:
            raise Exception("Activation function invalid")


# Storing Networks


def exportString(data: list):
    # Converts data list into text format.
    output: str = str(data[0])
    for layer in data[1]:
        output += "|" + ",".join(" ".join(str(x) for x in node) for node in layer)
    return output


def importString(data: str):
    # Imports a neural network stored as text.
    layers: list = data.split("|")
    output: list = [str(layers[0]), []]
    del layers[0]
    for layer in layers:
        layerValue: list = []
        for node in layer.split(","):
            layerValue.append(list(map(float, node.split())))
        output[1].append(layerValue)
    return output


# Creating Networks


def new(inputs: list, actFunc: str = "linear"):
    # Creates new network with given data
    # Input format: list with layers
    # EX: [2,3,1] >>> two input nodes, one hidden layer with 3 nodes, 1 output node
    # EX: [4,6,5,6,2] >>> 4 inputs, 1 layer with 6 nodes,
    # another with 5, another with 6, and 2 outputs
    # Activation function can be set as well

    output: list = [actFunc, []]
    lastLayer: list = [0] * inputs[0]
    for layer in inputs[1:]:
        layerValue: list = []
        for _ in range(layer):
            nodeValue: list = []
            nodeValue.append(uniform(-1, 1))
            for _ in lastLayer:
                nodeValue.append(uniform(-1, 1))
            layerValue.append(nodeValue)
        output[1].append(layerValue)
        lastLayer = layerValue
    return output


def duplicate(data):
    return [data[0], [[node[:] for node in layer] for layer in data[1]]]


# Analyzing Networks


def accuracyTest(data: list, inputs: list):
    # takes in inputs and expected outputs
    # compares how similar the actual results are.
    accData: list = []
    for dataNumber in inputs:
        answers: list = dataNumber[1]
        outputs: list = run(data, dataNumber[0])
        for i in range(len(answers)):
            accData.append(abs(float(answers[i]) - outputs[i]))
    return sum(accData) / len(accData)


# Training Networks


def _defaultTrainingAlgorithm(data, _, accuracy):
    # Simple training algorithm that changes a random weight or bias.
    # Needs to be run thousands of times before seeing much change
    # Not efficient but a simple example.

    output: list = duplicate(data)
    layer: int = randrange(len(output[1]))
    node: int = randrange(len(output[1][layer]))
    value: int = randrange(len(output[1][layer][node]))
    output[1][layer][node][value] += uniform(-accuracy, accuracy)
    return output


class train:
    # Codeframe for training the AI.
    # main input is a list of many cases of inputs and expected outputs.
    # EX: [[[0],[0]],[[1],[1]]] would give two cases:
    # one with the input of 0 and expected output of 0
    # and another with the input of 1 and output of 1.
    # pre-included algorithm functions are available but custom functions can be used.
    def __init__(
        self,
        data: list,
        inputs: list,
        algorithm=_defaultTrainingAlgorithm,
        seconds: int = 5,
        log: bool = False,
    ):

        bestData: list = data
        bestAccuracy: float = accuracyTest(data, inputs)
        self.originalData: list = duplicate(data)
        self.originalAccuracy: float = bestAccuracy
        self.log: bool = log
        startTime: float = time()
        num: int = 0
        dataHistory: list = [bestData]
        accuracyHistory: list = [bestAccuracy]
        while time() - startTime < seconds:
            num += 1
            newData: list = algorithm(bestData, inputs, bestAccuracy)
            newAccuracy: float = accuracyTest(newData, inputs)
            if newAccuracy < bestAccuracy:
                bestData = newData
                bestAccuracy = newAccuracy
            if log:
                dataHistory.append(duplicate(newData))
                accuracyHistory.append(newAccuracy)

        self.data: list = bestData
        self.accuracy: float = bestAccuracy
        self.iterations: int = num
        self.runTime: float = time() - startTime
        if log:
            self.dataHistory: list = dataHistory
            self.accuracyHistory: list = accuracyHistory

    def __str__(self):
        return f"""
AnalyzeR_v3 Data Training Summary:\n
Iterations: {self.iterations}
Time Elapsed(seconds): {self.runTime}
Log mode: {self.log}\n
Data: {self.data}
Accuracy: {self.accuracy}\n
Original Data: {self.originalData}
Original Accuracy: {self.originalAccuracy}
"""


# User Tools


class neuralNetwork:
    # All-in-one class that stores a neural network
    # and preforms actions with it.
    def __init__(self, inputs: list, actFunc=None):
        if actFunc is None:
            self.data = duplicate(inputs)
        else:
            self.data = new(inputs, actFunc)

    def __call__(self, inputs: list):
        return run(self.data, inputs)

    def train(
        self,
        inputs: list,
        algorithm=_defaultTrainingAlgorithm,
        seconds: int = 5,
        log: bool = False,
    ):
        newData = train(self.data, inputs, algorithm, seconds, log)
        self.data = newData.data

    def exportString(self):
        return exportString(self.data)


def shellInterface():
    # Shell based interface that allows users to create,
    # train, manipulate, and observe a Neural Network
    # Through the python shell.
    def parseInput(inputs: str):
        output: list = []
        for case in inputs.split(","):
            output.append(
                [
                    [float(inData) for inData in case.split(".")[0].split()],
                    [float(outData) for outData in case.split(".")[1].split()],
                ]
            )
        return output

    print("AnalyzeR-v3 REPL Shell interface")
    while True:
        mode = input(
            "\033[34mNew\033[0m neural network or \033[34mImport\033[0m existing network? >>"
        ).lower()
        if mode == "new":
            print("\nSetup instructions:")
            print("Neuron count for each layer, separated by spaces")
            print("Example: '2 4 3 1' creates a neural network")
            print("with two input neurons and one output neuron, as well as")
            print("two hidden layers, one with four neurons and another with three.")
            print("at least two layers are required")
            while True:
                rawInput = input("\nSetup new neural network >>")
                try:
                    newInputs: list = list(map(int, rawInput.split()))
                    if any(x <= 0 for x in newInputs) or len(newInputs) < 2:
                        raise Exception("Invalid list data")
                    new(newInputs, "linear")
                except Exception as _:
                    print("Invalid input. Input should be a list of positive integers")
                    print("separated by spaces. 2 layers are required at minimum.")
                else:
                    break
            print("\nActivation function instructions:")
            print("Type in the name of a preset activation function.")
            print(
                "Examples include: \033[34mlinear\033[0m, \033[34mReLU\033[0m, and \033[34msigmoid\033[0m."
            )
            while True:
                actFunc = input("\nActivation function >>").lower()
                try:
                    _applyActFunc(0, actFunc)
                    database = new(newInputs, actFunc)
                except Exception as _:
                    print("Activation function not valid.")
                else:
                    break
            break
        if mode == "import":
            print("Import neural network data from string")
            while True:
                try:
                    database = importString(input("\nEnter string data >>"))
                except Exception as _:
                    print(
                        "Invalid string data. Only use data generated by AnalyzeR-v3."
                    )
                else:
                    break
            break
        else:
            print("Command \033[34m" + mode + "\033[0m Not Understood.")
    print("\nNeural network loaded.\n")
    while True:
        mode = input("Command[Use/Test/Train/Export/Exit] >>")
        match mode.lower():
            case "use":
                print("Enter neural network inputs")
                print("Inputs should be numbers separated by spaces.")
                inputs: list = [float(x) for x in input("Enter inputs >>").split()]
                try:
                    print(run(database, inputs))
                except Exception as _:
                    print(
                        "Input invalid. Inputs should be a list of integers or floats."
                    )
            case "test":
                print("Enter accuracy test inputs")
                print("Inputs should be a list of use cases separated by commas")
                print("each case have inputs and outputs, a period separating them")
                print("and each input or output list should be separated by spaces.")
                print("Example: '0 0.0,0 1.1,1 0.1,1 1.0'")
                print("This creates 4 cases,")
                print("the first represents both inputs of zero and an output of zero,")
                print(
                    "the second shows the first input at zero while the second is at one,"
                )
                print("with the expected answer being one,")
                print("and so on.")
                try:
                    inputs = parseInput(input("Enter accuracy test inputs >>"))
                    print(accuracyTest(database, inputs))
                except Exception as _:
                    print("Input invalid.")
            case "train":
                print("Enter training inputs")
                print("Inputs should be a list of use cases separated by commas")
                print("each case have inputs and outputs, a period separating them")
                print("and each input or output list should be separated by spaces.")
                print("Example: '0 0.0,0 1.1,1 0.1,1 1.0'")
                print("This creates 4 cases,")
                print("the first represents both inputs of zero and an output of zero,")
                print(
                    "the second shows the first input at zero while the second is at one,"
                )
                print("with the expected answer being one,")
                print("and so on.")
                try:
                    inputs = parseInput(input("Enter training inputs >>"))
                    print("Please wait...")
                    trainData = train(database, inputs)
                    print(trainData)
                    database = trainData.data
                except Exception as _:
                    print("Input invalid.")
            case "export":
                print("Export string:\n")
                print(exportString(database))
                print(
                    "\nCopy this data and paste it into AnalyzeR-v3 later to re-import."
                )
            case "exit":
                if input("Exit shell interface?[Yes/No] >>").lower() == "yes":
                    break
            case _:
                print("Command \033[34m" + mode.lower() + "\033[0m Not Understood.")


if __name__ == "__main__":
    shellInterface()
