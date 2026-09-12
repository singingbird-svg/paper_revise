import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Use a Times-compatible font throughout the figure, including math text.
# Nimbus Roman is the installed metric-compatible Times implementation.
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Nimbus Roman'],
    'mathtext.fontset': 'stix',
    'axes.unicode_minus': False,
})

# ============================================================
# Data
# ============================================================

phi = [r'$\varphi_1$', r'$\varphi_2$', r'$\varphi_3$']
x = np.arange(len(phi))

# Mean time to the first feasible plan reported in Table III.
# Each list is ordered as phi_1, phi_2, and phi_3.
proposed_5 = [0.1, 0.1, 0.3]
poset_5    = [0.3, 1.2, 45.6]
milp_5     = [1.3, 2.8, 57.3]

proposed_20 = [0.4, 0.4, 0.4]
poset_20    = [0.6, 1.5, 48.5]
milp_20     = [17.9, 234.6, 2383.5]

proposed_80 = [0.9, 1.3, 1.4]
poset_80    = [1.1, 2.3, 49.3]
# All MILP runs at 5 x 80 were terminated by the OS before a feasible
# solution was found, so no numerical values are plotted.
milp_80     = [np.nan, np.nan, np.nan]


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
        '(a) 5×5'
    ),
    (
        proposed_20,
        poset_20,
        milp_20,
        '(b) 5×20'
    ),
    (
        proposed_80,
        poset_80,
        milp_80,
        '(c) 5×80'
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
    ax.set_ylim(0.05, 5000)

    # x-axis
    ax.set_xticks(x)
    ax.set_xticklabels(phi)

    # panel title
    ax.set_title(
        title,
        fontsize=18.0,
        fontweight='bold'
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

    if np.all(np.isnan(milp)):
        ax.text(
            0.5,
            0.93,
            'MILP: no feasible solution',
            transform=ax.transAxes,
            ha='center',
            va='top',
            color='#006400',
            fontsize=16.0,
            fontweight='bold'
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
plt.close(fig)
