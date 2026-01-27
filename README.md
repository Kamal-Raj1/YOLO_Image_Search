# YOLO-Powered Image Search Application

An intelligent image retrieval system that reduces manual annotation effort through automated object detection and flexible query-based search.

## 🎯 Project Overview

This application streamlines computer vision dataset curation by:
- Automatically detecting objects in images using YOLOv11
- Generating searchable metadata for each image
- Enabling fast, filter-based image search
- Visualizing bounding boxes interactively
- Exporting selected images for annotation workflows

## ✨ Key Features

### 1. Automated Object Detection
- Uses YOLOv11 for accurate object detection
- Generates JSON metadata containing:
  - Detected objects and their classes
  - Bounding box coordinates
  - Confidence scores
  - Per-class object counts

### 2. Flexible Search System
- **Boolean Logic Queries**: Search using AND/OR operators
  - AND: Find images containing ALL specified objects
  - OR: Find images containing ANY specified objects
- **Count-Based Filters**: Filter by number of objects
  - Example: "Find images with at least 3 people"
  - Example: "Show images with exactly 1 car"

### 3. Interactive Interface
- Built with Streamlit for easy use
- Real-time bounding box visualization
- Toggle detection overlays on/off
- Preview images before selection
- Batch export selected images

### 4. Streamlined Workflow
- Automates object detection across large image datasets
- Enables rapid filtering through boolean queries and count constraints
- Reduces manual dataset curation time compared to image-by-image review

## 🚀 Installation

### Prerequisites
```bash
Python 3.8+
pip
```

### Setup
```bash
# Clone the repository
git clone https://github.com/Kamal-Raj1/YOLO_Image_Search.git
cd YOLO_Image_Search

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Run the Application
```bash
streamlit run app.py
```

### Using the Interface
1. **Upload Images**: Select your image dataset folder
2. **Configure Detection**: Set confidence threshold (default: 0.35)
3. **Run Detection**: Process images with YOLOv11s
4. **Search & Filter**:
   - Select search mode (AND/OR)
   - Enter object classes (e.g., "person, car, dog")
   - Set count filters (optional)
5. **View Results**: Browse matching images with bounding boxes
6. **Export**: Select and export images for annotation

## 🏗️ Project Structure

```
YOLO_Image_Search/
├── app.py                    # Main Streamlit application
├── configs/
│   └── default.yaml         # Configuration file (model settings, paths)
├── src/
│   ├── __init__.py
│   ├── config.py            # Configuration loader
│   ├── inference.py         # YOLOv11 detection engine
│   └── utils.py             # Helper functions (search, visualization)
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md                # This file
```

## 🔧 Technical Details

### YOLOv11 Configuration
- **Model**: YOLOv11s (small) - balanced speed and accuracy
- **Confidence Threshold**: 0.35 (adjustable in config)
- **Supported Formats**: JPG, JPEG, PNG

### Configuration File (`configs/default.yaml`)
```yaml
model:
  model_name: "yolo11s.pt"
  conf_threshold: 0.35

data:
  image_extensions: [".jpg", ".jpeg", ".png"]
```

### Search Algorithm
- Boolean AND: Intersection of object sets
- Boolean OR: Union of object sets
- Count filtering: Post-processing after boolean logic
- Time complexity: O(n) where n = number of images

## 📊 Example Use Cases

### Use Case 1: Dataset Curation for Object Detection
**Goal**: Find training images with multiple people for the crowd detection model

**Steps**:
1. Run detection on your dataset
2. Search for "person" with count filter: minimum 3
3. Export filtered images with multiple people

### Use Case 2: Quality Control
**Goal**: Verify detection accuracy by reviewing specific object classes

**Steps**:
1. Search for a specific class (e.g., "car")
2. Review bounding boxes visually
3. Identify false positives/negatives

### Use Case 3: Balanced Dataset Creation
**Goal**: Create a balanced dataset with single-object images

**Steps**:
1. Set count filter: exactly 1 object
2. Export selected images per class
3. Build a balanced dataset for classification

## ⚡ Performance Characteristics

- **Detection**: Efficient inference with YOLOv11s model
- **Search Speed**: Near-instant metadata-based filtering
- **Scalability**: Handles large image datasets efficiently
- **Detection Classes**: 80 object categories from the COCO dataset
- **Memory Footprint**: Lightweight metadata storage

## 🎓 Key Learnings

1. **Automation Impact**: Automated detection eliminates repetitive manual review
2. **User Experience**: Interactive visualization makes dataset exploration intuitive
3. **Metadata Design**: Structured metadata enables powerful query capabilities
4. **Filtering Logic**: Boolean operators + count constraints cover diverse use cases

## 📝 License

MIT License

## 🙏 Acknowledgments

- [Ultralytics YOLOv11](https://github.com/ultralytics/ultralytics) for object detection
- [Streamlit](https://streamlit.io/) for the web framework

---

⭐ If you find this tool useful for your annotation workflows, please consider starring the repository!
