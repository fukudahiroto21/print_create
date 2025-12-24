# api/index.py
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image

def handler(request, response):
    # PDF を作成
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))

    # PNG を背景にする
    try:
        img = Image.open("assets/School Print.png")
        img_width, img_height = img.size
        c.drawImage("assets/School Print.png", 0, 0, width=img_width, height=img_height)
    except Exception as e:
        print("画像読み込み失敗:", e)

    # フォント埋め込み
    pdfmetrics.registerFont(TTFont("IPAexGothic", "assets/ipaexg.ttf"))
    c.setFont("IPAexGothic", 24)
    c.drawString(100, 200, "こんにちは、世界！")
    c.showPage()
    c.save()

    buffer.seek(0)
    response.setHeader("Content-Type", "application/pdf")
    response.setHeader("Content-Disposition", "inline; filename=output.pdf")
    response.send(buffer.getvalue())
