# Image Datasets

## Purpose

This folder stores image datasets for computer vision tasks — classification, object detection, segmentation, OCR, and multimodal AI systems.

---

## Naming Convention

```text
<task>-<description>-<version>/

# Examples:
classification-product-images-v1/
detection-retail-shelves-v1/
ocr-invoice-scans-v1/
segmentation-medical-v1/
```

---

## Folder Structure

```text
images/
│
├── raw/                  # original unmodified images
├── processed/            # resized, normalized, augmented
├── annotations/          # labels, bounding boxes, masks
├── splits/               # train / val / test splits
└── dataset-cards/        # documentation
```

---

## Common Tasks

| Task | Description | Common Formats |
|---|---|---|
| Classification | assign class label to image | JPEG, PNG |
| Object Detection | locate and classify objects | JPEG + COCO JSON |
| Segmentation | pixel-level classification | PNG masks |
| OCR | extract text from images | JPEG, TIFF |
| Multimodal | image + text pairs | JPEG + JSONL |

---

## Common Public Datasets

| Dataset | Task | Size |
|---|---|---|
| CIFAR-10 | classification | 60K images |
| ImageNet | classification | 1.2M images |
| COCO | detection + segmentation | 330K images |
| MNIST | digit classification | 70K images |
| Open Images | detection | 9M images |

---

## Recommended Formats

| Format | Use Case |
|---|---|
| JPEG | photos, large datasets |
| PNG | images with transparency, annotations |
| WebP | web-optimized, smaller size |
| TFRecords | TensorFlow pipelines |
| Parquet | metadata + image paths |

---

## Preprocessing Pipeline

```text
Raw Images
    ↓
Resize (e.g. 224×224)
    ↓
Normalize (mean/std or [0,1])
    ↓
Augmentation (flip, crop, rotate)
    ↓
Train / Val / Test Split
    ↓
DataLoader
```

---

## Usage Example

```python
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

dataset = datasets.ImageFolder("datasets/images/processed/", transform=transform)
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```

---

## Storage Tips

- store raw images separately — never overwrite originals
- use relative paths in annotation files for portability
- compress large datasets with `.zip` or `.tar.gz` before sharing
- use DVC for versioning large image collections

---

## Best Practices

- document class distribution (class imbalance is common)
- separate train/val/test at ingestion — never reshuffle after splitting
- store annotations alongside images in a consistent format
- validate image integrity before training (corrupted files cause silent errors)

**Common pitfalls:** data leakage between splits · missing normalization · inconsistent image sizes · unlabeled edge cases
