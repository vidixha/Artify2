"""Regenerate the main-body charts from the values reported in the paper's tables.

Run from the paper/ directory:  python3 figures/make_figures.py
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

BLUE = "#2a78d6"
ORANGE = "#eb6834"
GRAY = "#8f8e89"
AQUA = "#1baf7a"
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


def fluency_bars(path):
    # Author's fluency check: outputs that keep >=50% of the un-ablated output's words,
    # out of 400 per cell (single run + three seeds, 100 images each).
    fluent = {
        "hi-zero": [0, 0, 1, 0],
        "en-zero": [0, 0, 1, 4],
        "hi-mean": [1, 0, 243, 5],
        "en-mean": [1, 0, 3, 0],
        "random": [292, 303, 283, 291],
    }
    pct = {k: np.array(v) / 4.0 for k, v in fluent.items()}
    series = [
        ("hi-zero", "Hindi heads, zero-ablated", dict(color=BLUE)),
        ("en-zero", "English heads, zero-ablated", dict(color=ORANGE)),
        ("hi-mean", "Hindi heads, mean-ablated", dict(color="white", edgecolor=BLUE, hatch="\\\\\\\\")),
        ("en-mean", "English heads, mean-ablated", dict(color="white", edgecolor=ORANGE, hatch="\\\\\\\\")),
        ("random", "20 random heads (control)", dict(color="white", edgecolor=GRAY, hatch="////")),
    ]
    fig, ax = plt.subplots(figsize=(6.5, 2.4))
    x = np.arange(len(MODELS))
    w = 0.16
    for k, (key, label, style) in enumerate(series):
        xs = x + (k - 2) * w
        ax.bar(xs, pct[key], w * 0.88, label=label, linewidth=0.8, **style)
        for xi, v in zip(xs, pct[key]):
            if v < 5:
                ax.text(xi, v + 1.2, f"{v:g}", ha="center", va="bottom", fontsize=5.5, color=INK_2)
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=7)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("outputs still fluent (%)")
    ax.grid(axis="y", color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper center", ncol=3, fontsize=6.5, bbox_to_anchor=(0.5, 1.22), handlelength=1.4,
              columnspacing=1.2)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def layer_placement(path):
    # How many of each top-20 set lie in decoder layers 0-1, per model, language and condition.
    counts = {
        "Qwen2-VL-2B": {"A": [19, 20, 20], "B": [4, 3, 4], "C": [2, 2, 6]},
        "InternVL3-2B": {"A": [14, 18, 18], "B": [9, 15, 17], "C": [4, 6, 14]},
        "SmolVLM": {"A": [10, 14, 9], "B": [4, 4, 5], "C": [3, 4, 4]},
        "PaliGemma-3B": {"A": [5, 6, 7], "B": [3, 3, 3], "C": [6, 7, 5]},
    }
    # Expected count if the 20 heads were spread uniformly over the grid: 20 * heads in layers 0-1 / total heads.
    chance = {"Qwen2-VL-2B": 20 * 24 / 336, "InternVL3-2B": 20 * 24 / 336,
              "SmolVLM": 20 * 64 / 768, "PaliGemma-3B": 20 * 16 / 144}
    styles = {
        "A": ("A: text", dict(color=BLUE)),
        "B": ("B: image+query", dict(color=ORANGE, hatch="\\\\\\\\", edgecolor="white")),
        "C": ("C: image-only", dict(color=AQUA, hatch="....", edgecolor="white")),
    }
    fig, axes = plt.subplots(1, 4, figsize=(6.5, 2.0), sharey=True)
    x = np.arange(len(LANGS))
    w = 0.26
    for ax, m in zip(axes, MODELS):
        for k, cond in enumerate("ABC"):
            label, style = styles[cond]
            ax.bar(x + (k - 1) * w, counts[m][cond], w * 0.88, label=label, linewidth=0, **style)
        ax.axhline(chance[m], color=INK_2, lw=0.7, ls=(0, (3, 2)))
        ax.set_title(m, fontsize=8, color=INK, pad=4)
        ax.set_xticks(x)
        ax.set_xticklabels(LANGS)
        ax.set_ylim(0, 20)
        ax.set_yticks([0, 5, 10, 15, 20])
        ax.grid(axis="y", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(axis="x", length=0)
    axes[0].set_ylabel("top-20 heads in layers 0-1")
    handles, labels = axes[0].get_legend_handles_labels()
    handles.append(Line2D([], [], color=INK_2, lw=0.7, ls=(0, (3, 2))))
    labels.append("expected if spread evenly")
    fig.legend(handles, labels, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.1), fontsize=7,
               handlelength=1.6, columnspacing=1.4)
    fig.tight_layout(rect=(0, 0, 1, 0.93), w_pad=1.0)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    overlap_dumbbell("figures/overlap_dumbbell.pdf")
    layer_placement("figures/layer_placement.pdf")
    fluency_bars("figures/fluency_bars.pdf")
