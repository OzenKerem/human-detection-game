# Human Detection Game 🎮 👥

An interactive real-time human detection game that uses computer vision and artificial intelligence to detect people through your camera and randomly select one person with fun animations and sound effects!

## 🌟 Features

- Real-time human detection using YOLOv5
- Live camera feed processing
- Person counting and tracking
- Random person selection with animations
- Sound effects for selection events
- Beautiful UI with dynamic animations
- Full-screen display mode

## 🛠️ Technologies Used

- **Python 3.8+**
- **YOLOv5**: State-of-the-art object detection
- **OpenCV**: Real-time image processing
- **PyTorch**: Deep learning framework
- **Pygame**: Sound effects handling
- **NumPy**: Numerical computations
- **Pandas**: Data handling

## 📋 Prerequisites

Before running this project, make sure you have:
- Python 3.8 or higher installed
- A working webcam
- Sufficient disk space for the YOLOv5 model

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/OzenKerem/human-detection-game.git
cd human-detection-game
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download the YOLOv5 model weights (this happens automatically on first run)

## 💻 Usage

1. Make sure your webcam is connected and working
2. Run the main script:
```bash
python human_detection.py
```

3. Stand in front of the camera and wait for detections
4. The program will:
   - Detect all people in the frame
   - Display the count of detected people
   - After a few seconds, randomly select one person
   - Show an animation highlighting the selected person
   - Play a sound effect

## 🎮 Game Modes

### 1. Scanning Mode
- Detects and displays all people in the frame
- Shows person count
- Lists all detected people
- Waits for stable detection

### 2. Selection Mode
- Randomly selects one person
- Shows full-screen animation
- Plays sound effect
- Displays "SELECTED!" message
- Uses dynamic red color animations

## ⚙️ Configuration

The program uses several default settings that can be modified in the code:
- Window size: 1280x720
- Frame wait time: 3 seconds
- Animation speed
- Colors and effects

## 📁 Project Structure

```
human-detection-game/
│
├── human_detection.py     # Main application file
├── requirements.txt       # Python dependencies
├── ses.mp3               # Sound effect file
├── yolov5s.pt           # YOLOv5 model weights
│
└── output_frames/        # Directory for saved frames
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- YOLOv5 team for the amazing object detection model
- OpenCV community for computer vision tools
- PyTorch team for the deep learning framework

## 📧 Contact

For questions and feedback, please open an issue in the GitHub repository.

---
Made with ❤️ by [OzenKerem](https://github.com/OzenKerem)