"""Chronological document nodes on a common year scale; no influence arrows."""
from pathlib import Path
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
OUT = ROOT / "assets/figures/ch01-figures"
sys.path.insert(0, str(ROOT / "skills/scientific-visualization/scripts"))
from figure_export import export_figure


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    events = [
        {"year": 1937, "authors": "Turing", "topic": "规则、配置与计算边界", "reference": "[5]"},
        {"year": 1971, "authors": "Papert / Solomon", "topic": "学习者表达、运行与修改程序", "reference": "[6]"},
        {"year": 2006, "authors": "Wing", "topic": "面向更广泛人群的能力倡议", "reference": "[1]"},
        {"year": 2010, "authors": "Cuny / Snyder / Wing", "topic": "问题与解法的共同定义表述", "reference": "[2]"},
    ]
    (HERE / "timeline-data.json").write_text(json.dumps(events, ensure_ascii=False, indent=2) + "\n")
    font_manager.fontManager.addfont(Path.home() / ".local/share/jiaocai-tools/fonts/NotoSansCJKSC-Regular.otf")
    with plt.rc_context({"font.family": "Noto Sans CJK SC", "font.size": 11,
                         "svg.fonttype": "none", "pdf.fonttype": 42,
                         "figure.facecolor": "white", "savefig.facecolor": "white"}):
        fig, ax = plt.subplots(figsize=(155 / 25.4, 128 / 25.4))
        fig.subplots_adjust(left=.08, right=.96, top=.89, bottom=.27)
        ax.set(xlim=(1933, 2016), ylim=(-.50, 3.65), yticks=[],
               xticks=[1940, 1960, 1980, 2000], xlabel="出版年份")
        ax.tick_params(axis="x", labelsize=10.5)
        for side in ("top", "left", "right"):
            ax.spines[side].set_visible(False)
        ax.grid(axis="x", color="#DDDDDD", linewidth=.5)
        for i, event in enumerate(events):
            y = 3 - i
            ax.plot(event["year"], y, "o", color="#1F4E79", markeredgecolor="#222222", markersize=7)
            ax.text(event["year"], y + .21, str(event["year"]), ha="center", va="bottom", fontsize=11, weight="bold")
            x = 1942 if i == 0 else (1976 if i == 1 else 1938)
            ax.text(x, y + .06, event["authors"] + "  " + event["reference"], ha="left", va="center", fontsize=11.5, weight="bold")
            ax.text(x, y - .24, event["topic"], ha="left", va="center", fontsize=10.5)
        fig.text(.08, .96, "不同文献回答不同的问题", fontsize=12, weight="bold", va="top")
        fig.text(.08, .035, "点的位置按出版年份；行的位置只用于分隔文献\n图灵论文1936年收稿、宣读，1937年出版\n并置用于主题比较，不表示直接影响或因果传承", fontsize=10.5, va="bottom")
        export_figure(fig, OUT / "fig1-4", formats=["png", "svg", "pdf"],
                      dpi=400, bbox_inches=None, overwrite=True, write_manifest=True,
                      provenance={"raw_data": "materials/ch01-figures/timeline-data.json",
                                  "transformations": ["Common year axis; vertical rows carry no quantitative meaning"],
                                  "source": "Existing chapter references [5], [6], [1], [2]",
                                  "uncertainty": "Historical publication years, not measured effect or causal relation"})
        plt.close(fig)


if __name__ == "__main__":
    main()
