from flask import Flask, make_response
from io import BytesIO
import os
import random

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)


@app.route("/api")
def generate_pdf():
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
        c.drawImage(bg, 0, 0, width=page_width, height=page_height)

    # ===== 日本語フォント =====
    pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
    c.setFont("IPAexGothic", 22)

    # ===== 問題生成（10問） =====
    problems = [
        (random.randint(1, 20), random.randint(1, 20))
        for _ in range(10)
    ]

    # ===== レイアウト =====
    rows = 5
    cols = 2
    
    top_y = page_height - 140
    bottom_y = 120
    rowgap = (top_y - bottom_y) / 9
    start_x = 140

    # ===== 問題描画 =====
    for i, (a, b) in enumerate(problems, start=1):
        y = top_y - gap * (i - 1)
        c.drawString(start_x, y, f"{i}． {a} + {b}")

    # ===== PDF確定 =====
    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()

    # ===== Flaskレスポンス =====
    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=addition_print.pdf"

    return response


# ローカル確認用（Vercelでは実行されない）
if __name__ == "__main__":
    app.run(debug=True)
