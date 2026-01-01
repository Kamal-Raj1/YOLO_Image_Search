from pathlib import Path
import json
PROJECT_DIR = Path(__file__).parent.parent

def validate_path(img_path):
    path = Path(img_path)
    if path.exists():
        processed_path = PROJECT_DIR / "processed" / path.name
        processed_path.mkdir(parents=True, exist_ok = True)
        return processed_path
    else:
        return None

def save_metadata(metadata, img_path):
    '''
    this functions calls validate path and gets the processed path to save the metadata
    creates the metadata.json file and saves the metadata as a json file. 
    returns the output file path to show in UI.
    '''
    valid_path = validate_path(img_path)
    if valid_path is not None:
        output_file = valid_path / "metadata.json"
        with open(output_file, 'w') as f:
            json.dump(metadata, f)
        return output_file
    else: 
        return None

def load_metadata(metadata_path):
    '''
    We check if the given metadata path exists, if yes we load and return the metadata.
    If not we check in the processed directory for the metadata.json file and load from there.
    If not found we return None.
    '''
    metadata_path = Path(metadata_path)
    if metadata_path.exists():
        found = metadata_path
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            return metadata , found
    else: 
        # # check in processed directory
        #     processed_path = PROJECT_DIR / "processed" / metadata_path.stem / "metadata.json"
        #     if processed_path.exists():
        #         found = processed_path
        #         with open(processed_path, 'r') as f:
        #             metadata = json.load(f)
        #             return metadata, found
        #     else:
                return None, None

def get_unique_classes_and_counts(metadata):
    
    data = metadata
    unique_classes_and_counts = {}
    for item in data:
        for cls, count in zip(item['unique_classes'], item['unique_class_count']):
            if cls not in unique_classes_and_counts:
                unique_classes_and_counts[cls] = set()
            unique_classes_and_counts[cls].add(count)
        
# returning the dictionary with unique class names as keys 
# and list of counts particular class has as values in sorted order.
    return {cls: sorted(list(counts)) for cls, counts in unique_classes_and_counts.items()}