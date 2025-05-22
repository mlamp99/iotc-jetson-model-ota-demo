# Jetson Model OTA Demo

This project demonstrates:
- ONNX modela inference on NVIDIA Jetson (JetPack 5)
- Communication with an IoTConnect-enabled Snap via Unix socket
- OTA model updates delivered via IoTConnect

## 📦 Setup

```bash
python3 -m venv ai-env
source ai-env/bin/activate
pip install -r requirements.txt
```

## 🧠 Running the Inference Script

Ensure your Snap is installed and the socket service is running:

```bash
sudo snap start iotconnect.socket
```

Then run the script:

```bash
python3 mobilenet_infer.py
```

You should see classification output and MQTT messages from the Snap.

## 🗂️ Model Files

Place your ONNX model and labels in:

```
/var/snap/iotconnect/common/models/
```

Example:
```
/var/snap/iotconnect/common/models/mobilenet.onnx
/var/snap/iotconnect/common/models/labels.txt
```

## 📤 OTA Model Update

To create an OTA payload for IoTConnect:

```bash
cd model
tar -czvf ../ota/mobilenet-ota.tar.gz mobilenet.onnx labels.txt config.json
```

Upload the `.tar.gz` to a public URL or S3 and trigger an OTA command from the IoTConnect portal.

---

## 📎 Snap Socket Path

This script communicates with the Snap via:
```
/var/snap/iotconnect/common/iotc.sock
```

Make sure the Snap is listening and your device has access to this path.