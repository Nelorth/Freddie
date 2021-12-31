"""
Definition of utility plotting functions.
"""

__author__ = "Nikolas Kirschstein"
__copyright__ = "Copyright 2021, Nikolas Kirschstein, All rights reserved."
__license__ = "Apache License 2.0"
__version__ = "1.0.0"
__maintainer__ = "Nikolas Kirschstein"
__email__ = "nikolas.kirschstein@gmail.com"
__status__ = "Prototype"


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import utils.constants as c

from itertools import chain, cycle, product
from matplotlib.dates import DateFormatter
from matplotlib.patches import Patch

LINEWIDTH_THIN = 0.25  # thin plot linewidth
LINEWIDTH_THICK = 1  # thick plot linewidth
LINESTYLE = "--"  # default line style

# update settings for LaTeX exporting
mpl.rcParams.update({
    "text.usetex": True,
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "font.size": 11,
    "figure.autolayout": True,
    "text.latex.preamble": "\n".join([
        r"\usepackage{palatino}",
        r"\usepackage{siunitx}",
    ])
})


def plot_function(func, xlim, ylim=(), label=None, xlabel=None, ylabel=None, title=None, outfile=None, **kwargs):
    x = np.arange(xlim[0], xlim[1] + (xlim[1] - xlim[0]) / 100, (xlim[1] - xlim[0]) / 100)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylim:
        plt.ylim(ylim)
    plt.grid(linewidth=LINEWIDTH_THIN, linestyle=LINESTYLE)
    plt.plot(x, func(x), label=label, linewidth=LINEWIDTH_THICK, **kwargs)

    _save_figure(outfile)


def plot_metrics(train_metric, eval_metric, ylabel=None, outfile=None):
    plt.figure(figsize=(4, 3))
    plt.plot(range(1, len(train_metric) + 1), train_metric, label="training")
    plt.plot(range(1, len(eval_metric) + 1), eval_metric, label="validation")
    plt.legend()
    plt.grid(linestyle=LINESTYLE)
    plt.xlabel("Epoch")
    plt.ylabel(ylabel)

    _save_figure(outfile)


def plot_orbit(x, Y, *, symbol, labels=(), title=None, xlabel=None, ylabel=None, outfile=None):
    plt.gca().xaxis.set_major_formatter(DateFormatter("$%d$ %b '$%y$\n$%H$:$%M$", usetex=False))

    for (i, y) in enumerate(Y):
        plt.plot(x, y, linewidth=LINEWIDTH_THIN, label=f"${symbol}_{i + 1}$")

    n = np.linalg.norm(np.array(Y), axis=0)
    p = plt.plot(x, n, linewidth=LINEWIDTH_THIN, label=f"$\\pm||\\vec{{{symbol}}}||$")
    plt.plot(x, -n, linewidth=LINEWIDTH_THIN, color=p[-1].get_color())

    colors = ["whitesmoke", "indianred", "burlywood", "cornflowerblue", "lightgreen"]

    if len(labels) > 0:
        for i in range(len(labels) - 1):
            if labels[i] != 0:
                plt.axvspan(x[i], x[i + 1], alpha=0.5, facecolor=colors[labels[i]])

        class_legend = [Patch(facecolor=colors[key], label=val) for key, val in c.CLASSES.items()]
        plt.gca().add_artist(plt.legend(handles=class_legend, loc="upper right"))

    plt.grid(linewidth=LINEWIDTH_THIN, linestyle="--")
    plt.margins(x=0)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(fontsize=8)
    plt.legend(loc="upper left")

    _save_figure(outfile)


def plot_confusion_matrix(confmat, *,
                          cmap="Blues",
                          labels=None,
                          xlabel="predicted",
                          ylabel="true",
                          normalize=True,
                          show_colorbar=True,
                          show_values=True,
                          outfile=None):

    if normalize:
        confmat = confmat / confmat.sum()

    plt.set_cmap(cmap)
    im = plt.matshow(confmat)

    num_classes = confmat.shape[0]
    ticks = np.arange(num_classes)
    labels = labels if labels else ticks
    plt.xticks(ticks, labels, rotation=45)
    plt.yticks(ticks, labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if show_colorbar:
        plt.colorbar()

    if show_values:
        thresh = (confmat.max() + confmat.min()) / 2.0
        for i, j in product(range(num_classes), range(num_classes)):
            color = im.cmap(1.0) if confmat[i, j] < thresh else im.cmap(0)
            text = format(confmat[i, j], ".2g")
            plt.text(j, i, text, ha="center", va="center", color=color)

    _save_figure(outfile)


def _save_figure(outfile):
    if outfile:
        plt.savefig(outfile, bbox_inches="tight")
