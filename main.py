import cv2
from model_loader import muat_model
from counter import PenghitungBotol

SUMBER_VIDEO = "Botol2.mp4"
BATAS_THRESHOLD = 0.5

print("\nPenghitungan Botol YOLOv8 (Tanpa Tracking ID)")
print("➡ Tekan tombol 'Q' untuk keluar.\n")

model = muat_model("yolov8n.pt")

penghitung = PenghitungBotol()

video = cv2.VideoCapture(SUMBER_VIDEO)

fps = int(video.get(cv2.CAP_PROP_FPS))
lebar = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
tinggi = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

print(f"FPS Video       : {fps}")
print(f"Resolusi Video  : {lebar} x {tinggi}")

cv2.namedWindow("Penghitung Botol YOLOv8", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Penghitung Botol YOLOv8", lebar, tinggi)

while True:
    berhasil, frame = video.read()
    if not berhasil:
        break

    daftar_deteksi = []

    hasil = model.predict(
        frame,
        conf=BATAS_THRESHOLD,
        imgsz=416,
        classes=[39], 
        stream=False
    )

    for deteksi in hasil:
        for box in deteksi.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            daftar_deteksi.append([x1, y1, x2, y2])

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    frame = penghitung.perbarui(frame, daftar_deteksi)

    cv2.imshow("Penghitung Botol", frame)

    if cv2.waitKey(int(1000 / fps)) & 0xFF in (ord('q'), ord('Q')):
        break

video.release()
cv2.destroyAllWindows()

print(f"\nTotal Botol Terdeteksi: {penghitung.jumlah}")