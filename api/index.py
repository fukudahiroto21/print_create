from flask import Flask, send_file, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
import io
from PIL import Image

app = Flask(__name__)

@app.route("/", methods=["GET"])
def generate_pdf():
    # PDF をメモリ上に作成
    buffer = io.BytesIO()
    
    # A4横サイズに設定
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    # PNG を背景にする場合
    try:
        img = Image.open("assets/School Print.png")  # assets フォルダに置いた画像
        img_width, img_height = img.size
        # ReportLab は左下原点、サイズをポイントに変換
        c.drawImage("assets/School Print.png", 0, 0, width=img_width, height=img_height)
    except Exception as e:
        print("画像読み込み失敗:", e)
    
    # 文字を書き込み（フォント埋め込み）
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    pdfmetrics.registerFont(TTFont("IPAexGothic", "assets/ipaexg.ttf"))
    
    c.setFont("IPAexGothic", 24)
    c.drawString(100, 200, "こんにちは、世界！")  # サンプル文字
    c.showPage()
    c.save()

    buffer.seek(0)
    response = make_response(send_file(buffer, mimetype="application/pdf", download_name="output.pdf"))
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"  # ブラウザで開く
    return response

# Vercel は app を自動で認識
app = app
