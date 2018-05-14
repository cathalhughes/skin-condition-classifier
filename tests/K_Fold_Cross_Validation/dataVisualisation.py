import matplotlib.pyplot as plt
import ast

allData = [["Ringworm", "ringwormData/one.txt", "ringwormData/two.txt", "ringwormData/three.txt", "ringwormData/four.txt", "ringwormData/five.txt", "ringwormData/Rw.txt"],
            ["Hives", "hivesData/one.txt", "hivesData/two.txt", "hivesData/three.txt", "hivesData/four.txt", "hivesData/five.txt", "hivesData/Hi.txt"],
            ["Psoriasis", "psoriasisData/one.txt", "psoriasisData/two.txt", "psoriasisData/three.txt", "psoriasisData/four.txt", "PsoriasisData/five.txt", "psoriasisData/Ps.txt"],
            ["Shingles", "shinglesData/one.txt", "shinglesData/two.txt", "shinglesData/three.txt", "shinglesData/four.txt", "shinglesData/five.txt", "shinglesData/Sh.txt"],
            ["Eczema", "eczemaData/one.txt", "eczemaData/three.txt", "eczemaData/five.txt", "eczemaData/Ec.txt"]]
desc = ["K-Fold 1", "K-Fold 2", "K-Fold 3", "K-Fold 4", "K-Fold 5", "Final Trained"]
def parseTextFile(fname):
    with open(fname, "r") as f:
        line = f.readline()

    k = 0
    i = 0
    data = []
    while k < 4:

        while line[i] != "[" and i != len(line):
            i += 1
        if line[i] == "[":
            j = i + 1
        while line[j] != "]" and j != len(line):
            j += 1

        if line[j] == "]":
            lst = ast.literal_eval(line[i:j + 1])
        data.append(lst)
        i = j
        k += 1
    return data

def close_event():
    plt.close()

def createChart(data, name):
    epochs = [i for i in range(1, len(data[1]) + 1)]
    fig = plt.figure()
    timer = fig.canvas.new_timer(interval = 3000)
    timer.add_callback(close_event)
    #plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])
    plt.title(name)
    plt.xticks(epochs)
    plt.xlabel("Epochs")
    plt.ylabel("Percentage")

    plt.plot(epochs, data[0])
    plt.plot(epochs, data[1])
    plt.plot(epochs, data[2])
    plt.plot(epochs, data[3])

    plt.legend(['validation loss', 'validation accuracy', 'training loss', 'training accuracy'], loc='upper left')
    timer.start()
    plt.show()

for data in allData:
    if len(data) == 5:
        desc = [w.replace("K-Fold 4", "Final Trained") for w in desc]
    for i in range(1, len(data)):
        info = parseTextFile(data[i])
        description = desc[i - 1]
        name = description + " - " + data[0]
        createChart(info, name)


