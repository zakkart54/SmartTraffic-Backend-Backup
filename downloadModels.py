# from ultralytics import YOLO
# from torchvision.models import resnet50
import os
def createDirs(base_dir):

# Create the main directory
    os.makedirs(base_dir, exist_ok=True)
    # Create subdirectories under storage
    subdirs = [
        # Images directories
        "images",
        "images/unverified",
        
        # Images - v_test
        "images/v_test/flooded/positive",
        "images/v_test/flooded/negative",
        "images/v_test/obstacles/positive", 
        "images/v_test/obstacles/negative",
        "images/v_test/police/positive",
        "images/v_test/police/negative",
        "images/v_test/trafficJam/positive",
        "images/v_test/trafficJam/negative",
        
        # Images - v_train
        "images/v_train/flooded/positive",
        "images/v_train/flooded/negative",
        "images/v_train/obstacles/positive",
        "images/v_train/obstacles/negative",
        "images/v_train/police/positive",
        "images/v_train/police/negative",
        "images/v_train/trafficJam/positive",
        "images/v_train/trafficJam/negative",
        
        # Images - v_val
        "images/v_val/flooded/positive",
        "images/v_val/flooded/negative",
        "images/v_val/obstacles/positive",
        "images/v_val/obstacles/negative",
        "images/v_val/police/positive",
        "images/v_val/police/negative",
        "images/v_val/trafficJam/positive",
        "images/v_val/trafficJam/negative",
        
        # Texts directories
        "texts",
        "texts/unverified",
        
        # Texts - v_test
        "texts/v_test/flooded/positive",
        "texts/v_test/flooded/negative",
        "texts/v_test/obstacles/positive",
        "texts/v_test/obstacles/negative",
        "texts/v_test/police/positive",
        "texts/v_test/police/negative",
        "texts/v_test/trafficJam/positive",
        "texts/v_test/trafficJam/negative",
        
        # Texts - v_train
        "texts/v_train/flooded/positive",
        "texts/v_train/flooded/negative",
        "texts/v_train/obstacles/positive",
        "texts/v_train/obstacles/negative",
        "texts/v_train/police/positive",
        "texts/v_train/police/negative",
        "texts/v_train/trafficJam/positive",
        "texts/v_train/trafficJam/negative",
        
        # Texts - v_val
        "texts/v_val/flooded/positive",
        "texts/v_val/flooded/negative",
        "texts/v_val/obstacles/positive",
        "texts/v_val/obstacles/negative",
        "texts/v_val/police/positive",
        "texts/v_val/police/negative",
        "texts/v_val/trafficJam/positive",
        "texts/v_val/trafficJam/negative"
    ]
    # Create each subdirectory
    for subdir in subdirs:
        os.makedirs(os.path.join(base_dir, subdir), exist_ok=True)

if __name__ == "__main__":
    print('downloading')
    
    # a = resnet50(weights='ResNet50_Weights.DEFAULT')
    createDirs("storage")
    createDirs("src/storage")
    # model = YOLO('yolo11n.pt')
    print('downloaded')