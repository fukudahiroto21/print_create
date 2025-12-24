# api/index.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
import os

def handler(request):
    # PDFをメモリ上に作成（横向きA4）
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))  # 横向き

    # assetsフォルダのパスを計算（apiから見た相対パス）
    base_path = os.path.join(os.path.dirname(__file__), "../assets")
    png_path = os.path.join(base_path, "School Print.png")
    font_path = os.path.join(base_path, "ipaexg.ttf")

    # PNG背景を載せる
    img = ImageReader(png_path)
    page_width, page_height = landscape(A4)
    c.drawImage(img, 0, 0, width=page_width, height=page_height)

    # 日本語フォント埋め込み
    pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
    c.setFont("IPAexGothic", 24)
    c.drawString(50, page_height - 50, "こんにちは、世界！")  # 左上に文字

    c.showPage()
    c.save()
    buffer.seek(0)

    # PDFを直接返す（Base64変換不要）
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=output.pdf"
        },
        "body": buffer.getvalue()
    }
