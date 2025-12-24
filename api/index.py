from flask import Flask, make_response, jsonify
import os
import sys
import traceback

app = Flask(__name__)

def get_asset_paths():
    """アセットファイルのパスを取得"""
    try:
        current_file = os.path.abspath(__file__)
        api_dir = os.path.dirname(current_file)
        project_root = os.path.dirname(api_dir)
        assets_dir = os.path.join(project_root, "assets")
        
        return {
            'current_file': current_file,
            'api_dir': api_dir,
            'project_root': project_root,
            'assets_dir': assets_dir,
            'png_path': os.path.join(assets_dir, "School Print.png"),
            'font_path': os.path.join(assets_dir, "ipaexg.ttf")
        }
    except Exception as e:
        return {
            'error': str(e),
            'traceback': traceback.format_exc()
        }

@app.route('/')
@app.route('/api')
def index():
    """メインのPDF生成エンドポイント"""
    try:
        from io import BytesIO
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, landscape
        
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        page_width, page_height = landscape(A4)
        
        # パス取得
        paths = get_asset_paths()
        
        if 'error' in paths:
            c.setFont("Helvetica", 12)
            c.drawString(50, page_height - 50, f"Path error: {paths['error']}")
            c.showPage()
            c.save()
            pdf_value = buffer.getvalue()
            buffer.close()
            response = make_response(pdf_value)
            response.headers['Content-Type'] = 'application/pdf'
            return response
        
        png_path = paths['png_path']
        font_path = paths['font_path']
        
        # デバッグログ
        print("="*50)
        print("PDF Generation Started")
        print(f"PNG exists: {os.path.exists(png_path)}")
        print(f"Font exists: {os.path.exists(font_path)}")
        if os.path.exists(paths['assets_dir']):
            print(f"Assets contents: {os.listdir(paths['assets_dir'])}")
        print("="*50)
        
        # PNG背景の描画
        if os.path.exists(png_path):
            from reportlab.lib.utils import ImageReader
            print("Drawing PNG background...")
            img = ImageReader(png_path)
            c.drawImage(img, 0, 0, width=page_width, height=page_height)
            print("PNG drawn successfully")
        else:
            print("PNG not found")
            c.setFont("Helvetica", 10)
            y_pos = page_height - 100
            c.drawString(50, y_pos, f"Missing Image: {png_path}")
            y_pos -= 20
            if os.path.exists(paths['assets_dir']):
                contents = str(os.listdir(paths['assets_dir']))[:80]
                c.drawString(50, y_pos, f"Assets: {contents}")
        
        # 日本語フォント設定
        if os.path.exists(font_path):
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            print("Registering Japanese font...")
            pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
            c.setFont("IPAexGothic", 24)
            c.drawString(50, page_height - 50, "こんにちは、世界!")
            print("Font registered successfully")
        else:
            print("Font not found")
            c.setFont("Helvetica", 24)
            c.drawString(50, page_height - 50, "Font not found, using Helvetica")
            
        c.showPage()
        c.save()
        
        pdf_value = buffer.getvalue()
        buffer.close()
        
        print("PDF generation completed")
        
        response = make_response(pdf_value)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        
        return response
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/debug')
def debug():
    """デバッグ情報"""
    try:
        paths = get_asset_paths()
        
        if 'error' in paths:
            return jsonify(paths), 500
        
        debug_info = {
            'status': 'debug working',
            'cwd': os.getcwd(),
            'paths': {
                'project_root': paths['project_root'],
                'assets_dir': paths['assets_dir'],
                'png': paths['png_path'],
                'font': paths['font_path']
            },
            'exists': {
                'assets_dir': os.path.exists(paths['assets_dir']),
                'png': os.path.exists(paths['png_path']),
                'font': os.path.exists(paths['font_path'])
            },
            'contents': {}
        }
        
        if os.path.exists(paths['assets_dir']):
            debug_info['contents']['assets'] = os.listdir(paths['assets_dir'])
        if os.path.exists(paths['project_root']):
            debug_info['contents']['project_root'] = os.listdir(paths['project_root'])
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test')
def test():
    """テストエンドポイント"""
    return jsonify({
        'status': 'ok',
        'message': 'API is working',
        'python_version': sys.version
    })

# ローカル開発用
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
