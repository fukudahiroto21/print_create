# api/index.py
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def handler(request):
    # PDFをメモリ上に作成
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(595, 842))  # A4縦

    # 日本語フォント埋め込み
    pdfmetrics.registerFont(TTFont("IPAexGothic", "assets/ipaexg.ttf"))
    c.setFont("IPAexGothic", 24)
    c.drawString(100, 800, "こんにちは、世界！")

    # PNG背景を載せる場合
    from reportlab.lib.utils import ImageReader
    img = ImageReader("assets/School Print.png")
    c.drawImage(img, 0, 0, width=595, height=842)

    c.showPage()
    c.save()
    buffer.seek(0)

    # HTTPレスポンスとして返す
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=output.pdf"
        },
        "body": buffer.getvalue(),
        "isBase64Encoded": True  # Vercelでバイナリ返却するために必須
    }
