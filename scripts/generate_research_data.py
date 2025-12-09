#!/usr/bin/env python3
"""
Generate comprehensive research_data.json from ALL GitHub projects
"""
import json

# Load the complete projects data
with open('_data/projects.json', 'r', encoding='utf-8') as f:
    all_projects = json.load(f)

# Map to research data format
research_data = []

# Category mapping based on project name/tags
def categorize_project(name, languages):
    name_lower = name.lower()
    if any(term in name_lower for term in ['diabetic', 'pneumonia', 'skin', 'ecg', 'health', 'medical']):
        return 'medical', 'high'
    elif any(term in name_lower for term in ['detection', 'recognition', 'classification', 'face', 'gender']):
        return 'computer-vision', 'medium'
    elif any(term in name_lower for term in ['prediction', 'cluster', 'analysis', 'fifa', 'titanic', 'car']):
        return 'analytics', 'medium'
    elif any(term in name_lower for term in ['agent', 'ai', 'web', 'creator']):
        return 'ai-systems', 'medium'
    elif any(term in name_lower for term in ['control', 'drone', 'rl', 'gym']):
        return 'control-systems', 'medium'
    else:
        return 'general', 'low'

def get_tags(languages, frameworks, name):
    tags = []
    
    # From languages
    if 'Python' in languages or 'Jupyter Notebook' in languages:
        if any(fw in str(frameworks) for fw in ['TensorFlow', 'Keras', 'PyTorch']):
            tags.append('Deep Learning')
        if any(fw in str(frameworks) for fw in ['Scikit-learn', 'XGBoost']):
            tags.append('Machine Learning')
    
    # From frameworks
    if 'Streamlit' in str(frameworks) or 'Flask' in str(frameworks):
        tags.append('Web Applications')
    
    # From project name
    name_lower = name.lower()
    if any(term in name_lower for term in ['medical', 'health', 'diabetic', 'pneumonia', 'skin', 'ecg']):
        tags.append('Medical AI')
    if any(term in name_lower for term in ['detection', 'classification', 'recognition', 'vision']):
        tags.append('Computer Vision')
    if any(term in name_lower for term in ['prediction', 'analysis', 'analytics']):
        tags.append('Predictive Analytics')
    if any(term in name_lower for term in ['control', 'rl', 'reinforcement', 'agent']):
        tags.append('Control Science')
    if any(term in name_lower for term in ['data', 'science', 'cluster']):
        tags.append('Data Science')
    
    # Default if empty
    if not tags:
        tags = ['Data Science']
    
    return tags[:3]  # Max 3 tags per project

for proj in all_projects:
    category, impact = categorize_project(proj['name'], proj.get('languages', []))
    
    research_entry = {
        "title": proj['name'].replace('-', ' ').replace('_', ' ').title(),
        "abstract": proj.get('abstract', proj.get('description', 'Research implementation in progress.')),
        "tags": get_tags(
            proj.get('languages', []),
            proj.get('frameworks', []),
            proj['name']
        ),
        "github": proj['url'],
        "category": category,
        "impact": impact,
        "stars": proj.get('stars', 0)
    }
    
    research_data.append(research_entry)

# Sort by impact then stars
impact_order = {'high': 3, 'medium': 2, 'low': 1}
research_data.sort(key=lambda x: (impact_order.get(x['impact'], 0), x['stars']), reverse=True)

# Save
with open('_data/research_data.json', 'w', encoding='utf-8') as f:
    json.dump(research_data, f, indent=2, ensure_ascii=True)

print(f"Generated research_data.json with {len(research_data)} projects")
