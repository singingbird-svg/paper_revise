import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================
# Data
# ============================================================

phi = [r'$\varphi_1$', r'$\varphi_2$', r'$\varphi_3$']
x = np.arange(len(phi))

# 5 x 5
proposed_5 = [0.3089, 0.6987, 1.3311]
poset_5    = [17.921, 89.203, 267.98]
milp_5     = [6.5013, 51.4076, 349.1159]

# 5 x 10
proposed_10 = [0.3890, 0.7216, 1.7716]
poset_10    = [18.385, 89.430, 268.98]
milp_10     = [6.8304, 59.7567, 371.2282]

# 5 x 20
proposed_20 = [0.4203, 1.1497, 1.7783]
poset_20    = [17.124, 90.137, 270.42]
milp_20     = [13.9042, 67.0037, 483.9699]


# ============================================================
# Figure
# ============================================================

fig, axes = plt.subplots(
    1, 3,
    figsize=(10.5, 3.8),
    sharey=True
)

datasets = [
    (
        proposed_5,
        poset_5,
        milp_5,
        r'(a) $5\times5$'
    ),
    (
        proposed_10,
        poset_10,
        milp_10,
        r'(b) $5\times10$'
    ),
    (
        proposed_20,
        poset_20,
        milp_20,
        r'(c) $5\times20$'
    )
]


# ============================================================
# Plot each panel
# ============================================================

for ax, (proposed, poset, milp, title) in zip(axes, datasets):

    # Proposed
    ax.plot(
        x,
        proposed,
        marker='o',
        linestyle='-',
        linewidth=2.5,
        markersize=9,
        label='Proposed'
    )

    # Poset
    ax.plot(
        x,
        poset,
        marker='s',
        linestyle='--',
        linewidth=2.5,
        markersize=9,
        label='Poset'
    )

    # MILP
    ax.plot(
        x,
        milp,
        marker='^',
        linestyle=':',
        linewidth=2.5,
        markersize=10,
        label='MILP'
    )

    # Log scale
    ax.set_yscale('log')
    ax.set_ylim(0.1, 1000)

    # x-axis
    ax.set_xticks(x)
    ax.set_xticklabels(phi)

    # panel title
    ax.set_title(
        title,
        fontsize=16.0
    )

    # grid
    ax.grid(
        axis='y',
        which='major',
        linewidth=0.8,
        alpha=0.30
    )

    ax.grid(
        axis='y',
        which='minor',
        linewidth=0.5,
        alpha=0.10
    )

    # remove unnecessary borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.tick_params(
        axis='x',
        labelsize=20.0
    )

    ax.tick_params(
        axis='y',
        labelsize=15.0
    )


# ============================================================
# Labels
# ============================================================

axes[0].set_ylabel(
    r'$T_{\mathrm{first}}$ (s)',
    fontsize=20.0
)

# Shared legend
handles, labels = axes[0].get_legend_handles_labels()

fig.legend(
    handles,
    labels,
    loc='upper left',
    ncol=3,
    frameon=False,
    fontsize=18.0,
    markerscale=1.2,
    bbox_to_anchor=(0.055, 1.04),
    borderaxespad=0
)


# ============================================================
# Layout
# ============================================================

plt.tight_layout(
    rect=[0, 0, 1, 0.93]
)

# Save
output_dir = Path(__file__).resolve().parent.parent / 'pic'

plt.savefig(
    output_dir / 'scalability_Tfirst.pdf',
    bbox_inches='tight'
)

plt.show()
