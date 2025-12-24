# api/index.py
import os
from io import BytesIO
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from flask import Flask, send_file, Response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def generate_pdf():
    try:
        # ファイルパス
        base_dir = os.path.dirname(__file__)
        png_path = os.path.join(base_dir, "assets/School Print.png")
        font_path = os.path.join(base_dir, "assets/ipaexg.ttf")

        # フォント登録
        pdfmetrics.registerFont(TTFont("IpaExG", font_path))

        # PDF バッファ
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        width, height = landscape(A4)

        # フォント設定
        c.setFont("IpaExG", 14)
        c.drawString(50, height - 50, "日本語テスト")

        # PNG を読み込んでページにフィットさせる
        img = Image.open(png_path)
        img_width, img_height = img.size
        scale = min(width / img_width, height / img_height)
        draw_width = img_width * scale
        draw_height = img_height * scale
        x = (width - draw_width) / 2
        y = (height - draw_height) / 2
        c.drawImage(png_path, x, y, draw_width, draw_height)

        c.showPage()
        c.save()
        buffer.seek(0)

        # PDF を返す
        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="output.pdf"
        )

    except Exception as e:
        return Response(f"Error: {e}", status=500)

