"""
LLaVA-Med Fine-Tuning for Medical Image Analysis

This script demonstrates how to fine-tune LLaVA-Med for downstream
medical imaging tasks, specifically for breast cancer pathology.

Author: Dr. Rajan Prasad Tripathi | AUT AI Innovation Lab
Reference: https://github.com/microsoft/LLaVA-Med/issues/127
Related: https://github.com/rajantripathi/Breast-Cancer-Multimodal-AI
"""

import os
import json
import torch
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class FineTuningConfig:
    """Configuration for LLaVA-Med fine-tuning."""

    # Model settings
    base_model: str = "microsoft/llava-med-v1.5-7b"
    model_base: str = "liuhaotian/llava-v1.5-7b"
    output_dir: str = "./llava-med-finetuned"

    # LoRA settings
    lora_r: int = 64
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    lora_targets: List[str] = None

    # Training settings
    num_epochs: int = 3
    batch_size: int = 4
    learning_rate: float = 2e-5
    warmup_ratio: float = 0.03
    weight_decay: float = 0.01

    # Data settings
    data_path: str = "./medical_data.json"
    image_folder: str = "./images"
    max_length: int = 2048

    def __post_init__(self):
        if self.lora_targets is None:
            self.lora_targets = ["q_proj", "v_proj", "k_proj", "o_proj"]


def setup_model(config: FineTuningConfig):
    """
    Set up LLaVA-Med model for fine-tuning.

    Requires:
    - llava package from https://github.com/haotian-liu/LLaVA
    - PEFT for LoRA fine-tuning
    """
    try:
        from llava.model.builder import load_pretrained_model
        from llava.mm_utils import get_model_name_from_path
        from peft import LoraConfig, get_peft_model, TaskType
    except ImportError:
        print("Please install required packages:")
        print("pip install git+https://github.com/haotian-liu/LLaVA.git")
        print("pip install peft transformers accelerate")
        return None, None, None, None

    # Load base model
    model_name = get_model_name_from_path(config.base_model)
    tokenizer, model, image_processor, context_len = load_pretrained_model(
        model_path=config.base_model,
        model_base=config.model_base,
        model_name=model_name,
        device_map="auto"
    )

    # Configure LoRA for medical domain adaptation
    lora_config = LoraConfig(
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        target_modules=config.lora_targets,
        lora_dropout=config.lora_dropout,
        bias="none",
        task_type=TaskType.CAUSAL_LM
    )

    # Apply LoRA
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    return tokenizer, model, image_processor, context_len


def prepare_medical_dataset(
    data_path: str,
    image_folder: str,
    tokenizer,
    image_processor,
    max_length: int = 2048
):
    """
    Prepare medical imaging dataset for fine-tuning.

    Expected data format (JSON):
    [
        {
            "id": "sample_001",
            "image": "pathology_001.png",
            "conversations": [
                {"from": "human", "value": "<image>\nDescribe this pathology slide."},
                {"from": "gpt", "value": "This pathology slide shows..."}
            ]
        }
    ]
    """
    try:
        from llava.data.dataset import LazySupervisedDataset
    except ImportError:
        print("Using custom dataset loader...")
        return create_custom_dataset(data_path, image_folder, tokenizer, image_processor)

    # Use LLaVA's built-in dataset loader
    with open(data_path, 'r') as f:
        data = json.load(f)

    return data


def create_custom_dataset(
    data_path: str,
    image_folder: str,
    tokenizer,
    image_processor
):
    """Create a custom dataset for medical imaging."""

    class MedicalImageDataset(torch.utils.data.Dataset):
        def __init__(self, data_path, image_folder, tokenizer, image_processor):
            with open(data_path, 'r') as f:
                self.data = json.load(f)
            self.image_folder = image_folder
            self.tokenizer = tokenizer
            self.image_processor = image_processor

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            item = self.data[idx]

            # Load image
            image_path = os.path.join(self.image_folder, item['image'])
            from PIL import Image
            image = Image.open(image_path).convert('RGB')

            # Process image
            image_tensor = self.image_processor.preprocess(image, return_tensors='pt')['pixel_values'][0]

            # Process text
            conversations = item['conversations']
            text = ""
            for conv in conversations:
                if conv['from'] == 'human':
                    text += f"USER: {conv['value']} "
                else:
                    text += f"ASSISTANT: {conv['value']}</s>"

            text_tokens = self.tokenizer(
                text,
                return_tensors='pt',
                padding='max_length',
                truncation=True,
                max_length=2048
            )

            return {
                'input_ids': text_tokens['input_ids'][0],
                'attention_mask': text_tokens['attention_mask'][0],
                'pixel_values': image_tensor,
                'labels': text_tokens['input_ids'][0].clone()
            }

    return MedicalImageDataset(data_path, image_folder, tokenizer, image_processor)


def preprocess_medical_image(image_path: str, modality: str = "pathology"):
    """
    Preprocess medical images for LLaVA-Med.

    Different modalities require different preprocessing:
    - Pathology: Stain normalization, tissue detection
    - Radiology: Window/level adjustment, contrast enhancement
    - Dermatology: Color normalization, hair removal
    """
    try:
        import cv2
        import numpy as np
        from PIL import Image
    except ImportError:
        print("Please install opencv-python and numpy for image preprocessing")
        return None

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if modality == "pathology":
        # Stain normalization for histopathology
        # Using Macenko method or Reinhard normalization
        image = normalize_stains(image)

    elif modality == "radiology":
        # Contrast enhancement for radiology
        image = enhance_contrast(image)

    elif modality == "dermatology":
        # Hair removal and color normalization for dermoscopy
        image = remove_hair(image)
        image = normalize_color(image)

    return Image.fromarray(image)


def normalize_stains(image: np.ndarray) -> np.ndarray:
    """
    Normalize H&E staining in pathology images.

    This is critical for consistent model performance across
    different scanners and staining protocols.
    """
    # Simplified stain normalization
    # In production, use staintools or similar library
    import numpy as np

    # Convert to OD space
    OD = -np.log((image.astype(np.float32) + 1) / 256)

    # Simple reinhard normalization
    mean = OD.mean(axis=(0, 1))
    std = OD.std(axis=(0, 1))

    # Normalize to standard values (from a reference image)
    ref_mean = np.array([0.5, 0.5, 0.5])
    ref_std = np.array([0.2, 0.2, 0.2])

    OD_normalized = (OD - mean) / std * ref_std + ref_mean

    # Convert back to RGB
    image_normalized = np.exp(-OD_normalized) * 256 - 1
    image_normalized = np.clip(image_normalized, 0, 255).astype(np.uint8)

    return image_normalized


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """Enhance contrast for radiology images."""
    import cv2

    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)

    return enhanced


def remove_hair(image: np.ndarray) -> np.ndarray:
    """Remove hair artifacts from dermoscopy images."""
    import cv2

    # Morphological closing to remove thin structures
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 17))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)

    # Threshold and inpaint
    _, thresh = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    inpainted = cv2.inpaint(image, thresh, 1, cv2.INPAINT_TELEA)

    return inpainted


def normalize_color(image: np.ndarray) -> np.ndarray:
    """Normalize color for dermatology images."""
    import cv2

    # Simple color normalization
    image = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    image[:, :, 0] = cv2.normalize(image[:, :, 0], None, 0, 255, cv2.NORM_MINMAX)
    image = cv2.cvtColor(image, cv2.COLOR_LAB2RGB)

    return image


def train_model(config: FineTuningConfig):
    """
    Train LLaVA-Med on medical imaging data.
    """
    try:
        from transformers import TrainingArguments, Trainer
    except ImportError:
        print("Please install transformers: pip install transformers")
        return

    # Set up model
    tokenizer, model, image_processor, context_len = setup_model(config)
    if model is None:
        return

    # Prepare dataset
    train_dataset = prepare_medical_dataset(
        config.data_path,
        config.image_folder,
        tokenizer,
        image_processor,
        config.max_length
    )

    # Training arguments
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_dir=f"{config.output_dir}/logs",
        logging_steps=10,
        save_steps=100,
        save_total_limit=3,
        fp16=torch.cuda.is_available(),
        gradient_checkpointing=True,
        optim="adamw_torch",
        report_to="none"
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        tokenizer=tokenizer
    )

    # Train
    trainer.train()

    # Save
    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)

    print(f"Model saved to {config.output_dir}")


# Sample medical conversation data format
SAMPLE_DATA = [
    {
        "id": "breast_pathology_001",
        "image": "breast_h&e_001.png",
        "conversations": [
            {
                "from": "human",
                "value": "<image>\nAnalyze this breast tissue biopsy. What histological features do you observe?"
            },
            {
                "from": "gpt",
                "value": "This H&E stained breast tissue section shows the following histological features:\n\n1. **Architecture**: The normal lobular architecture is disrupted, with irregularly shaped glands and ducts.\n\n2. **Cellular Features**: The epithelial cells show mild nuclear atypia with slightly enlarged, hyperchromatic nuclei. Nucleoli are visible but not prominent.\n\n3. **Mitotic Activity**: Occasional mitotic figures are present (estimated 2-3 per 10 HPF).\n\n4. **Stromal Changes**: The surrounding stroma shows mild fibrosis and chronic inflammatory infiltrate.\n\n**Assessment**: These findings are consistent with atypical ductal hyperplasia (ADH). Clinical correlation and immunohistochemical staining (such as E-cadherin) may be helpful for further characterization.\n\n**Note**: This assessment is for clinical decision support only. A qualified pathologist should review the complete case for definitive diagnosis."
            }
        ]
    },
    {
        "id": "breast_pathology_002",
        "image": "breast_h&e_002.png",
        "conversations": [
            {
                "from": "human",
                "value": "<image>\n这是乳腺组织切片吗？请描述你观察到的特征。"
            },
            {
                "from": "gpt",
                "value": "这是一张乳腺组织的H&E染色切片。我观察到以下组织学特征：\n\n1. **组织结构**：正常的小叶结构部分保留，可见一些扩张的导管。\n\n2. **细胞特征**：导管内衬覆的上皮细胞呈单层排列，细胞大小较一致，核仁不明显。\n\n3. **间质变化**：间质内可见少量淋巴细胞浸润。\n\n**评估**：这些表现符合纤维囊性改变的特征，属于良性病变。\n\n**注意**：此评估仅供临床参考，最终诊断需由病理医师结合完整病史做出。"
            }
        ]
    }
]


def create_sample_dataset(output_path: str = "./medical_data_sample.json"):
    """Create a sample dataset file for demonstration."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(SAMPLE_DATA, f, ensure_ascii=False, indent=2)
    print(f"Sample dataset created at {output_path}")


# Main execution
if __name__ == "__main__":
    # Create sample dataset
    create_sample_dataset()

    # Print configuration
    config = FineTuningConfig(
        lora_r=64,
        lora_alpha=16,
        num_epochs=3,
        batch_size=4,
        learning_rate=2e-5
    )

    print("\nFine-tuning Configuration:")
    print(f"  Base Model: {config.base_model}")
    print(f"  LoRA Rank: {config.lora_r}")
    print(f"  LoRA Alpha: {config.lora_alpha}")
    print(f"  Learning Rate: {config.learning_rate}")
    print(f"  Epochs: {config.num_epochs}")

    print("\nTo start fine-tuning, run:")
    print("  train_model(config)")

    print("\nKey considerations for medical imaging fine-tuning:")
    print("  1. Use stain normalization for pathology images")
    print("  2. Apply contrast enhancement for radiology")
    print("  3. Include multilingual medical terminology in training data")
    print("  4. Validate with clinical experts before deployment")
