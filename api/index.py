from http.server import BaseHTTPRequestHandler
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import io
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # PNG のパス（リポジトリ直下基準）
        img_path = os.path.join("assets", "School Print.png")

        # PDF をメモリ上で生成
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        img = ImageReader(img_path)
        page_width, page_height = A4

        # 画像をページいっぱいに配置（比率はそのまま）
        c.drawImage(
            img,
            0, 0,
            width=page_width,
            height=page_height,
            preserveAspectRatio=True,
            mask='auto'
        )

        c.showPage()
        c.save()

        pdf_bytes = buffer.getvalue()
        buffer.close()

        # レスポンス
        self.send_response(200)
        self.send_header("Content-Type", "application/pdf")
        self.send_header(
            "Content-Disposition",
            'attachment; filename="output.pdf"'
        )
        self.end_headers()
        self.wfile.write(pdf_bytes)
