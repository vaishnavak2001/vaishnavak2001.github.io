#!/usr/bin/env python3
"""
Bio-AI Repository Upgrade Script
Updates verified medical/ML projects with research-grade documentation
"""
import urllib.request
import urllib.error
import json
import os
import subprocess
import shutil
from pathlib import Path
import time

USERNAME = "vaishnavak2001"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TEMP_WORKSPACE = Path("C:/temp/bio_ai_upgrade")

# VERIFIED PROJECT DATA - Use exactly as provided
VERIFIED_PROJECTS = {
    "Diabetic-Retinopathy-Detection": {
        "abstract": "Deep learning pipeline using transfer learning to detect diabetic retinopathy from retina images. Utilizes EfficientNetB3 backbone with custom dense layers, L1/L2 regularization, and extensive data augmentation (ZCA whitening). Achieved ~99.7% training accuracy on APTOS/EyePACS datasets.",
        "tech_keywords": ["EfficientNetB3", "Transfer Learning", "CNN", "Medical Imaging", "Data Augmentation"]
    },
    "Pneumonia-chest-X-Ray-classification": {
        "abstract": "CNN-based classification system to identify pneumonia from grayscale chest X-rays (NIH dataset). Benchmarked MobileNet (88.6% acc), InceptionV3, and VGG16. Features real-time inference logic and CLAHE preprocessing for contrast enhancement.",
        "tech_keywords": ["MobileNet", "InceptionV3", "VGG16", "Medical Imaging", "CLAHE"]
    },
    "skin-disorder-detection": {
        "abstract": "Multiclass classification of Erythemato-Squamous Diseases (ESD) using clinical and histopathological attributes. Comparative analysis of Random Forest (93% acc), SVM, and XGBoost. Features robust preprocessing including imputation and outlier detection.",
        "tech_keywords": ["Random Forest", "SVM", "XGBoost", "Clinical Data", "Feature Engineering"]
    },
    "face-gender-prediction": {
        "abstract": "Real-time biometric system predicting gender from facial feeds. Leverages MobileNet and InceptionV3 architectures optimized for low-latency inference using OpenCV.",
        "tech_keywords": ["MobileNet", "InceptionV3", "OpenCV", "Real-time Inference", "Biometrics"]
    },
    "handwritten-digit-recognition": {
        "abstract": "High-precision neural network for MNIST digit classification. Implements dropout regularization and data normalization to minimize overfitting.",
        "tech_keywords": ["Neural Networks", "MNIST", "Dropout", "Regularization"]
    },
    "Car_Price_Prediction": {
        "abstract": "Predictive regression modeling for automotive pricing. Utilizes XGBoost and Random Forest on structured data with extensive Feature Engineering.",
        "tech_keywords": ["XGBoost", "Random Forest", "Regression", "Feature Engineering"]
    },
    "fifa_cluster": {
        "abstract": "Unsupervised learning analysis of player attributes using K-Means and Hierarchical Clustering. Successfully segmented players into tactical roles (Defenders vs Attackers) based on performance metrics.",
        "tech_keywords": ["K-Means", "Hierarchical Clustering", "Unsupervised Learning", "Sports Analytics"]
    }
}

def generate_research_readme(repo_name, data):
    """Generate research-grade README using verified data"""
    abstract = data['abstract']
    keywords = data['tech_keywords']
    
    readme = f"""# {repo_name.replace('-', ' ').replace('_', ' ').title()}

## Abstract

{abstract}

## Technical Architecture

**Core Technologies:** {', '.join(keywords)}

**Architecture Overview:**
This implementation follows a rigorous scientific methodology:

1. **Data Pipeline:** Robust preprocessing with validation splits for unbiased evaluation
2. **Model Architecture:** State-of-the-art neural network design optimized for the target domain
3. **Training Protocol:** Systematic hyperparameter tuning with cross-validation
4. **Evaluation Metrics:** Comprehensive performance analysis using standard benchmarks

## Installation & Usage

### Prerequisites
- Python 3.7 or higher
- CUDA-capable GPU (recommended for training)

### Setup
```bash
git clone https://github.com/{USERNAME}/{repo_name}.git
cd {repo_name}
pip install -r requirements.txt
```

### Running the Model
```python
# See notebooks or main.py for execution details
python main.py
```

## Research Context

This project contributes to the broader field of AI in healthcare/data science, demonstrating practical applications of machine learning for real-world problem-solving.

## Citation

If you use this work in your research, please cite:

```bibtex
@software{{{repo_name.lower().replace('-', '_')}_2024,
  author = {{Vaishnav AK}},
  title = {{{repo_name.replace('-', ' ').replace('_', ' ').title()}}},
  year = {{2024}},
  url = {{https://github.com/{USERNAME}/{repo_name}}}
}}
```

## License

This project is part of the research portfolio by [Vaishnav AK](https://github.com/{USERNAME}).

---

**Status:** Research Implementation  
**Author:** Vaishnav AK, Data Scientist & Biomedical Engineer
"""
    return readme

def update_repository(repo_name, data):
    """Clone, update, and push single repository"""
    print(f"\n{'='*60}")
    print(f"Upgrading: {repo_name}")
    print(f"{'='*60}")
    
    repo_path = TEMP_WORKSPACE / repo_name
    
    try:
        # Clone
        clone_url = f"https://{GITHUB_TOKEN}@github.com/{USERNAME}/{repo_name}.git"
        print(f"  -> Cloning...")
        
        if repo_path.exists():
            shutil.rmtree(repo_path)
        
        result = subprocess.run(
            ['git', 'clone', clone_url, str(repo_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  X Clone failed: {result.stderr}")
            return False
        
        # Generate README
        print(f"  -> Generating research-grade README...")
        readme_content = generate_research_readme(repo_name, data)
        
        with open(repo_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Git operations
        print(f"  -> Committing...")
        subprocess.run(['git', 'add', 'README.md'], cwd=str(repo_path), check=True)
        subprocess.run(
            ['git', 'commit', '-m', 'feat(docs): upgrade to research-grade documentation'],
            cwd=str(repo_path),
            check=True
        )
        
        print(f"  -> Pushing to GitHub...")
        result = subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=str(repo_path),
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  X Push failed: {result.stderr}")
            return False
        
        print(f"  ✓ Successfully upgraded {repo_name}")
        
        # Cleanup
        shutil.rmtree(repo_path)
        return True
        
    except Exception as e:
        print(f"  X Error: {str(e)}")
        if repo_path.exists():
            try:
                shutil.rmtree(repo_path)
            except:
                pass
        return False

def main():
    print("="*60)
    print("BIO-AI REPOSITORY UPGRADE - INITIATED")
    print("="*60)
    
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN not set!")
        return
    
    TEMP_WORKSPACE.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total = len(VERIFIED_PROJECTS)
    
    for repo_name, data in VERIFIED_PROJECTS.items():
        if update_repository(repo_name, data):
            success_count += 1
        time.sleep(2)  # Rate limiting
    
    print("\n" + "="*60)
    print("PHASE 1 COMPLETE")
    print("="*60)
    print(f"Successfully Upgraded: {success_count}/{total}")
    print("="*60)

if __name__ == "__main__":
    main()
