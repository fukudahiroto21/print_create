from http.server import BaseHTTPRequestHandler
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import io
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base_dir = os.getcwd()
        img_path = os.path.join(base_dir, "assets", "School_Print.png")
        font_path = os.path.join(base_dir, "assets", "ipaexg.ttf")

        # PNGサイズ取得
        img = Image.open(img_path)
        width, height = img.size

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))

        # フォント登録（＝埋め込み）
        pdfmetrics.registerFont(
            TTFont("IPAexGothic", font_path)
        )

        # 背景画像
        c.drawImage(
            ImageReader(img_path),
            0, 0,
            width=width,
            height=height,
            mask="auto"
        )

        # フォント指定
        c.setFont("IPAexGothic", 60)

        # 日本語テキスト描画
        c.drawString(120, height - 200, "なまえ：")
        c.drawString(120, height - 300, "５ + ３ =")

        c.showPage()
        c.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()

        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header(
            "Content-Disposition",
            'attachment; filename="print.pdf"'
        )
        self.end_headers()
        self.wfile.write(pdf_bytes)
