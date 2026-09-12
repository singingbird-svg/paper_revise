#!/usr/bin/env python3
"""Plot the scaled BnB trace while preserving the layout of Fig. 6."""

import csv
import math
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_FILE = SCRIPT_DIR / "data" / "bnb_combo_trace.csv"
OUTPUT_PREFIX = SCRIPT_DIR / "bnb_combo_bounds_compressed_scaled"
SCALE_FACTOR = 1.25
MAX_STEP = 800
TICK_STEPS = [0, 50, 100, 200, 400, 800]
Y_LIM = (35, 120)
Y_TICKS = [40, 50, 60, 70, 80, 90, 100, 110]
REQUIRED_COLUMNS = {"lb", "global_best", "ub_recorded"}


def compressed_x(step):
    """Map 0--50 linearly and give each subsequent doubling equal width."""
    if step <= 50:
        return step / 50.0
    return 1.0 + math.log(step / 50.0, 2.0)


def scaled_value(row, column, row_number):
    """Read and scale one finite numeric value from a CSV row."""
    try:
        value = float(row[column])
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Invalid {column!r} value on CSV data row {row_number}: "
            f"{row.get(column)!r}"
        ) from exc
    if not math.isfinite(value):
        raise ValueError(
            f"Non-finite {column!r} value on CSV data row {row_number}: {value}"
        )
    return value * SCALE_FACTOR


def load_trace(path):
    """Load the first 800 search records and scale the three plotted fields."""
    rows = []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            missing_text = ", ".join(sorted(missing))
            raise ValueError(f"Missing required CSV columns: {missing_text}")

        # As in the original Fig. 6 script, file order is the true search
        # order; the CSV's step column is intentionally not used.
        for step, row in enumerate(reader, start=1):
            if step > MAX_STEP:
                break
            rows.append(
                {
                    "step": step,
                    "upper": scaled_value(row, "ub_recorded", step),
                    "lower": scaled_value(row, "lb", step),
                    "global_best": scaled_value(row, "global_best", step),
                }
            )

    if len(rows) < MAX_STEP:
        raise ValueError(
            f"Expected at least {MAX_STEP} CSV rows, but found {len(rows)}"
        )
    return rows


def aggregate_for_display(rows):
    """Match the aggregation and visual resolution used in Fig. 6."""
    summary = []
    index = 0
    while index < len(rows):
        step = rows[index]["step"]
        if step <= 100:
            block_size = 1
            interval_end = 100
        elif step <= 200:
            block_size = 2
            interval_end = 200
        elif step <= 400:
            block_size = 4
            interval_end = 400
        else:
            block_size = 8
            interval_end = MAX_STEP

        block = rows[index : min(index + block_size, interval_end, len(rows))]
        upper = [row["upper"] for row in block]
        lower = [row["lower"] for row in block]
        summary.append(
            {
                "step": 0.5 * (block[0]["step"] + block[-1]["step"]),
                "upper": statistics.median(upper),
                "upper_min": min(upper),
                "upper_max": max(upper),
                "lower": statistics.median(lower),
                "lower_min": min(lower),
                "lower_max": max(lower),
            }
        )
        index += len(block)
    return summary


def main():
    rows = load_trace(DATA_FILE)
    x = [compressed_x(row["step"]) for row in rows]
    global_best = [row["global_best"] for row in rows]
    summary = aggregate_for_display(rows)
    summary_x = [compressed_x(row["step"]) for row in summary]

    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "mathtext.fontset": "stix",
            "font.size": 12,
            "axes.labelsize": 13,
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.5,
            "axes.linewidth": 0.8,
        }
    )

    fig, ax = plt.subplots(figsize=(6.2, 4.15))
    upper_line, = ax.plot(
        summary_x,
        [row["upper"] for row in summary],
        color="#d62728",
        linewidth=1.05,
        zorder=3,
    )
    lower_line, = ax.plot(
        summary_x,
        [row["lower"] for row in summary],
        color="#b3a400",
        linewidth=1.05,
        zorder=3,
    )
    ax.fill_between(
        summary_x,
        [row["upper_min"] for row in summary],
        [row["upper_max"] for row in summary],
        color="#d62728",
        alpha=0.10,
        linewidth=0,
        zorder=1,
    )
    ax.fill_between(
        summary_x,
        [row["lower_min"] for row in summary],
        [row["lower_max"] for row in summary],
        color="#b3a400",
        alpha=0.12,
        linewidth=0,
        zorder=1,
    )
    global_best_line, = ax.plot(
        x,
        global_best,
        color="#2044c7",
        linewidth=1.8,
        drawstyle="steps-post",
        label=r"$J^\star$",
        zorder=3,
    )

    ax.set_xlim(compressed_x(0), compressed_x(MAX_STEP))
    ax.set_ylim(*Y_LIM)
    ax.set_xticks([compressed_x(step) for step in TICK_STEPS])
    ax.set_xticklabels([str(step) for step in TICK_STEPS])
    ax.set_yticks(Y_TICKS)
    ax.set_xlabel("Search iteration")
    ax.set_ylabel("Completion time (s)")
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#dedede", linewidth=0.65)

    legend_handles = [upper_line, lower_line, global_best_line]
    ax.legend(
        legend_handles,
        [r"$\mathrm{UB}$", r"$\mathrm{LB}$", r"$J^\star$"],
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=3,
        frameon=True,
        fontsize=12,
        columnspacing=1.8,
        handlelength=2.2,
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_PREFIX.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(OUTPUT_PREFIX.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)

    print(f"Read: {DATA_FILE}")
    print(f"Scale factor: {SCALE_FACTOR}")
    print(f"Plotted rows: {len(rows)}")
    print(f"Wrote: {OUTPUT_PREFIX.with_suffix('.png')}")
    print(f"Wrote: {OUTPUT_PREFIX.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
