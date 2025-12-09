import json
import os
import subprocess
import urllib.request
from datetime import datetime

# --- CONFIGURATION ---
USERNAME = "vaishnavak2001"
OUTPUT_FILE = "_data/research_data.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# --- TIER 1 DATA PAYLOAD (Exact Text) ---
TIER_1_DATA = {
    "diabetic-retinopathy-detection": {
        "abstract": "Deep learning pipeline using transfer learning to detect diabetic retinopathy from retina images. Utilizes EfficientNetB3 backbone with custom dense layers, L1/L2 regularization, and extensive data augmentation (ZCA whitening). Achieved ~99.7% training accuracy on APTOS/EyePACS datasets.",
        "tags": ["EfficientNetB3", "Medical Imaging", "Deep Learning", "Transfer Learning"],
        "category": "Medical AI"
    },
    "pneumonia-detection": {
        "abstract": "CNN-based classification system to identify pneumonia from grayscale chest X-rays (NIH dataset). Benchmarked MobileNet (88.6% acc), InceptionV3, and VGG16. Features real-time inference logic and CLAHE preprocessing for contrast enhancement.",
        "tags": ["CNN", "MobileNet", "InceptionV3", "Medical Imaging"],
        "category": "Medical AI"
    },
    "Pneumonia-chest-X-Ray-classification": {
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
     "GenderDetc_complete_using_colab": {
        "abstract": "Real-time biometric system predicting gender from facial feeds. Leverages MobileNet and InceptionV3 architectures optimized for low-latency inference using OpenCV.",
        "tags": ["Computer Vision", "Biometrics", "MobileNet", "Real-time"],
        "category": "Computer Vision"
    },
    "handwritten-digit-recognition": {
        "abstract": "High-precision neural network for MNIST digit classification. Implements dropout regularization and data normalization to minimize overfitting.",
        "tags": ["MNIST", "Neural Networks", "Deep Learning"],
        "category": "Computer Vision"
    },
    "PRCP_1002_Handwritten_Digits_Recognition": {
         "abstract": "High-precision neural network for MNIST digit classification. Implements dropout regularization and data normalization to minimize overfitting.",
        "tags": ["MNIST", "Neural Networks", "Deep Learning"],
        "category": "Computer Vision"
    },
    "auto-price-prediction": {
        "abstract": "Predictive regression modeling for automotive pricing. Utilizes XGBoost and Random Forest on structured data with extensive Feature Engineering.",
        "tags": ["Regression", "XGBoost", "Predictive Analytics"],
        "category": "Analytics"
    },
    "Car_Price_Prediction": {
        "abstract": "Predictive regression modeling for automotive pricing. Utilizes XGBoost and Random Forest on structured data with extensive Feature Engineering.",
        "tags": ["Regression", "XGBoost", "Predictive Analytics"],
        "category": "Analytics"
    },
    "fifa20-clustering": {
        "abstract": "Unsupervised learning analysis of player attributes using K-Means and Hierarchical Clustering. Successfully segmented players into tactical roles (Defenders vs Attackers) based on performance metrics.",
        "tags": ["Clustering", "K-Means", "Unsupervised Learning", "Sports Analytics"],
        "category": "Analytics"
    },
    "fifa_cluster": {
        "abstract": "Unsupervised learning analysis of player attributes using K-Means and Hierarchical Clustering. Successfully segmented players into tactical roles (Defenders vs Attackers) based on performance metrics.",
        "tags": ["Clustering", "K-Means", "Unsupervised Learning", "Sports Analytics"],
        "category": "Analytics"
    }
}

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return []

def infer_tags(repo):
    tags = []
    if repo.get('language'):
        tags.append(repo['language'])
    
    name = repo['name'].lower()
    desc = (repo.get('description') or "").lower()
    
    keywords = {
        "python": "Python",
        "react": "React",
        "node": "Node.js",
        "nn": "Neural Networks",
        "cnn": "CNN",
        "lstm": "LSTM",
        "vision": "Computer Vision",
        "nlp": "NLP",
        "data": "Data Science",
        "api": "API",
        "bot": "Automation",
        "agent": "AI Agent"
    }
    
    for k, v in keywords.items():
        if k in name or k in desc:
            if v not in tags:
                tags.append(v)
    
    return tags

def process_data(repos):
    final_data = []
    
    for repo in repos:
        name = repo['name']
        
        # Skip portfolio itself if desired, or keep it
        if name.lower() == f"{USERNAME}.github.io".lower():
            continue
            
        entry = {
            "id": name,
            "title": name.replace("-", " ").replace("_", " ").title(),
            "github": repo['html_url'],
            "year": datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ").year
        }
        
        # Check Tier 1
        if name in TIER_1_DATA:
            t1 = TIER_1_DATA[name]
            entry.update({
                "featured": True,
                "abstract": t1['abstract'],
                "tags": t1['tags'],
                "category": t1['category']
            })
        else:
            # Tier 2
            entry.update({
                "featured": False,
                "abstract": repo.get('description') or "Scientific software archive.",
                "tags": infer_tags(repo),
                "category": "Software Archive"
            })
            
        final_data.append(entry)
        
    # Sort: Featured first, then by year desc
    final_data.sort(key=lambda x: (not x['featured'], -x['year']))
    return final_data

if __name__ == "__main__":
    print("Fetching global repository data...")
    repos = fetch_repos()
    print(f"Found {len(repos)} repositories.")
    
    full_data = process_data(repos)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(full_data)} entries.")
