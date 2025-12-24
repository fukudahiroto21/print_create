from http.server import BaseHTTPRequestHandler
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from PIL import Image

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # PNGパス
        img_path = os.path.join("assets", "School Print.png")

        # PNGをPillowで読み込み
        img = Image.open(img_path)
        width_px, height_px = img.size

        # PDFをPNGと同じサイズで作成
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width_px, height_px))

        pdf_img = ImageReader(img_path)

        # 左下(0,0)からピッタリ描画
        c.drawImage(
            pdf_img,
            0, 0,
            width=width_px,
            height=height_px,
            mask="auto"
        )

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
