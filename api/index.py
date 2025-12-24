from flask import Flask, make_response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
import os

app = Flask(__name__)

@app.route('/api')
def handler():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    # パス解決（Vercel環境では絶対パスを取得）
    current_dir = os.path.dirname(__file__)
    png_path = os.path.abspath(os.path.join(current_dir, "../assets/School Print.png"))
    font_path = os.path.abspath(os.path.join(current_dir, "../assets/ipaexg.ttf"))

    try:
        # PNG背景の描画
        if os.path.exists(png_path):
            img = ImageReader(png_path)
            c.drawImage(img, 0, 0, width=page_width, height=page_height)
        else:
            c.drawString(50, page_height - 100, f"Missing Image: {png_path}")

        # 日本語フォント設定
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
            c.setFont("IPAexGothic", 24)
            c.drawString(50, page_height - 50, "こんにちは、世界！")
        else:
            c.setFont("Helvetica", 24)
            c.drawString(50, page_height - 50, "Font not found, using Helvetica")

    except Exception as e:
        # 万が一の描画エラー時
        c.setFont("Helvetica", 12)
        c.drawString(50, 50, f"Error: {str(e)}")

    c.showPage()
    c.save()
    
    pdf_value = buffer.getvalue()
    buffer.close()

    response = make_response(pdf_value)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    return response

# Vercelが関数を認識するために必要
app.debug = True
