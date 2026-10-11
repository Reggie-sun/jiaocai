"""Two independent textbook candidates; no chapter or Harness mutation."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle
from fontTools.ttLib import TTCollection
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "skills/scientific-visualization/scripts"))
from figure_export import export_figure

BLUE, INK = "#1F4E79", "#222222"


def graph(out, data, binary):
    mx = ET.Element("mxfile", host="drawio", version="32.4.1")
    page = ET.SubElement(mx, "diagram", name="局部候选与全局瓶颈", id="bottleneck")
    model = ET.SubElement(page, "mxGraphModel", page="1", pageWidth="900", pageHeight="710")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    common = "html=0;whiteSpace=wrap;fontFamily=Noto Sans CJK SC;fontSize=24;fontColor=#222222;"

    def cell(id, value, x, y, w, h, style="text;strokeColor=none;fillColor=none;", parent="1"):
        n = ET.SubElement(root, "mxCell", id=id, value=value, style=common+style, vertex="1", parent=parent)
        ET.SubElement(n, "mxGeometry", x=str(x), y=str(y), width=str(w), height=str(h), **{"as":"geometry"})
        return n

    # Real container; all graph nodes are children. Resource d stays outside.
    cell("reachable", "", 20, 60, 660, 430, "rounded=1;container=1;pointerEvents=0;fillColor=#FFFFFF;strokeColor=#555555;dashed=1;strokeWidth=2;")
    cell("heading", "同一组请求的可达关系", 70, 0, 560, 40, "text;strokeColor=none;fontSize=28;fontStyle=1;")
    request_xy = {"T1": (60, 145), "T2": (280, 145), "T3": (500, 145)}
    for r,(x,y) in request_xy.items():
        cell(r, r, x, y, 80, 80, "ellipse;fillColor=#FFFFFF;strokeColor=#222222;strokeWidth=2;fontSize=28;", "reachable")
    for p,y in [("b",20),("c",295)]:
        cell(p, p, 270, y, 100, 70, "rounded=1;fillColor=#FFFFFF;strokeColor=#1F4E79;strokeWidth=3;fontSize=28;", "reachable")
        cell(p+"-capacity", "容量 1", 390, y+15, 150, 40, parent="reachable")
    cell("d", "d", 740, 205, 100, 80, "rounded=1;fillColor=#FFFFFF;strokeColor=#555555;dashed=1;strokeWidth=2;fontSize=28;")
    cell("isolated-label", "存在但不可达", 690, 305, 210, 40)
    cell("isolated-note", "无允许关系", 700, 350, 190, 40)
    for r, positions in data["bottleneck"]["allowed"].items():
        for p in positions:
            # K3,2 planar placement: b/c above/below the request row.
            styles = common+"edgeStyle=none;rounded=1;orthogonalLoop=1;jettySize=auto;endArrow=none;startArrow=none;strokeWidth=2;strokeColor=#1F4E79;"
            styles += "exitX=0.5;exitY="+("0" if p=="b" else "1")+";entryX=0.5;entryY="+("1" if p=="b" else "0")+";"
            edge = ET.SubElement(root, "mxCell", id=f"allow-{r}-{p}", style=styles, edge="1", source=r, target=p, parent="reachable")
            ET.SubElement(edge, "mxGeometry", relative="1", **{"as":"geometry"})
    cell("legend", "T1—T3 为请求；连线是允许关系，不是已选安排", 0, 500, 900, 40)
    cell("count-left", "3 项请求", 60, 565, 290, 40, "text;strokeColor=none;fontSize=28;fontStyle=1;")
    cell("greater", ">", 385, 580, 80, 70, "text;strokeColor=none;fontSize=40;fontStyle=1;")
    cell("count-right", "2 个可达位置", 500, 565, 350, 40, "text;strokeColor=none;fontSize=28;fontStyle=1;")
    for i,r in enumerate(data["bottleneck"]["requests"]):
        cell("count-"+r, r, 65+i*90, 615, 70, 60, "ellipse;fillColor=#FFFFFF;strokeColor=#222222;strokeWidth=2;")
    for i,p in enumerate(["b","c"]):
        cell("count-"+p, p, 575+i*110, 615, 90, 60, "rounded=1;fillColor=#FFFFFF;strokeColor=#1F4E79;strokeWidth=3;")
    cell("proof", "至少一项无处可放；增加不可达的 d 不能消除瓶颈", 0, 680, 900, 40)
    source = out / "fig1-2-candidate.drawio"
    ET.indent(mx)
    ET.ElementTree(mx).write(source, encoding="utf-8", xml_declaration=True)
    for fmt in ("png","svg","pdf"):
        command = ["xvfb-run","-a",str(binary),"-x","-f",fmt,"-o",str(source.with_suffix("."+fmt)),str(source)]
        if fmt == "png": command += ["--width","2441","--border","0"]
        if fmt == "svg": command += ["--embed-svg-images"]
        command += ["--disable-gpu","--no-sandbox"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=90)
        if result.returncode: raise RuntimeError(result.stderr[-2000:])
    # PNG resolution metadata describes the actual pixel count at 155 mm.
    p=source.with_suffix(".png")
    with Image.open(p) as im:
        image=im.convert("RGB")
        dpi=image.width/(155/25.4)
        image.save(p,dpi=(dpi,dpi))


def intervals(out, data):
    # Fontconfig sees the installed collection, but Matplotlib's cache may not.
    # Select its actual SC face, rather than silently using DejaVu/JP fallback.
    font_source = Path(subprocess.check_output(["fc-match", "-f", "%{file}", "Noto Sans CJK SC"],text=True))
    font_file = Path.home()/".local/share/jiaocai-tools/fonts/NotoSansCJKSC-Regular.otf"
    if not font_file.exists():
        font_file.parent.mkdir(parents=True,exist_ok=True)
        collection=TTCollection(font_source)
        face=next(f for f in collection.fonts if f["name"].getDebugName(1)=="Noto Sans CJK SC")
        face.save(font_file)
    font_manager.fontManager.addfont(font_file)
    assert font_manager.FontProperties(fname=font_file).get_name()=="Noto Sans CJK SC"
    plt.rcParams.update({"font.family":"Noto Sans CJK SC", "font.size":11,
                         "axes.labelsize":11,"xtick.labelsize":10.5,"ytick.labelsize":11,
                         "svg.fonttype":"none","pdf.fonttype":42,"axes.unicode_minus":False,
                         "figure.facecolor":"white","savefig.facecolor":"white"})
    fig, axs = plt.subplots(3, 1, figsize=(155/25.4, 157/25.4))
    fig.subplots_adjust(left=.10, right=.96, bottom=.20, top=.94, hspace=1.10)
    titles=["活动重叠", "端点相接", "准备与清理独占场地"]
    for index,(ax,case) in enumerate(zip(axs,data["intervals"]["cases"])):
        ax.set(xlim=(535,725),ylim=(-.65,1.85),yticks=[1,0],yticklabels=["A","B"],xticks=[540,600,660,720],xticklabels=["9:00","10:00","11:00","12:00"])
        effective_a=case.get("effective_A",case["A"])
        effective_b=case.get("effective_B",case["B"])
        common_minutes=max(0,min(effective_a[1],effective_b[1])-max(effective_a[0],effective_b[0]))
        ax.set_title(f"{titles[index]}：共同占用 {common_minutes} 分钟",loc="left",fontsize=11.5,pad=12)
        ax.grid(axis="x",color="#D0D0D0",linewidth=.5)
        for side in ("top","left","right"): ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_linewidth(.7)
        ax.tick_params(axis="y",length=0,pad=6)
        for name,y in [("A",1),("B",0)]:
            start,end=case[name]
            ax.add_patch(Rectangle((start,y-.19),end-start,.38,facecolor="#F2F2F2",edgecolor=BLUE if name=="A" else INK,linewidth=1.1,linestyle="-" if name=="A" else "--",zorder=3))
            effective=case.get("effective_"+name,[start,end])
            ax.plot(effective[0],y,"o",color=INK,markersize=3,zorder=5)
            ax.plot(effective[1],y,"o",markerfacecolor="white",markeredgecolor=INK,markersize=4,zorder=5)
        overlap=case["expected_overlap"]
        if index==2:
            cleanup=case["A_cleanup_minutes"]
            preparation=case["B_preparation_minutes"]
            assert effective_a[1]==case["A"][1]+cleanup
            assert effective_b[0]==case["B"][0]-preparation
            ax.add_patch(Rectangle((case["A"][1],.81),cleanup,.38,facecolor="white",edgecolor=BLUE,hatch="////",linewidth=1,zorder=4))
            ax.add_patch(Rectangle((effective_b[0],-.19),preparation,.38,facecolor="white",edgecolor=INK,hatch="....",linewidth=1,zorder=4))
            ax.annotate(f"清理 {cleanup} 分钟",xy=(case["A"][1]+cleanup/2,1.19),xytext=(638,1.70),ha="center",va="center",fontsize=10.5,arrowprops={"arrowstyle":"-","color":INK,"lw":.7})
            ax.annotate(f"准备 {preparation} 分钟",xy=(effective_b[0]+preparation/2,-.19),xytext=(610,-.48),ha="center",fontsize=10.5,arrowprops={"arrowstyle":"-","color":INK,"lw":.7})
            ax.plot(overlap,[.49,.49],color=INK,lw=1.4,marker="|",markersize=9,zorder=6)
            ax.text(overlap[0]-2,.50,f"{overlap[0]//60}:{overlap[0]%60:02d}",ha="right",va="center",fontsize=10.5)
            ax.text(overlap[1]+2,.50,f"{overlap[1]//60}:{overlap[1]%60:02d}",ha="left",va="center",fontsize=10.5)
            # Effective endpoints are redrawn above the extension hatches.
            ax.plot(effective_b[0],0,"o",color=INK,markersize=3,zorder=6)
            ax.plot(effective_a[1],1,"o",markerfacecolor="white",markeredgecolor=INK,markersize=4,zorder=6)
        elif overlap:
            ax.add_patch(Rectangle((overlap[0],-.30),overlap[1]-overlap[0],1.60,facecolor="none",edgecolor=INK,hatch="|||",linewidth=.7,zorder=2))
        else:
            ax.axvline(effective_a[1],color=INK,ls=":",lw=.9)
    fig.text(.10,.035,"实心起点、空心终点表示 [开始, 结束)\n竖纹表示重叠；斜纹为清理，点纹为准备\n三组使用相同时间尺度",fontsize=10.5,va="bottom")
    export_figure(fig,out/"fig1-6-candidate",formats=["svg","pdf","png"],dpi=400,bbox_inches=None,overwrite=True,write_manifest=True,provenance={"raw_data":"materials/teaching-figures-pilot/data.json","transformations":[f"minutes since midnight; cleanup extends A by {cleanup}, preparation extends B by {preparation}"],"source":"original chapter teaching example; not observed measurements","uncertainty":"not applicable; exact example intervals"})
    plt.close(fig)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output-dir",type=Path,default=ROOT/"assets/figures/teaching-pilot")
    parser.add_argument("--drawio",type=Path,default=Path("/home/reggie/.local/share/jiaocai-tools/drawio-32.4.1/opt/drawio/drawio"))
    args=parser.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    data=json.loads((HERE/"data.json").read_text())
    graph(args.output_dir,data,args.drawio)
    intervals(args.output_dir,data)
    for number in (2,6):
        with Image.open(args.output_dir/f"fig1-{number}-candidate.png") as im:
            im.convert("L").save(args.output_dir/f"fig1-{number}-candidate-grayscale.png")
    manifest={"style":"textbook-style-v1.0","stage":"independent candidates; not chapter replacements","figures":[]}
    for number,desc in [(2,"全部六条允许关系构成可达部分；d无连接。3项请求争用2个容量1的位置，整体无解。"),(6,"三组共用9至12点时间轴；重叠60分钟、相接0分钟、独占准备/清理后10:45至11:20冲突35分钟。")]:
        paths=[args.output_dir/f"fig1-{number}-candidate.{ext}" for ext in (["drawio","svg","png","pdf"] if number==2 else ["svg","png","pdf"])]
        manifest["figures"].append({"baseline":f"assets/figures/ch01-rewrite/fig1-{number}.png","id":f"图1-{number} independent candidate","description":desc,"insert_width_mm":155,"source":"本书原创教学示例重新可视化；不更改正文、练习或数据。","files":{str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})
    (args.output_dir/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")


if __name__ == "__main__": main()
