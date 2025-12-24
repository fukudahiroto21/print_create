# api/index.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import base64

def handler(request):
    # PDFをメモリ上に作成
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(595, 842))  # A4縦

    # PNG背景を載せる場合
    img = ImageReader("assets/School Print.png")
    c.drawImage(img, 0, 0, width=595, height=842)

    # 日本語フォント埋め込み
    pdfmetrics.registerFont(TTFont("IPAexGothic", "assets/ipaexg.ttf"))
    c.setFont("IPAexGothic", 24)
    c.drawString(100, 800, "こんにちは、世界！")

    c.showPage()
    c.save()

    # PDFをbase64に変換
    pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=output.pdf"
        },
        "body": pdf_base64,
        "isBase64Encoded": True
    }
