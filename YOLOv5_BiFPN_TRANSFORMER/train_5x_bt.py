import os
import subprocess
import torch 
import yaml
import gc
import wget

# Clear memory of garbage and cache files
gc.collect()
torch.cuda.empty_cache()

# Create custom dataset file for inital training
result = {
    "train": f"/gwhd_dataset/ds_train/images/train",
    "val": f"/gwhd_dataset/ds_train/images/val",
    "nc": 1,
    "names": ["wheat"],
}

with open("custom_dataset1.yaml", "w") as f:
    dump = yaml.dump(result, default_flow_style=False)
    f.write(dump)

# Create the results directory for initial training phase
results_dir_path = 'results_5x_bt'

try:
	os.makedirs(results_dir_path, exist_ok=True) 
	print(f"Directory '{results_dir_path}' created successfully.")
except Exception as e:
	print(f"An error occurred: {e}")
	
# Download and get initial pretrained weights
file_url = 'https://drive.google.com/file/d/1DNL789y60gJGztySyMOYdUiOqrR4emdj/view?usp=drive_link'
output_file = 'yolo_5x_bt.pt'
wget.download(file_url, out=output_file)
print(f'Download complete. File saved as {output_file}')

# Specify paths to  configuration files
cfg_yaml_path = 'yolo_5x_bt.yaml'
data_yaml_path = 'custom_dataset1.yaml'
hyp_yaml_path = 'hyp_5x_bt.yaml'
weights = 'yolo_5x_bt.pt'
project_path = os.path.join('results_5x_bt', 'runs', 'train')
proj_name = 'exp_5x_bt1' 

# Define the training parameters
img_size = 800
batch_size = 8
epochs = 50
es_epoch = 10

print("Train Model:")

# Command to execute the training script
command = [
    'python', 'YOLOv5/train.py',
    '--img', str(img_size),
    '--batch', str(batch_size),
    '--epochs', str(epochs),
    '--cfg', cfg_yaml_path,
    '--data', data_yaml_path,
    '--hyp', hyp_yaml_path,
    '--weights', weights,
    '--project', project_path,
    '--name', proj_name,
    '--patience', str(es_epoch),
]

# Open a file to write the outputto log file
with open('train_5x_bt_log1.txt', 'w') as log_file:
    result = subprocess.run(command, stdout=log_file, stderr=subprocess.STDOUT)

if result.returncode != 0:
    print(f"Command failed with return code {result.returncode}. See 'train_5x_bt_log1.txt' for details.")
else:
    print("Command executed successfully. See 'train_5x_bt_log1.txt' for details.")

print("Training the Model Completed.")
