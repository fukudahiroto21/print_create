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
    # 1. PDFをメモリ上に作成
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    # 2. パスの設定
    # Vercel環境ではプロジェクトルートからの相対パスに注意が必要
    base_path = os.path.join(os.path.dirname(__file__), "../assets")
    png_path = os.path.join(base_path, "School Print.png")
    font_path = os.path.join(base_path, "ipaexg.ttf")

    # 3. 背景画像の描画（ファイルが存在する場合のみ）
    if os.path.exists(png_path):
        img = ImageReader(png_path)
        c.drawImage(img, 0, 0, width=page_width, height=page_height)

    # 4. フォントの設定と描画（ファイルが存在する場合のみ）
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
        c.setFont("IPAexGothic", 24)
        c.drawString(50, page_height - 50, "こんにちは、世界！")
    else:
        # フォントがない場合の予備
        c.setFont("Helvetica", 24)
        c.drawString(50, page_height - 50, "Font not found. Hello!")

    c.showPage()
    c.save()
    
    # 5. レスポンスの作成
    pdf_value = buffer.getvalue()
    buffer.close()

    response = make_response(pdf_value)
    response.headers['Content-Type'] = 'application/pdf'
    # inlineにすることで、ブラウザで直接開くように指示します
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    return response

# ローカルデバッグ用
if __name__ == "__main__":
    app.run(debug=True)
