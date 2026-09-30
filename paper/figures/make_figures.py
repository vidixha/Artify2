"""Regenerate the main-body charts from the values reported in the paper's tables.

Run from the paper/ directory:  python3 figures/make_figures.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY = "#8f8e89"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"
CHANCE = "#ecebe7"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.edgecolor": INK_2,
    "axes.labelcolor": INK,
    "axes.linewidth": 0.6,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
    "pdf.fonttype": 42,
})

MODELS = ["Qwen2-VL-2B", "InternVL3-2B", "SmolVLM", "PaliGemma-3B"]
LANGS = ["en", "es", "hi"]


def overlap_dumbbell(path):
    # Table 2: A∩C (text vs image-only) and B∩C (image+query vs image-only), K=20.
    a_c = {
        "Qwen2-VL-2B": [0.081, 0.053, 0.176],
        "InternVL3-2B": [0.176, 0.250, 0.667],
        "SmolVLM": [0.143, 0.111, 0.212],
        "PaliGemma-3B": [0.333, 0.290, 0.290],
    }
    b_c = {
        "Qwen2-VL-2B": [0.538, 0.538, 0.429],
        "InternVL3-2B": [0.176, 0.212, 0.667],
        "SmolVLM": [0.667, 0.905, 0.905],
        "PaliGemma-3B": [0.333, 0.250, 0.333],
    }
    chance = {"Qwen2-VL-2B": 0.081, "InternVL3-2B": 0.081, "SmolVLM": 0.053, "PaliGemma-3B": 0.143}

    fig, axes = plt.subplots(1, 4, figsize=(6.5, 1.9), sharey=True)
    y = np.arange(len(LANGS))[::-1]
    for ax, m in zip(axes, MODELS):
        ax.axvspan(0, chance[m], color=CHANCE, lw=0, zorder=0)
        for yi, lo, hi in zip(y, a_c[m], b_c[m]):
            ax.plot([lo, hi], [yi, yi], color=GRID, lw=2, zorder=1, solid_capstyle="round")
        ax.scatter(b_c[m], y, marker="s", s=64, color=ORANGE, edgecolor="white", linewidth=1, zorder=2)
        ax.scatter(a_c[m], y, marker="o", s=30, color=BLUE, edgecolor="white", linewidth=1, zorder=3)
        ax.set_title(m, fontsize=8, color=INK, pad=4)
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(["0", "0.5", "1"])
        ax.set_ylim(-0.6, 2.6)
        ax.grid(axis="x", color=GRID, lw=0.5, zorder=0)
        ax.set_axisbelow(True)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(LANGS)
    fig.supxlabel("Jaccard overlap of top-20 heads", fontsize=8, color=INK, y=0.04)
    handles = [
        Line2D([], [], marker="o", ls="", color=BLUE, markeredgecolor="white", markersize=6,
               label="text vs. image-only (A$\\cap$C)"),
        Line2D([], [], marker="s", ls="", color=ORANGE, markeredgecolor="white", markersize=7,
               label="image+query vs. image-only (B$\\cap$C)"),
        Patch(facecolor=CHANCE, edgecolor="none", label="below chance ($p_{95}$)"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.08),
               handletextpad=0.4, columnspacing=1.6)
    fig.tight_layout(rect=(0, 0.02, 1, 0.94), w_pad=1.2)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def ablation_bars(path):
    # Table 7 (seed variance): mean ± sd over three seeds, percent of outputs whose script flips.
    hi_zero = ([70.3, 11.7, 35.3, 97.3], [5.0, 1.2, 2.1, 0.5])
    en_zero = ([46.3, 17.0, 35.3, 15.3], [3.4, 2.2, 2.1, 2.9])
    random = ([7.0, 14.0, 8.7, 7.0], [4.9, 6.2, 0.9, 2.8])
    en_mean = ([33.7, 23.3, 47.0, 65.0], [8.8, 2.5, 1.6, 2.9])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 2.3), gridspec_kw={"width_ratios": [3, 2.5]})
    x = np.arange(len(MODELS))
    err = dict(ecolor=INK_2, elinewidth=0.7, capsize=1.8, capthick=0.7)
    labels = ["Qwen2-VL\n2B", "InternVL3\n2B", "SmolVLM\n", "PaliGemma\n3B"]

    w = 0.26
    ax1.bar(x - w, hi_zero[0], w * 0.9, yerr=hi_zero[1], color=BLUE, label="Hindi heads, zero-ablated", error_kw=err)
    ax1.bar(x, en_zero[0], w * 0.9, yerr=en_zero[1], color=ORANGE, label="English heads, zero-ablated", error_kw=err)
    ax1.bar(x + w, random[0], w * 0.9, yerr=random[1], color="white", edgecolor=GRAY, hatch="////",
            linewidth=0.8, label="random 20 heads (control)", error_kw=err)
    ax1.set_title("(a) Top heads vs. random heads", fontsize=8, color=INK, loc="left")

    w2 = 0.36
    ax2.bar(x - w2 / 2, en_zero[0], w2 * 0.9, yerr=en_zero[1], color=ORANGE, label="zero-ablated", error_kw=err)
    ax2.bar(x + w2 / 2, en_mean[0], w2 * 0.9, yerr=en_mean[1], color="white", edgecolor=ORANGE, hatch="\\\\\\\\",
            linewidth=0.8, label="mean-ablated", error_kw=err)
    ax2.set_title("(b) English heads: zero vs. mean ablation", fontsize=8, color=INK, loc="left")

    for ax in (ax1, ax2):
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=6.5)
        ax.set_ylim(0, 105)
        ax.set_yticks([0, 25, 50, 75, 100])
        ax.grid(axis="y", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
        ax.legend(loc="upper left", fontsize=7, handlelength=1.4, borderaxespad=0.2)
    ax1.set_ylabel("outputs whose script flips (%)")
    fig.tight_layout(w_pad=2)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def lineage_matrix(path):
    # Section 6.4: shared (layer, head) positions among each pair's top-20 text-condition heads.
    order = ["Qwen2-VL-2B", "InternVL3-2B", "PaliGemma-3B", "SmolVLM"]
    family = {"Qwen2-VL-2B": "Qwen2", "InternVL3-2B": "Qwen2.5", "PaliGemma-3B": "Gemma", "SmolVLM": "SmolLM2"}
    pairs = {
        ("Qwen2-VL-2B", "InternVL3-2B"): 18,
        ("Qwen2-VL-2B", "PaliGemma-3B"): 8,
        ("InternVL3-2B", "PaliGemma-3B"): 9,
        ("Qwen2-VL-2B", "SmolVLM"): 2,
        ("InternVL3-2B", "SmolVLM"): 1,
        ("PaliGemma-3B", "SmolVLM"): 0,
    }
    n = len(order)
    mat = np.full((n, n), np.nan)
    for i, a in enumerate(order):
        for j, b in enumerate(order):
            if j < i:
                mat[i, j] = pairs.get((a, b), pairs.get((b, a)))

    cmap = LinearSegmentedColormap.from_list("blue_seq", ["#f4f8fd", "#86b6ef", "#2a78d6", "#104281"])
    fig, ax = plt.subplots(figsize=(3.3, 2.7))
    from matplotlib.patches import Rectangle
    for i in range(n):
        for j in range(n):
            if j < i:
                v = int(mat[i, j])
                ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=cmap(v / 20),
                                       edgecolor="white", linewidth=2))
                ax.text(j, i, str(v), ha="center", va="center", fontsize=9,
                        color="white" if v >= 10 else INK)
    ticks = [f"{m}\n({family[m]})" for m in order]
    ax.set_xticks(range(n))
    ax.set_xticklabels(ticks, fontsize=6.5, rotation=0)
    ax.set_yticks(range(n))
    ax.set_yticklabels(ticks, fontsize=6.5)
    ax.set_xlim(-0.5, n - 1.5)
    ax.set_ylim(n - 0.5, 0.5)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Shared (layer, head) positions\nbetween top-20 text-condition sets", fontsize=8, color=INK, pad=6)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    overlap_dumbbell("figures/overlap_dumbbell.pdf")
    ablation_bars("figures/ablation_bars.pdf")
    lineage_matrix("figures/lineage_matrix.pdf")
