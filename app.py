import streamlit as st
import  sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import json
from src.inference import YOLOModelInference
from src.utils import save_metadata, load_metadata, get_unique_classes_and_counts


# Add the parent directory to the system path
sys.path.append(str(Path(__file__).parent))

def img_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def init_session_state():
    session_default = {
        'metadata': None,
        'filtered_options': {}, # stores the dictonary {class_name: [counts]} eg. {"person": [1,2,3], "car": [1,4]}
        'search_params': {
            "search_mode": "Any of the selected classes (OR)",
            "selected_classes": [],
            "threshold": {},
        },
        'filtered_metadata': [],
        'show_boxes': True,
        'grid_cols': 3,
        'highlight_matches': True,
    }
    
    for key, value in session_default.items():
        if key not in st.session_state:
            st.session_state[key] = value
        
init_session_state()
st.set_page_config(page_title="YOLO image search", layout="wide")
st.title("YOLO Powered Image Search Application")

options = st.radio("Select an option:",
                   ("Process new image data", "Load metadata"), horizontal=True)
if options == "Process new image data":
    with st.expander("Process new image data", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
         
            image_path = st.text_input("Image directory path", placeholder = "/path/to/your/images")
        with col2: 
            model_path = st.text_input("Model weights path", "yolo11s.pt")
        
        if st.button("Process Images"):
            if image_path:
                try:
                    # call the inferencer model here
                    with st.spinner("Processing images..."): 
                        inference = YOLOModelInference(model_path)
                        metadata = inference.process_image_directory(image_path)
                        output_file = save_metadata(metadata, image_path)
                        # if output file is not none then show success message.
                        if output_file is not None:
                            st.success(f"{len(metadata)} processed.")
                            st.code(f"Metadata saved at: {output_file}")
                            st.session_state['metadata'] = metadata  
                            st.session_state['filtered_options'] = get_unique_classes_and_counts(metadata)
                              
                        else:
                            st.error("File not found. Please check the image directory path.")
                
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            else:
                st.error("Please provide image directory path to continue.")
else:
    with st.expander("Load metadata", expanded=True):
        path_metadata = st.text_input("Metadata file path", placeholder = "/path/to/your/metadata.json")
        if st.button("Load Metadata"):
            if path_metadata:
                try:
                    with st.spinner("loading metadata..."):
                        metadata = load_metadata(path_metadata)
                        # metadata is tuple and none if not found
                        metadata, found = metadata
                        if metadata is not None:
                            st.success(f"Metadata loaded with {len(metadata)} records.")
                            st.code(f"Metadata loaded from: {found}")
                            st.session_state['metadata'] = metadata
                            st.session_state['filtered_options'] = get_unique_classes_and_counts(metadata)
                            

                        else:
                            st.error("Metadata file not invalid, Provide valid metadata file path.")
                except Exception as e:
                    st.error(f"An error occured: {e}")
            else:
                st.error("Please provide metadata file path to continue.")
    st.write(f"{st.session_state['filtered_options']}")
    
    
######### SEARCH AND FILTER SECTION #############
if st.session_state['metadata'] is not None: 
    st.subheader("Search and Filter")
    with st.container():
        
        st.session_state['search_params']["search_mode"] = st.radio("Select Search Mode" , 
             ("Any of the selected classes (OR)", "All of the selected classes (AND)"),
             key="search_mode", horizontal=True)
        
    
        st.session_state.search_params["selected_classes"] = st.multiselect(
            "Choose classes to search:", options=list(st.session_state['filtered_options'].keys()),
            )
        
        if st.session_state.search_params["selected_classes"]:
            st.subheader("Set threshold counts for selected classes:")
            cols = st.columns(len(st.session_state.search_params["selected_classes"]))
            for i,cls in enumerate(st.session_state.search_params["selected_classes"]):
                with cols[i]:
                    st.session_state.search_params["threshold"][cls] = st.selectbox(
                        f"Maximum count for {cls}:", 
                        options=["None"]+list(st.session_state['filtered_options'][cls]),
                    )
        
        if st.button("Search Images", type="primary", key="search_button") and st.session_state.search_params["selected_classes"]:
            result=[]
            search_params = st.session_state.search_params
            
            for item in st.session_state['metadata']:
                match = False
                class_matches = {}
                
                for cls in search_params["selected_classes"]:
                    class_detections = [det for det in item["detections"] if det["class_name"] == cls]
                    class_count = len(class_detections)
                    class_matches[cls] = False
                    
                    threshold = search_params["threshold"].get(cls, "None") 
                    # checking threshold condition from user
                    if threshold is None or threshold == "None":
                        # suppose user did not set any threshold count for this class
                        # but class is present in image we will consider it a match and show all the images
                        if class_count >0:
                            class_matches[cls] = True
                    else:
                            # if class count is !=0 and is less than threshold then its a match image
                        class_matches[cls] = (class_count >0 and class_count <= int(threshold))
                
                if search_params["search_mode"] == "Any of the selected classes (OR)":
                    # if any class matches we consider this image a match
                    match = any(class_matches.values())
                
                else: 
                    # all classes must match for this image to be considered a match
                    match = all(class_matches.values())
                    
                if match:
                    result.append(item)
                
            st.session_state['filtered_metadata'] = result
    

#### Display Filtered Results ###
if st.session_state['filtered_metadata'] is not None:
    results = st.session_state['filtered_metadata']
    st.subheader(f"Filtered Results: {len(results)} images found")
    
    with st.expander("Display Options", expanded=True):
        cols = st.columns(3)
        with cols[0]:
            st.session_state.show_boxes = st.checkbox("Show Bounding Boxes",
                    value=st.session_state.show_boxes
            )
        with cols[1]:
            st.session_state.grid_cols = st.slider("Grid Columns", min_value=2, max_value=5,
                      value=st.session_state.grid_cols
            )
        with cols[2]:
            st.session_state.highlight_matches = st.checkbox("Highlight Matches",
                    value=st.session_state.highlight_matches
            )
    # Display images in grid format
    grid_cols = st.columns(st.session_state.grid_cols)
    col_index = 0
    
    for result in results:
        with grid_cols[col_index]:
            try: 
                img = Image.open(result["image_path"])
                draw = ImageDraw.Draw(img)
                
                if st.session_state.show_boxes:
                    for det in result["detections"]:
                        bbox = det["bbox"]
                        class_name = det["class_name"]
                        count = det["count"]
                        a=0
                        # Draw bounding box
                        if class_name in st.session_state.search_params["selected_classes"]:
                            draw.rectangle(bbox, outline="green", width=4)
                            a=1
                        
                        elif not st.session_state.highlight_matches:
                            draw.rectangle(bbox, outline="gray", width=1)
                        else:
                            continue
                        
                        if class_name in st.session_state.search_params["selected_classes"] or not st.session_state.highlight_matches:
                            # Annotate with class name and count
                            label = f"{class_name} {det['confidence']: .2f}"
                            text_bbox = draw.textbbox((0, 0), label, font=ImageFont.load_default())
                            text_width = text_bbox[2] - text_bbox[0]
                            text_height = text_bbox[3] - text_bbox[1]
                            draw.rectangle([bbox[0], bbox[1] - text_height, bbox[0] + text_width, bbox[1]], fill="green" if a == 1 else "gray")
                            draw.text((bbox[0], bbox[1] - text_height), label, fill="white", font=ImageFont.load_default())
                # Build class_counts from the metadata structure
                class_counts = dict(zip(result['unique_classes'], result['unique_class_count']))
                meta_items = [f"{k}: {v}" for k, v in class_counts.items() 
                              if k in st.session_state.search_params["selected_classes"]]         

                st.markdown(f""" 
                            <div class="image-card">
                                <div class="image-container">
                                    <img src="data:image/png;base64,{img_to_base64(img)}" alt="Image" style="width:100%; height:auto; border: 2px solid #ccc; border-radius: 5px;"/>
                                </div>
                                <div class="meta-overlay">
                                    <strong> {Path(result['image_path']).name} </strong><br/>
                                    {", ".join(meta_items) if meta_items else "No matching classes"}
                                </div>
                            </div>
         
                            """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading image {result['image_path']}: {e}")
                continue
        
        
        col_index = (col_index + 1) % st.session_state.grid_cols
    
    with st.expander("Export Filtered Metadata"):
        st.download_button(
            label="Download Metadata as JSON",
            data=json.dumps(results, indent=4),
            file_name="filtered_metadata.json",
            mime="application/json"
        )