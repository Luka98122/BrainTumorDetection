from typing import Dict, Tuple, List
import matplotlib.pyplot as plt
import numpy as np
import PIL
import torch
import json
import os


def sample_to_pil_image(sample: np.ndarray, image_shape):
    image = np.reshape(sample, newshape=image_shape)
    image = PIL.Image.fromarray(np.uint8(image*255))
    if image.size[0] < 140:
        new_size = (140, 140) 
    return image.resize(size=new_size)


def get_accuracy(y_hat, y):
    y_pred = torch.sigmoid(y_hat) > 0.5
    y_true = y > 0.5 
    correct = (y_pred == y_true).float().sum()
    total = torch.numel(y)
    return (correct / total).item()


def plot_curve(curves: Tuple[List], labels: Tuple[List], plot_name):
    
    fig, ax = plt.subplots(figsize=[6.4, 3])

    max_len = 0
    for curve in curves:
        if len(curve) > max_len:
            max_len = len(curve)
    
    x_axis = list(range(max_len))
    
    for curve, label in zip(curves, labels):
        ax.plot(x_axis, curve, label=label)
    
    ax.set_xlabel('epochs')
    ax.set_ylabel(plot_name)
    ax.legend()
    fig.tight_layout()
    return fig


def keep_store_dict(curve, label, store_dict: Dict=None):
    
    if store_dict is None:
        store_dict = {}
    
    if not isinstance(curve, list):
        if torch.is_tensor(curve):
            curve = curve.detach().numpy()
        
        if isinstance(curve, np.ndarray):
            curve = curve.tolist()
        else:
            curve = [curve]

    if label in store_dict:    
        store_dict[label].extend(curve)
    else:
        store_dict[label] = curve
    
    return store_dict


def store_dict_to_disk(file_path, store_dict: Dict, overwrite=False):
    
    if overwrite is False and os.path.isfile(file_path):
        prev_dict = load_dict_from_disk(file_path=file_path)
    else:
        prev_dict = None

    if prev_dict is not None:
        for key, val in store_dict.items():
            if key in prev_dict:
                prev_val: List = prev_dict[key]
                prev_val.extend(val)
                store_dict[key] = prev_val
    
    with open(file_path, 'w') as f:
        json.dump(store_dict, f, indent=4)


def load_dict_from_disk(file_path):
    with open(file_path, 'r') as f:
        store_dict = json.load(f)
    return store_dict
