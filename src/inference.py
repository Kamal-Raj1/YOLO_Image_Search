from ultralytics import YOLO
import torch 
import os
from pathlib import Path
import numpy as np
from PIL import Image
from src.config import load_config


class YOLOModelInference:
    def __init__(self,  model_name):
        self.model = YOLO(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        config = load_config() # loaded config from default.yaml
        self.conf_threshold = config['model']['conf_threshold']
        self.image_extensions = config['data']['image_extensions']
    
    def __process_single_image(self, image_path:Path):
        '''we do the inference here on each image by getting the 
           image and produce the metadata for it.
        '''
        results = self.model.predict(image_path, conf=self.conf_threshold,device=self.device)
        # Getting the class names and number of object detections
        # A single image may have multiple detections and multiple classes
        detections = []
        class_counts = {}
        for result in results: 
        # iterate through each result, each results (usually single image) may contain multiple bboxes
            for box in result.boxes: 
                #iterate through each detected box
                cls_id = int(box.cls)
                cls_name = result.names[cls_id]
                conf = float(box.conf)
                bbox = box.xyxy[0].cpu().numpy().tolist() # Bounding box coordinates
                detections.append({
                    "class_name": cls_name,
                    "confidence": conf,
                    "bbox": bbox,
                    "count" : 1
                })
                # This will give us the unique classes and their counts per image 
                if cls_name in class_counts:
                    class_counts[cls_name] +=1
                else:
                    class_counts[cls_name] =1 
        # Update the detections with the counts         
        for det in detections: 
            det['count'] = class_counts[det['class_name']]
        
        return {
            "image_path": str(image_path),
            "detections": detections,
            "total_detections": len(detections),
            "unique_classes":  list(class_counts.keys()),
            "unique_class_count": list(class_counts.values()),
        }
        
    
    def process_image_directory(self, image_dir:str):
        ''' scan the directory to get the image files and pass each image path
            to process_single_image function for inference and metadata extraction.
        '''
        metadata =[]
        pattern = list(self.image_extensions)
        print("Searching for image files with extensions:", pattern)
        img_paths=[]
        for extension in pattern:
            img_paths.extend(Path(image_dir).glob(f"*{extension}"))
            
        for img_path in img_paths:
            try:
                metadata.append(self.__process_single_image(img_path))
            except Exception as e:
                print(f"Error processing image {img_path}: {e}")
        return metadata