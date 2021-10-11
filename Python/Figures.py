import numpy
import pandas
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors


# Settings

fileInput  = '../Data/sincos.txt'
fileSd     = '../Data/sd.png'
fileMax    = '../Data/max.png'
fileDelta  = '../Data/delta.png'
fileLowest = '../Data/lowest.png'


# Functions

def plotContour(inputTable, outputTable, stat, title, minBar, maxBar, barLabel, contourLevels, contourThreshold, width, height):
    fig, ax = pyplot.subplots() 

    ax.set_aspect(aspect = 'equal')

    pyplot.pcolormesh(inputTable, outputTable, stat, shading = 'auto', cmap = 'inferno', norm = colors.LogNorm(vmin = minBar, vmax = maxBar))

    pyplot.xticks([4, 8, 12, 16, 20, 24, 28, 32])
    pyplot.yticks([4, 8, 12, 16, 20, 24, 28, 32])
        
    pyplot.xlabel('Input bits', fontsize = 12)
    pyplot.ylabel('Output bits', fontsize = 12)

    cb = pyplot.colorbar()
    cb.set_label(label = barLabel, size = 12)

    cs = pyplot.contour(inputTable, outputTable, stat, contourLevels, colors = ['w' if x <= contourThreshold else 'k' for x in contourLevels])
    ax.clabel(cs, inline = True, fmt = '%1.E', inline_spacing = 5, fontsize = 10)

    pyplot.gcf().set_size_inches(width, height)


def plotDelta(width, height):
    for delta in range(5):
        y = numpy.diag(sd, delta)
        x = numpy.arange(bitMin + delta, bitMax - delta + 1, 2)
        color = ['C0', 'C1', 'C2', 'C3', 'C4'][delta]
        pyplot.semilogy(x, y, '.-', color = color)

    for delta in range(5):
        y = numpy.diag(error, delta)
        x = numpy.arange(bitMin + delta, bitMax - delta + 1, 2)
        color = ['C0', 'C1', 'C2', 'C3', 'C4'][delta]
        pyplot.semilogy(x, y, '.-', color = color)

    pyplot.ylim(1E-9, 1)

    pyplot.xticks([8, 16, 24, 32, 40, 48, 56, 64])

    yticks = [1]
    for i in range(1, 10):
        for j in range(9, 0, -1):
            yticks.append((10 ** -i) * j)

    pyplot.yticks(yticks)

    pyplot.xlabel('Input + output bit-length')
    pyplot.ylabel('Maximum absolute error\nStandard deviation of the error')

    legend = pyplot.legend(['+0', '+1', '+2', '+3', '+4'], title = 'Bit-length delta', frameon = False)
    legend._legend_box.align = "left"

    pyplot.gcf().set_size_inches(width, height)


def plotLowest(width, height):
    bit = numpy.arange(bitMin, bitMin + bitRange)

    for delta in range(int(minSdDelta.min()), int(minSdDelta.max()) + 1):
        slice = minSdDelta == delta
        color = ['C0', 'C1', 'C2', 'C3', 'C4'][delta]
        pyplot.semilogy(bit[slice], minSdValue[slice], '.', color = color, markersize = 12)

    pyplot.plot(bit, minSdValue, 'k', zorder = 0)

    for delta in range(int(minErrorDelta.min()), int(minErrorDelta.max()) + 1):
        slice = minErrorDelta == delta
        color = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5'][delta]
        pyplot.semilogy(bit[slice], minErrorValue[slice], '.', color = color, markersize = 12)

    pyplot.plot(bit, minErrorValue, 'k', zorder = 0)

    pyplot.ylim(1E-9, 1)

    pyplot.xticks([8, 16, 24, 32, 40, 48, 56, 64])

    yticks = [1]
    for i in range(1, 10):
        for j in range(9, 0, -1):
            yticks.append((10 ** -i) * j)

    pyplot.yticks(yticks)

    pyplot.xlabel('Input + output bit-length')
    pyplot.ylabel('Maximum absolute error\nStandard deviation of the error')

    legend = pyplot.legend(['+0', '+1', '+2', '+3', '+4'], title = 'Bit-length delta', frameon = False)
    legend._legend_box.align = "left"

    pyplot.gcf().set_size_inches(width, height)


# Code

df = pandas.read_csv(fileInput)

m = df.to_numpy()

inputMin  = int(m[:, 0].min())
inputMax  = int(m[:, 0].max())
outputMin = int(m[:, 1].min())
outputMax = int(m[:, 1].max())
bitMin    = inputMin + inputMin
bitMax    = inputMax + outputMax

inputRange  = inputMax  - inputMin  + 1
outputRange = outputMax - outputMin + 1
bitRange    = bitMax - bitMin + 1

sd = numpy.zeros((inputRange, outputRange))
error = numpy.zeros((inputRange, outputRange))

minSdValue = numpy.ones(bitRange)
minSdDelta = numpy.zeros(bitRange)

minErrorValue = numpy.ones(bitRange)
minErrorDelta = numpy.ones(bitRange)

for i in range(m.shape[0]):
    inputBit  = int(m[i, 0]) - inputMin
    outputBit = int(m[i, 1]) - outputMin
    sd[inputBit, outputBit] = m[i, 3]
    error[inputBit, outputBit] = max(abs(m[i,4]), abs(m[i, 5]))

    if sd[inputBit, outputBit] < minSdValue[inputBit + outputBit]:
        minSdValue[inputBit + outputBit] = sd[inputBit, outputBit]
        minSdDelta[inputBit + outputBit] = outputBit - inputBit
    
    if error[inputBit, outputBit] < minErrorValue[inputBit + outputBit]:
        minErrorValue[inputBit + outputBit] = error[inputBit, outputBit]
        minErrorDelta[inputBit + outputBit] = outputBit - inputBit

inputTable  = numpy.arange(inputMin, inputMax + 1)
outputTable = numpy.arange(outputMin, outputMax + 1)

levels = [1E-8, 1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1]
plotContour(inputTable, outputTable, sd.T, '', 1E-8, 1E-0, 'Standard deviation of the error', levels, 3E-5, 6, 4.75)
pyplot.savefig(fileSd, dpi = 300)
pyplot.clf()

levels = [1E-7, 1E-6, 1E-5, 1E-4, 1E-3, 1E-2, 1E-1]
plotContour(inputTable, outputTable, error.T, '', 1E-8, 1E-0, 'Maximum absolute error', levels, 3E-5, 6, 4.75)
pyplot.savefig(fileMax, dpi = 300)
pyplot.clf()

pyplot.close()

plotDelta(9, 6)
pyplot.savefig(fileDelta, dpi = 300)
pyplot.clf()

plotLowest(9, 6)
pyplot.savefig(fileLowest, dpi = 300)
pyplot.clf()