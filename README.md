# ✋ Hand Gesture Volume Controller

A real-time hand gesture system volume controller using Python, MediaPipe, and Pycaw.
By detecting the distance between your thumb and index finger, you can intuitively control the system volume — no touch required!

---

## 📷 Preview
<p align="center">
  <img src="https://github.com/amberyliang/Hand-Gesture-Volume-Controller/blob/main/demo.jpg" width="500">
</p>

---

## 🔧 Technologies Used
- [MediaPipe](https://google.github.io/mediapipe/) – real-time hand landmark detection
- [OpenCV](https://opencv.org/) – camera capture & visualization
- [pycaw](https://github.com/AndreMiras/pycaw) – Windows system volume control via Core Audio API
- Python 3.x

---

## 🖥️ Features
- Real-time hand tracking and gesture recognition
- Maps hand distance to system volume (0% – 100%)
- Visual feedback via volume percentage and landmark overlays

---

## 🚀 Getting Started

### 1️⃣ Install Dependencies
```bash
pip install opencv-python mediapipe pycaw comtypes
```

### 2️⃣ Run the Script
```bash
python hand_volume_control.py
```

> ⚠️ This project requires a local machine with a webcam. It does not run in cloud environments like Google Colab.

---

## 📁 Project Structure
```
hand-volume-controller/
├── hand_volume_control.py    # Main script
├── README.md                 # Project documentation

```

---

## 🙋‍♀️ Author
Made with 💡 by Yu-Jung, Liang — built as a creative exploration into computer vision + HCI.

---

## 📄 License
This project is licensed under the MIT License.
