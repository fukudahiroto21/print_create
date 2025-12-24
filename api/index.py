from flask import Flask, make_response
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
import os

# Flaskアプリのインスタンス化
app = Flask(__name__)

@app.route('/api')
def handler():
    # 1. PDFをメモリ上に作成（横向きA4）
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)

    # 2. アセットのパス設定
    base_path = os.path.join(os.path.dirname(__file__), "../assets")
    png_path = os.path.join(base_path, "School Print.png")
    font_path = os.path.join(base_path, "ipaexg.ttf")

    # 3. 背景画像を載せる（ファイル確認付き）
    if os.path.exists(png_path):
        img = ImageReader(png_path)
        c.drawImage(img, 0, 0, width=page_width, height=page_height)

    # 4. 日本語フォント設定と描画（ファイル確認付き）
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
        c.setFont("IPAexGothic", 24)
        c.drawString(50, page_height - 50, "こんにちは、世界！")
    else:
        # フォントがない場合のデバッグ用テキスト
        c.setFont("Helvetica", 24)
        c.drawString(50, page_height - 50, "Font file not found.")

    c.showPage()
    c.save()
    
    # 5. PDFデータを取得してバッファを閉じる
    pdf_value = buffer.getvalue()
    buffer.close()

    # 6. Flaskのレスポンスを作成
    response = make_response(pdf_value)
    
    # ヘッダーを明示的に設定
    response.headers['Content-Type'] = 'application/pdf'
    # inlineにすることでブラウザで開く。filenameで保存時の名前を指定。
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    
    return response

# Vercelでは不要ですが、ローカル実行用に
if __name__ == "__main__":
    app.run(debug=True)
