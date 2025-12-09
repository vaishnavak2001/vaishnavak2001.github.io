import json
import os
import urllib.request
from datetime import datetime

# --- CONFIGURATION ---
USERNAME = "vaishnavak2001"
OUTPUT_FILE = "_data/research_data.json"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# --- FEATURED PROJECTS (User Defined) ---
# Mapping Repo Names (or creating virtual ones) to User Descriptions
FEATURED_PROJECTS = {
    # Group 1: Intelligent Diagnostic Signal & Image Processing
    "ecg-classification-cnn-lstm": {
        "title": "ECG Arrhythmia Detection",
        "abstract": "Engineered a hybrid CNN-LSTM model for the MIT-BIH dataset, implementing digital filtering and normalization for real-time anomaly detection.",
        "tags": ["CNN-LSTM", "Signal Processing", "MIT-BIH", "Real-time"],
        "category": "Signal Processing"
    },
    "EEG-Seizure-Detection": { # Virtual or Real
        "title": "EEG Seizure Detection",
        "abstract": "Developed CNN-based models for time-series EEG signal analysis, utilizing feature extraction to identify pathological waveforms.",
        "tags": ["CNN", "EEG", "Time-Series", "Feature Extraction"],
        "category": "Signal Processing",
        "virtual": True, # Flag to create if repo not found
        "url": "https://github.com/vaishnavak2001" 
    },
    "PhysioNet-ECG-Digitization": { # Virtual or Real
        "title": "PhysioNet ECG Digitization System",
        "abstract": "Developed an automated 'Computer Vision to Time-Series' pipeline to digitize historical paper ECG scans. Implemented a DL architecture using YOLOv8 for layout detection and Swin Transformers for signal extraction, featuring dynamic calibration and artifact removal.",
        "tags": ["YOLOv8", "Swin Transformers", "Computer Vision", "Digitization"],
        "category": "Signal Processing",
        "virtual": True,
        "url": "https://github.com/vaishnavak2001"
    },
    
    # Group 2: Medical Image Analysis
    "Pneumonia-chest-X-Ray-classification": {
        "title": "Pneumonia Detection",
        "abstract": "Built diagnostic tools by fine-tuning pre-trained CNN architectures (VGG16, ResNet) using transfer learning, extensive data augmentation, and hyperparameter optimization for X-ray classification.",
        "tags": ["VGG16", "ResNet", "Transfer Learning", "Medical Imaging"],
        "category": "Medical Imaging"
    },
    "Diabetic-Retinopathy-Detection": {
        "title": "Diabetic Retinopathy Detection",
        "abstract": "Built diagnostic tools by fine-tuning pre-trained CNN architectures (VGG16, ResNet) using transfer learning, extensive data augmentation, and hyperparameter optimization for fundus image classification.",
        "tags": ["VGG16", "ResNet", "Transfer Learning", "Medical Imaging"],
        "category": "Medical Imaging"
    },
    
    # Group 3: Control Systems & Predictive Analytics
    "ControlGym-mass-spring-damper": {
        "title": "ControlGym: Mass-Spring-Damper",
        "abstract": "Reinforcement Learning environment for classical control problems. Investigated Deep RL (PPO, SAC) versus classical optimal control (LQR) in stochastic environments, demonstrating RL's robustness.",
        "tags": ["Reinforcement Learning", "Control Theory", "OpenAI Gym", "PPO"],
        "category": "Control Systems"
    },
    
    # Group 4: Generative AI & Agents (New Requests)
    "Welltrack-ai": {
        "title": "WellTrack AI",
        "abstract": "Comprehensive health monitoring system using AI agents to track and predict wellness metrics. Integrates predictive modeling with a user-friendly interface.",
        "tags": ["Generative AI", "Health Tech", "Python"],
        "category": "Generative AI"
    },
    "restaurant-rag-agent": {
        "title": "Restaurant RAG Agent",
        "abstract": "Retrieval-Augmented Generation (RAG) agent designed for restaurant recommendation and query handling. Utilizes vector databases to provide context-aware responses.",
        "tags": ["RAG", "LLMs", "LangChain", "Vector DB"],
        "category": "Generative AI"
    },
    "capstone-project-the-agentops-guardian-5dgai": {
        "title": "AgentOps Guardian",
        "abstract": "Capstone project focusing on operationalizing AI agents. Implements monitoring, safety guardrails, and performance tracking for autonomous agent systems.",
        "tags": ["AgentOps", "AI Safety", "Autonomous Agents"],
        "category": "Generative AI"
    },
    "career_agent": {
        "title": "Autonomous Career Agent",
        "abstract": "AI-driven career counselor agent that aggregates job market data and matches user profiles with opportunities using natural language processing.",
        "tags": ["NLP", "AI Agents", "Career Tech"],
        "category": "Generative AI"
    },
     "skin-disorder-detection": {
        "title": "Skin Disorder Detection",
        "abstract": "Multiclass classification of Erythemato-Squamous Diseases (ESD) using clinical and histopathological attributes. Comparative analysis of Random Forest (93% acc), SVM, and XGBoost.",
        "tags": ["Dermatology", "Random Forest", "Medical AI"],
        "category": "Medical Imaging"
    }
}

def fetch_repos():
    # Attempt to fetch repos. If token fails, return empty list.
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}. Using sanitized local backup if available.")
        # Fallback to reading existing sanitized projects.json if API fails
        try:
             with open('_data/projects.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

def infer_tags(repo):
    tags = []
    if repo.get('language'):
        tags.append(repo['language'])
    return tags

def process_data(repos):
    final_data = []
    processed_repos = set()

    # 1. Add Featured Projects (Real & Virtual)
    for key, info in FEATURED_PROJECTS.items():
        # Check if this key matches a real repo
        matching_repo = next((r for r in repos if r['name'].lower() == key.lower()), None)
        
        entry = {
            "id": key,
            "title": info['title'],
            "abstract": info['abstract'],
            "tags": info['tags'],
            "category": info['category'],
            "featured": True,
            "year": 2025 # Default
        }

        if matching_repo:
            entry["github"] = matching_repo['html_url']
            entry["year"] = datetime.strptime(matching_repo['created_at'].split("T")[0], "%Y-%m-%d").year
            processed_repos.add(matching_repo['name'])
        else:
            # Virtual Entry
            if info.get('virtual'):
                entry["github"] = info.get('url', f"https://github.com/{USERNAME}")
                entry["year"] = 2024
            else:
                continue # Skip if not virtual and not found

        final_data.append(entry)

    # 2. Add Remaining Repos as Archive
    for repo in repos:
        name = repo['name']
        if name in processed_repos or name.lower() in [k.lower() for k in FEATURED_PROJECTS.keys()]:
            continue
        if name.lower() == f"{USERNAME}.github.io".lower():
            continue

        entry = {
            "id": name,
            "title": name.replace("-", " ").replace("_", " ").title(),
            "github": repo['html_url'],
            "year": datetime.strptime(repo['created_at'].split("T")[0], "%Y-%m-%d").year,
            "featured": False,
            "abstract": repo.get('description') or "Scientific software archive.",
            "tags": infer_tags(repo),
            "category": "Software Archive"
        }
        final_data.append(entry)
        
    final_data.sort(key=lambda x: (not x['featured'], -x['year']))
    return final_data

if __name__ == "__main__":
    print("Fetching repository data...")
    repos = fetch_repos()
    print(f"Found {len(repos)} repositories.")
    
    full_data = process_data(repos)
    
    # Strip Unicode for safety
    def sanitize(obj):
        if isinstance(obj, str): return obj.encode('ascii', 'ignore').decode('ascii')
        if isinstance(obj, list): return [sanitize(i) for i in obj]
        if isinstance(obj, dict): return {k: sanitize(v) for k, v in obj.items()}
        return obj
        
    full_data = sanitize(full_data)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(full_data, f, indent=2)
        
    print(f"Generated {len(full_data)} projects in {OUTPUT_FILE}")
