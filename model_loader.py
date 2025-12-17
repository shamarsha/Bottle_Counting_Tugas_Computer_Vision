from ultralytics import YOLO

def muat_model(nama_model="yolov8n.pt"):
    """Memuat model YOLO berdasarkan file yang diberikan."""
    
    print(f"Sedang memuat model: {nama_model} ...")
    model = YOLO(nama_model)
    print("Model berhasil dimuat!")
    
    return model