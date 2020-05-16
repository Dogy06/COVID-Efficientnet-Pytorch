"""
Minimal prediction example
"""

import torch
from PIL import Image

from model.architecture import COVIDNext50
from data.transforms import val_transforms

import config

rev_mapping = {idx: name for name, idx in config.mapping.items()}

model = COVIDNext50(n_classes=len(rev_mapping))

ckpt_pth = './experiments/ckpts/COVIDNext50_NewData_F1_94.36_step_11200.pth'
weights = torch.load(ckpt_pth)['state_dict']
model.load_state_dict(weights)
model.eval()

transforms = val_transforms(width=config.width, height=config.height)
while True:
	img_pth = input("Drag image here: ").replace("'", "")
	img = Image.open(img_pth).convert("RGB")
	img_tensor = transforms(img).unsqueeze(0)
	
	with torch.no_grad():
	    logits = model(img_tensor)
	    cat_id = int(torch.argmax(logits))
	print("Prediction for {} is: {}".format(img_pth, rev_mapping[cat_id]))
