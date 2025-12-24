from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image
import base64
import os

def handler(request):
    try:
        # PNG 読み込み
        assets_path = os.path.join(os.path.dirname(__file__), '../assets/School Print.png')
        bg_image = Image.open(assets_path)
        width, height = bg_image.size

        # PDF 作成（横向き）
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))

        # 日本語フォント埋め込み
        font_path = os.path.join(os.path.dirname(__file__), '../assets/ipaexg.ttf')
        pdfmetrics.registerFont(TTFont('IPAexG', font_path))
        c.setFont("IPAexG", 24)

        # PNG を PDF に描画
        c.drawImage(ImageReader(bg_image), 0, 0, width=width, height=height)

        # サンプル文字
        c.drawString(50, height - 50, "こんにちは、Vercel PDF!")

        c.showPage()
        c.save()

        pdf_data = buffer.getvalue()
        buffer.close()

        # Base64 エンコード
        encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Content-Disposition": "inline; filename=output.pdf"
            },
            "body": encoded_pdf,
            "isBase64Encoded": True
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
