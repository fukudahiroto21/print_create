from io import BytesIO
import os
import random

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from vercel import Response   # ← これが決定打


def handler(request):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    assets_dir = os.path.join(project_root, "assets")

    png_path = os.path.join(assets_dir, "School Print.png")
    font_path = os.path.join(assets_dir, "ipaexg.ttf")

    if os.path.exists(png_path):
        bg = ImageReader(png_path)
        c.drawImage(bg, 0, 0, width=page_width, height=page_height)

    pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
    c.setFont("IPAexGothic", 22)

    problems = [(random.randint(1, 20), random.randint(1, 20)) for _ in range(10)]

    top_y = page_height - 140
    bottom_y = 120
    gap = (top_y - bottom_y) / 9
    start_x = 140

    for i, (a, b) in enumerate(problems, start=1):
        y = top_y - gap * (i - 1)
        c.drawString(start_x, y, f"{i}． {a} + {b}")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return Response(
        pdf_bytes,
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=addition_print.pdf"
        }
    )
