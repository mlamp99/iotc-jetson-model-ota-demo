import cv2
import onnxruntime as ort
import numpy as np
import os
import json
import socket

# Path setup
MODEL_DIR = "/var/snap/iotconnect/common/models"
MODEL_PATH = os.path.join(MODEL_DIR, "mobilenet.onnx")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.txt")
SOCKET_PATH = "/var/snap/iotconnect/common/iotc.sock"

# Load labels
with open(LABELS_PATH, "r") as f:
    labels = [line.strip() for line in f]

# Load ONNX model
session = ort.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name

# Initialize camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Could not open /dev/video0")

print("Running inference. Press Ctrl+C to stop.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Preprocess frame
        img = cv2.resize(frame, (224, 224)).astype(np.float32) / 255.0
        img = (img - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
        img = np.transpose(img, (2, 0, 1)).reshape(1, 3, 224, 224)

        # Inference
        output = session.run(None, {input_name: img})[0]
        class_id = int(np.argmax(output))
        confidence = float(np.max(output))

        label = labels[class_id] if class_id < len(labels) else f"class_{class_id}"
        result = {"label": label, "confidence": round(confidence, 3)}

        print("Detected:", result)

        # Send result over socket
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(SOCKET_PATH)
            sock.send(json.dumps(result).encode())
            sock.close()
        except Exception as e:
            print("Socket error:", e)

        if cv2.waitKey(1000) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()