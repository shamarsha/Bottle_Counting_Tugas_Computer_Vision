import cv2
import cvzone

class PenghitungBotol:
    """
    Counter BOTOL PALING AMAN
    - 1 garis
    - tanpa tracking
    - 1 botol = +1 
    """

    def __init__(self):
        self.jumlah = 0
        self.garis_x = None

        self.botol_dalam_proses = False  

    def gambar_garis(self, frame):
        h, w, _ = frame.shape
        if self.garis_x is None:
            self.garis_x = int(w * 0.30)

        cv2.line(
            frame,
            (self.garis_x, 0),
            (self.garis_x, h),
            (255, 0, 0),
            5
        )

    def perbarui(self, frame, daftar_objek):
        self.gambar_garis(frame)

        garis = self.garis_x
        toleransi = 15  

        ada_di_garis = False
        ada_jauh_kanan = False

        for (x1, y1, x2, y2) in daftar_objek:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            if abs(cx - garis) <= toleransi:
                ada_di_garis = True

            if cx > garis + 2 * toleransi:
                ada_jauh_kanan = True


        if ada_di_garis and not self.botol_dalam_proses:
            self.jumlah += 1
            self.botol_dalam_proses = True

        if ada_jauh_kanan and not ada_di_garis:
            self.botol_dalam_proses = False

        cvzone.putTextRect(
            frame,
            f"Jumlah: {self.jumlah}",
            (30, 50),
            scale=2,
            thickness=2,
            colorR=(255, 0, 255)
        )

        return frame