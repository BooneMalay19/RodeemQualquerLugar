import win32gui
import win32ui
import win32con
import win32api
from flask import Flask, Response
from PIL import Image
import io

app = Flask(__name__)

# Nome correto da janela do Doom
DOOM_WINDOW_TITLE = 'DOOM Shareware - Chocolate Doom 3.1.0'

def capture_window(title):
    hwnd = win32gui.FindWindow(None, title)
    if not hwnd:
        print("❌ Janela do DOOM não encontrada.")
        return None

    # Obter dimensões da janela
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # Captura via GDI
    hwindc = win32gui.GetWindowDC(hwnd)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (0, 0), win32con.SRCCOPY)

    # Convertendo para imagem PIL
    bmpinfo = bmp.GetInfo()
    bmpstr = bmp.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    # Cleanup
    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img

# Gera os frames pra transmissão
def generate_frames():
    while True:
        img = capture_window(DOOM_WINDOW_TITLE)
        if img is None:
            import time
            time.sleep(3)
            continue

        # Codifica como JPEG
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        frame = buf.getvalue()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Rota do vídeo
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Página simples
@app.route('/')
def index():
    return '''
    <html>
    <body style="margin: 0; padding: 0; overflow: hidden;">
        <img src="/video_feed" style="width: 100vw; height: 100vh; object-fit: cover;">
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
