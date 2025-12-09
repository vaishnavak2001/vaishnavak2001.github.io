#!/usr/bin/env python3
"""
BIO-INTELLIGENCE OMNI-PROTOCOL
------------------------------
Global Repository Synchronization & Documentation System
Tier 1: Featured Research (Gold Standard)
Tier 2: Scientific Archive (Automated Analysis)
"""

import os
import json
import subprocess
import shutil
import time
from pathlib import Path

# --- CONFIGURATION ---
USERNAME = "vaishnavak2001"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TEMP_WIDTH = Path("C:/temp/omni_protocol_workspace")

# --- TIER 1 DATA PAYLOAD (Exact Text) ---
TIER_1_DATA = {
    "diabetic-retinopathy-detection": {
        "abstract": "Deep learning pipeline using transfer learning to detect diabetic retinopathy from retina images. Utilizes EfficientNetB3 backbone with custom dense layers, L1/L2 regularization, and extensive data augmentation (ZCA whitening). Achieved ~99.7% training accuracy on APTOS/EyePACS datasets.",
        "tags": ["EfficientNetB3", "Medical Imaging", "Deep Learning", "Transfer Learning"],
        "category": "Medical AI"
    },
    "pneumonia-detection": { # Map to actual repo name if slightly different
        "abstract": "CNN-based classification system to identify pneumonia from grayscale chest X-rays (NIH dataset). Benchmarked MobileNet (88.6% acc), InceptionV3, and VGG16. Features real-time inference logic and CLAHE preprocessing for contrast enhancement.",
        "tags": ["CNN", "MobileNet", "InceptionV3", "Medical Imaging"],
        "category": "Medical AI"
    },
    "Pneumonia-chest-X-Ray-classification": { # Handling potential repo name variance
        "abstract": "CNN-based classification system to identify pneumonia from grayscale chest X-rays (NIH dataset). Benchmarked MobileNet (88.6% acc), InceptionV3, and VGG16. Features real-time inference logic and CLAHE preprocessing for contrast enhancement.",
        "tags": ["CNN", "MobileNet", "InceptionV3", "Medical Imaging"],
        "category": "Medical AI"
    },
    "skin-disorder-detection": {
        "abstract": "Multiclass classification of Erythemato-Squamous Diseases (ESD) using clinical and histopathological attributes. Comparative analysis of Random Forest (93% acc), SVM, and XGBoost. Features robust preprocessing including imputation and outlier detection.",
        "tags": ["Random Forest", "SVM", "XGBoost", "Clinical Data"],
        "category": "Medical AI"
    },
    "face-gender-prediction": {
        "abstract": "Real-time biometric system predicting gender from facial feeds. Leverages MobileNet and InceptionV3 architectures optimized for low-latency inference using OpenCV.",
        "tags": ["Computer Vision", "Biometrics", "MobileNet", "Real-time"],
        "category": "Computer Vision"
    },
     "GenderDetc_complete_using_colab": { # Potential actual name
        "abstract": "Real-time biometric system predicting gender from facial feeds. Leverages MobileNet and InceptionV3 architectures optimized for low-latency inference using OpenCV.",
        "tags": ["Computer Vision", "Biometrics", "MobileNet", "Real-time"],
        "category": "Computer Vision"
    },
    "handwritten-digit-recognition": {
        "abstract": "High-precision neural network for MNIST digit classification. Implements dropout regularization and data normalization to minimize overfitting.",
        "tags": ["MNIST", "Neural Networks", "Deep Learning"],
        "category": "Computer Vision"
    },
    "PRCP_1002_Handwritten_Digits_Recognition": { # Potential actual name
         "abstract": "High-precision neural network for MNIST digit classification. Implements dropout regularization and data normalization to minimize overfitting.",
        "tags": ["MNIST", "Neural Networks", "Deep Learning"],
        "category": "Computer Vision"
    },
    "auto-price-prediction": {
        "abstract": "Predictive regression modeling for automotive pricing. Utilizes XGBoost and Random Forest on structured data with extensive Feature Engineering.",
        "tags": ["Regression", "XGBoost", "Predictive Analytics"],
        "category": "Analytics"
    },
    "Car_Price_Prediction": { # Potential actual name
        "abstract": "Predictive regression modeling for automotive pricing. Utilizes XGBoost and Random Forest on structured data with extensive Feature Engineering.",
        "tags": ["Regression", "XGBoost", "Predictive Analytics"],
        "category": "Analytics"
    },
    "fifa20-clustering": {
        "abstract": "Unsupervised learning analysis of player attributes using K-Means and Hierarchical Clustering. Successfully segmented players into tactical roles (Defenders vs Attackers) based on performance metrics.",
        "tags": ["Clustering", "K-Means", "Unsupervised Learning", "Sports Analytics"],
        "category": "Analytics"
    },
    "fifa_cluster": { # Potential actual name
        "abstract": "Unsupervised learning analysis of player attributes using K-Means and Hierarchical Clustering. Successfully segmented players into tactical roles (Defenders vs Attackers) based on performance metrics.",
        "tags": ["Clustering", "K-Means", "Unsupervised Learning", "Sports Analytics"],
        "category": "Analytics"
    }
}

# --- HELPER FUNCTIONS ---

def get_all_repos():
    """Fetch all public repos using GitHub CLI or curl (fallback)"""
    # Assuming user has gh cli or we use requests/curl if available. 
    # Using python subprocess with curl for broad compatibility given the context
    cmd = [
        "curl", "-H", f"Authorization: token {GITHUB_TOKEN}",
        f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching repos:", result.stderr)
        return []
    try:
        return json.loads(result.stdout)
    except:
        return []

def analyze_tech_stack(repo_path):
    """Tier 2 Logic: Scan files to infer tech stack"""
    languages = set()
    frameworks = set()
    
    # Extensions map
    ext_map = {
        '.py': 'Python', '.js': 'JavaScript', '.ipynb': 'Jupyter Notebook', 
        '.cpp': 'C++', '.java': 'Java', '.html': 'HTML/CSS'
    }
    
    # Framework signatures
    fw_sigs = {
        'tensorflow': 'TensorFlow', 'keras': 'Keras', 'torch': 'PyTorch',
        'sklearn': 'Scikit-learn', 'pandas': 'Pandas', 'react': 'React',
        'django': 'Django', 'flask': 'Flask', 'streamlit': 'Streamlit',
        'opencv': 'OpenCV', 'gym': 'OpenAI Gym'
    }
    
    for root, dirs, files in os.walk(repo_path):
        if '.git' in root: continue
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in ext_map:
                languages.add(ext_map[ext])
            
            # Simple content scan for frameworks (first 50 lines)
            try:
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(2000).lower() 
                    for sig, name in fw_sigs.items():
                        if sig in content:
                            frameworks.add(name)
            except:
                pass
                
    return list(languages), list(frameworks)

def generate_readme(repo_name, tier, data=None, tech_analysis=None):
    """Generate Research Paper formatted README"""
    if tier == 1:
        abstract = data['abstract']
        tech_stack = ", ".join(data['tags'])
        category = data['category']
    else:
        # Synthesize for Tier 2
        langs, fws = tech_analysis
        tech_stack = ", ".join(langs + fws)
        category = "Software Archive"
        
        # Heuristic Abstract
        clean_name = repo_name.replace('-', ' ').replace('_', ' ').title()
        if 'notebook' in [l.lower() for l in langs]:
            abstract = f"Computational analysis and research implementation for **{clean_name}**. Utilizes interactive notebook environments for data exploration and algorithmic validation."
        elif 'python' in [l.lower() for l in langs]:
             abstract = f"Backend algorithm implementation for **{clean_name}**. Developed in Python with a focus on modular architecture and data processing efficiency."
        else:
             abstract = f"Source code repository for **{clean_name}**. Implements core logic and structural components for the target application domain."

    readme = f"""# {repo_name.replace('-', ' ').replace('_', ' ').title()}

![Status](https://img.shields.io/badge/Status-Research_Grade-002147?style=flat-square&logo=github) ![Category](https://img.shields.io/badge/Domain-{category.replace(' ', '_')}-008080?style=flat-square)

## \U0001f4c4 Abstract

{abstract}

## \u2699\ufe0f Technical Architecture

**Stack:** {tech_stack}

### Implementation Details
The system architecture adheres to rigorous software engineering standards. 
{ 'Key components include data preprocessing pipelines, model inference engines, and modular utility wrappers.' if tier == 2 else 'The solution leverages advanced architectural patterns optimized for the specific problem domain, ensuring high performance and reproducibility.'}

## \U0001f4da Citation

If you utilize this work in your research, please cite:

```bibtex
@software{{{repo_name.lower().replace('-', '_')}_2025,
  author = {{Vaishnav AK}},
  title = {{{repo_name.replace('-', ' ').replace('_', ' ').title()}}},
  year = {{2025}},
  url = {{https://github.com/{USERNAME}/{repo_name}}},
  note = {{Bio-Intelligence Research Ecosystem}}
}}
```

---
*© {time.strftime('%Y')} Vaishnav AK. Engineered for Biomedical Innovation.*
"""
    return readme

def process_repo(repo):
    name = repo['name']
    
    # Skip the portfolio repo to avoid recursion issues or overwriting the site
    if name.lower() == f"{USERNAME}.github.io".lower():
        print(f"Skipping Portfolio Repo: {name}")
        return

    print(f"Processing: {name}...")
    
    repo_dir = TEMP_WIDTH / name
    
    # 1. Clone
    if repo_dir.exists():
        shutil.rmtree(repo_dir)
    
    clone_url = repo['clone_url'].replace("https://", f"https://{GITHUB_TOKEN}@")
    subprocess.run(["git", "clone", clone_url, str(repo_dir)], capture_output=True)
    
    # 2. Determine Tier & Generate
    if name in TIER_1_DATA:
        print(f"  -> TIER 1 (Featured)")
        readme_content = generate_readme(name, 1, data=TIER_1_DATA[name])
    else:
        print(f"  -> TIER 2 (Archive)")
        langs, fws = analyze_tech_stack(repo_dir)
        readme_content = generate_readme(name, 2, tech_analysis=(langs, fws))
        
    # 3. Write
    with open(repo_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    # 4. Commit & Push
    subprocess.run(["git", "add", "README.md"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "commit", "-m", "feat(docs): automated research documentation"], cwd=repo_dir, capture_output=True)
    subprocess.run(["git", "push"], cwd=repo_dir, capture_output=True)
    print(f"  -> Synced.")

def main():
    if not GITHUB_TOKEN:
        print("CRITICAL: NO GITHUB TOKEN FOUND.")
        return

    print("--- BIO-INTELLIGENCE OMNI-PROTOCOL STARTED ---")
    TEMP_WIDTH.mkdir(parents=True, exist_ok=True)
    
    repos = get_all_repos()
    print(f"Found {len(repos)} repositories.")
    
    for repo in repos:
        try:
            process_repo(repo)
        except Exception as e:
            print(f"Error processing {repo['name']}: {e}")
            
    # Cleanup
    try:
        shutil.rmtree(TEMP_WIDTH)
    except:
        pass
        
    print("--- MISSION COMPLETE ---")

if __name__ == "__main__":
    main()
