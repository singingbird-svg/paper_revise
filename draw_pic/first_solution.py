import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ============================================================
# Data
# ============================================================

tasks = [
    r'$\varphi_1$',
    r'$\varphi_2$',
    r'$\varphi_3$',
    r'$\varphi_4$'
]

# Plan cost J
J_dis = np.array([
    136.79,
    79.84,
    203.32,
    251.67
])

J_score = np.array([
    125.23,
    74.06,
    173.36,
    212.98
])

J_plan = np.array([
    125.23,
    74.06,
    170.24,
    203.87
])

J_opt = np.array([
    102.67,
    67.73,
    170.24,
    176.93
])

# Time to the first feasible solution
T_dis = np.array([
    0.1750,
    0.0604,
    0.0825,
    0.4077
])

T_score = np.array([
    0.1702,
    0.0619,
    0.0807,
    0.4864
])


# ============================================================
# Figure layout
# ============================================================

x = np.arange(len(tasks))

bar_width = 0.20

# Two bars are placed on the left and right of x.
x_dis = x - 0.17
x_score = x + 0.17

# The vertical connected-dot line is exactly in the middle.
x_cost = x


fig, ax1 = plt.subplots(figsize=(9.0, 5.2))


# ============================================================
# 1. Bars: first-solution cost
# ============================================================

ax1.bar(
    x_dis,
    J_dis,
    width=bar_width,
    color='#7EC8F5',
    edgecolor='#000000',
    linewidth=0.8,
    label=r'$J(\Pi_{\mathrm{init}}^{\mathrm{dis}})$',
    zorder=2
)

ax1.bar(
    x_score,
    J_score,
    width=bar_width,
    color='#FFB347',
    edgecolor='#000000',
    linewidth=0.8,
    label=r'$J(\Pi_{\mathrm{init}}^{\mathrm{score}})$',
    zorder=2
)


# ============================================================
# 2. Vertical connected-dot line
#    J(Pi_init^dis)
#        |
#    J(Pi_init^score)
#        |
#    J(Pi_plan^score)
#        |
#    J(Pi_opt)
# ============================================================

cost_line_color = '#000000'

for i in range(len(x)):

    # Vertical line from optimum to discovery-order first solution
    ax1.vlines(
        x_cost[i],
        J_opt[i],
        J_dis[i],
        colors=cost_line_color,
        linewidth=1.0,
        alpha=1.0,
        zorder=4
    )

    # Horizontal dashed connector from the blue bar to the center line
    ax1.hlines(
        J_dis[i],
        x_dis[i] + bar_width / 2,
        x_cost[i],
        colors=cost_line_color,
        linestyles='dashed',
        linewidth=1.0,
        zorder=5
    )

    # Horizontal dashed connector from the orange bar to the center line
    ax1.hlines(
        J_score[i],
        x_cost[i],
        x_score[i] - bar_width / 2,
        colors=cost_line_color,
        linestyles='dashed',
        linewidth=1.0,
        zorder=5
    )

    # Small intersection point for Pi_init^dis
    ax1.plot(
        x_cost[i],
        J_dis[i],
        marker='o',
        markersize=2.5,
        color=cost_line_color,
        linestyle='None',
        zorder=6
    )

    # Small intersection point for Pi_init^score
    ax1.plot(
        x_cost[i],
        J_score[i],
        marker='o',
        markersize=2.5,
        color=cost_line_color,
        linestyle='None',
        zorder=6
    )

    # Pi_plan^score
    ax1.plot(
        x_cost[i],
        J_plan[i],
        marker='D',
        markersize=5.2,
        color='#1F4E79',
        linestyle='None',
        zorder=8
    )

    # Pi_opt
    ax1.plot(
        x_cost[i],
        J_opt[i],
        marker='o',
        markersize=7.5,
        color='#2CA02C',
        markeredgewidth=1.5,
        linestyle='None',
        zorder=9
    )


# Add Pi_plan and Pi_opt to legend
ax1.plot(
    [],
    [],
    marker='D',
    linestyle='None',
    markersize=5.2,
    color='#1F4E79',
    label=r'$J(\Pi_{\mathrm{plan}}^{\mathrm{score}})$'
)

ax1.plot(
    [],
    [],
    marker='o',
    linestyle='None',
    markersize=7.5,
    color='#2CA02C',
    markeredgewidth=1.5,
    label=r'$J(\Pi_{\mathrm{opt}})$'
)


# ============================================================
# 3. Left y-axis: plan cost
# ============================================================

ax1.set_ylabel(
    r'Plan cost $J$ (s)',
    fontsize=17.0
)

ax1.set_xticks(x)
ax1.set_xticklabels(tasks)

ax1.set_ylim(
    55,
    270
)

ax1.set_yticks(
    np.arange(60, 261, 20)
)

ax1.tick_params(
    axis='x',
    labelsize=17.0
)

ax1.tick_params(
    axis='y',
    labelsize=15.0
)

ax1.grid(
    axis='y',
    alpha=0.18,
    linewidth=0.8
)

ax1.set_axisbelow(True)


# ============================================================
# 4. Right y-axis: first-solution time
# ============================================================

ax2 = ax1.twinx()

ax2.plot(
    x,
    T_dis,
    marker='o',
    markersize=4.8,
    color='#1F4E79',
    linestyle=(0, (6, 2)),
    linewidth=1.6,
    label=r'$T(\Pi_{\mathrm{init}}^{\mathrm{dis}})$',
    zorder=10
)

ax2.plot(
    x,
    T_score,
    marker='s',
    markersize=4.6,
    color='#D55E00',
    linestyle=(0, (2.5, 1.5)),
    linewidth=1.6,
    label=r'$T(\Pi_{\mathrm{init}}^{\mathrm{score}})$',
    zorder=10
)

ax2.set_ylabel(
    'Solution time T (s)',
    fontsize=17.0
)

ax2.set_ylim(
    0,
    1.0
)

ax2.set_yticks(
    np.arange(0, 1.01, 0.2)
)

ax2.tick_params(
    axis='y',
    labelsize=15.0
)

# ============================================================
# 5. Appearance
# ============================================================

ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)


# Cost legend
handles1, labels1 = ax1.get_legend_handles_labels()

legend1 = ax1.legend(
    handles1,
    labels1,
    frameon=False,
    prop={'size': 15.0},
    ncol=2,
    loc='upper left'
)

ax1.add_artist(legend1)


# Time legend
ax2.legend(
    frameon=False,
    prop={'size': 15.0},
    ncol=2,
    loc='upper right',
    columnspacing=1.0
)


# ============================================================
# 6. Save
# ============================================================

fig.tight_layout()

output_dir = Path(__file__).resolve().parent.parent / 'pic'

plt.savefig(
    output_dir / 'first_solution_quality.pdf',
    bbox_inches='tight'
)

plt.show()
