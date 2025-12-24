from flask import Flask, make_response, jsonify
import os
import sys
import traceback

app = Flask(__name__)

# Vercel用のエラーハンドリング
@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({
        'error': str(e),
        'traceback': traceback.format_exc(),
        'type': type(e).__name__
    }), 500

def get_asset_paths():
    """アセットファイルのパスを取得"""
    # api/index.py の位置を基準にする
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

@app.route('/api/debug')
def debug():
    """デバッグ情報を表示"""
    try:
        paths = get_asset_paths()
        
        debug_info = {
            'current_working_directory': os.getcwd(),
            'current_file': paths['current_file'],
            'api_directory': paths['api_dir'],
            'project_root': paths['project_root'],
            'assets_directory': paths['assets_dir'],
            'paths': {
                'png': paths['png_path'],
                'font': paths['font_path']
            },
            'exists': {
                'api_dir': os.path.exists(paths['api_dir']),
                'project_root': os.path.exists(paths['project_root']),
                'assets_dir': os.path.exists(paths['assets_dir']),
                'png': os.path.exists(paths['png_path']),
                'font': os.path.exists(paths['font_path'])
            },
            'directory_contents': {}
        }
        
        # 各ディレクトリの内容を取得
        for key in ['api_dir', 'project_root', 'assets_dir']:
            dir_path = paths[key]
            if os.path.exists(dir_path):
                try:
                    debug_info['directory_contents'][key] = os.listdir(dir_path)
                except Exception as e:
                    debug_info['directory_contents'][key] = f"Error: {str(e)}"
            else:
                debug_info['directory_contents'][key] = "Directory does not exist"
        
        return jsonify(debug_info)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api')
def handler():
    """PDF生成エンドポイント"""
    try:
        from io import BytesIO
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, landscape
        
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=landscape(A4))
        page_width, page_height = landscape(A4)
        
        # パス取得
        paths = get_asset_paths()
        png_path = paths['png_path']
        font_path = paths['font_path']
        
        # デバッグログ出力（Vercelのログに記録される）
        print("="*50)
        print("PDF Generation Started")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Project root: {paths['project_root']}")
        print(f"Assets directory: {paths['assets_dir']}")
        print(f"PNG path: {png_path}")
        print(f"PNG exists: {os.path.exists(png_path)}")
        print(f"Font path: {font_path}")
        print(f"Font exists: {os.path.exists(font_path)}")
        
        if os.path.exists(paths['assets_dir']):
            print(f"Assets directory contents: {os.listdir(paths['assets_dir'])}")
        else:
            print("Assets directory does not exist!")
        print("="*50)
        
        # PNG背景の描画
        if os.path.exists(png_path):
            from reportlab.lib.utils import ImageReader
            print("Drawing PNG background...")
            img = ImageReader(png_path)
            c.drawImage(img, 0, 0, width=page_width, height=page_height)
            print("PNG background drawn successfully")
        else:
            print("PNG file not found, drawing error message")
            c.setFont("Helvetica", 10)
            y_pos = page_height - 100
            c.drawString(50, y_pos, f"Missing Image: {png_path}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Assets dir exists: {os.path.exists(paths['assets_dir'])}")
            y_pos -= 20
            if os.path.exists(paths['assets_dir']):
                c.drawString(50, y_pos, f"Assets contents: {os.listdir(paths['assets_dir'])}")
            y_pos -= 20
            c.drawString(50, y_pos, f"Project root: {paths['project_root']}")
        
        # 日本語フォント設定
        if os.path.exists(font_path):
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            print("Registering Japanese font...")
            pdfmetrics.registerFont(TTFont("IPAexGothic", font_path))
            c.setFont("IPAexGothic", 24)
            c.drawString(50, page_height - 50, "こんにちは、世界!")
            print("Japanese text drawn successfully")
        else:
            print("Font file not found, using Helvetica")
            c.setFont("Helvetica", 24)
            c.drawString(50, page_height - 50, "Font not found, using Helvetica")
            c.setFont("Helvetica", 10)
            c.drawString(50, page_height - 80, f"Font path: {font_path}")
            
        c.showPage()
        c.save()
        
        pdf_value = buffer.getvalue()
        buffer.close()
        
        print("PDF generation completed")
        print("="*50)
        
        response = make_response(pdf_value)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        
        return response
        
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/test')
def test():
    """簡易テストエンドポイント"""
    return jsonify({
        'status': 'ok',
        'message': 'API is working',
        'python_version': sys.version,
        'cwd': os.getcwd(),
        '__file__': __file__
    })

# ローカル開発用
if __name__ == '__main__':
    app.run(debug=True, port=5000)
