from io import BytesIO
import os
import random

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def handler(request):
    # ===== PDF基本設定 =====
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    # ===== パス解決 =====
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    assets_dir = os.path.join(project_root, "assets")

    png_path = os.path.join(assets_dir, "School Print.png")
    font_path = os.path.join(assets_dir, "ipaexg.ttf")

    # ===== 背景PNG =====
    if os.path.exists(png_path):
        bg = ImageReader(png_path)
        c.drawImage(
            bg,
            0,
            0,
            width=page_width,
            height=page_height
        )

    # ===== 日本語フォント =====
    pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
    c.setFont("IPAexGothic", 22)

    # ===== 問題生成（10問） =====
    problem_count = 10
    min_num = 1
    max_num = 20

    problems = [
        (random.randint(min_num, max_num),
         random.randint(min_num, max_num))
        for _ in range(problem_count)
    ]

    # ===== レイアウト =====
    top_y = page_height - 140
    bottom_y = 120
    usable_height = top_y - bottom_y
    line_gap = usable_height / (problem_count - 1)

    start_x = 140

    # ===== 問題描画 =====
    for i, (a, b) in enumerate(problems, start=1):
        y = top_y - line_gap * (i - 1)
        text = f"{i}． {a} + {b}"
        c.drawString(start_x, y, text)

    # ===== PDF確定 =====
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    # ===== レスポンス =====
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=addition_print.pdf"
        },
        "body": pdf_bytes
    }
