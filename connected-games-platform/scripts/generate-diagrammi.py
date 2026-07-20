from pathlib import Path
import runpy

from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "03-diagrammi.pdf"
COMMON = runpy.run_path(str(Path(__file__).with_name("generate-diagrammi-completi.py")))
PAGE_W, PAGE_H = landscape(A4)


def main():
    c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
    selected = [
        COMMON["page_2_use_cases"],
        COMMON["page_3_domain"],
        COMMON["page_1_architecture"],
        COMMON["page_7_match"],
        COMMON["page_8_offline"],
    ]
    titles = [
        "Casi d'uso",
        "Dominio dati",
        "Package e architettura",
        "Sequenza partita MQTT",
        "Sequenza offline",
    ]
    for title, fn in zip(titles, selected):
        COMMON["page_header"](c, title)
        fn(c)
        c.showPage()
    c.save()
    print(OUT)


if __name__ == "__main__":
    main()
