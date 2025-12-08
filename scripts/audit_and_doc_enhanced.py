#!/usr/bin/env python3
"""
Enhanced Audit Script with Deep Semantic Analysis
Generates synthesized abstracts and technical architecture descriptions
"""
import urllib.request
import urllib.error
import json
import os
import sys
import time
import base64

USERNAME = "vaishnavak2001"
OUTPUT_FILE = "_data/projects.json"
TOKEN = os.environ.get("GITHUB_TOKEN")

def get_headers():
    headers = {"User-Agent": "Portfolio-Audit-Agent"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    return headers

def fetch_repos(page=1):
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error fetching repos: {e}")
        return []

def get_readme_content(repo_name, default_branch):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/readme"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
    except urllib.error.HTTPError:
        return ""

def get_languages(repo_name):
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/languages"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError:
        return {}

def get_file_content(repo_name, file_path, default_branch):
    """Fetch specific file content from repository"""
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/contents/{file_path}?ref={default_branch}"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if data.get('encoding') == 'base64':
                return base64.b64decode(data['content']).decode('utf-8', errors='ignore')
    except:
        pass
    return None

def analyze_tech_stack(languages, repo_name, default_branch):
    """Analyze and return detailed tech stack"""
    sorted_langs = sorted(languages.items(), key=lambda item: item[1], reverse=True)
    primary_langs = [l[0] for l in sorted_langs]
    
    # Deep analysis based on file detection
    frameworks = []
    architecture_notes = []
    
    # Check for package.json (Node.js/JavaScript)
    package_json = get_file_content(repo_name, 'package.json', default_branch)
    if package_json:
        try:
            pkg = json.loads(package_json)
            deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
            
            if any(k in deps for k in ['react', 'react-dom']):
                frameworks.append('React')
                architecture_notes.append("Component-based UI architecture using React")
            if 'next' in deps:
                frameworks.append('Next.js')
                architecture_notes.append("Server-side rendering with Next.js framework")
            if 'express' in deps:
                frameworks.append('Express')
                architecture_notes.append("RESTful API built on Express.js")
            if 'vue' in deps:
                frameworks.append('Vue.js')
                architecture_notes.append("Reactive UI framework with Vue.js")
            if 'typescript' in deps or 'TypeScript' in primary_langs:
                architecture_notes.append("Type-safe development with TypeScript")
        except:
            pass
    
    # Check for requirements.txt (Python)
    requirements = get_file_content(repo_name, 'requirements.txt', default_branch)
    if requirements:
        req_lower = requirements.lower()
        if 'flask' in req_lower:
            frameworks.append('Flask')
            architecture_notes.append("Lightweight WSGI web framework using Flask")
        if 'django' in req_lower:
            frameworks.append('Django')
            architecture_notes.append("Full-stack MVC architecture with Django")
        if 'tensorflow' in req_lower or 'keras' in req_lower:
            frameworks.append('TensorFlow/Keras')
            architecture_notes.append("Deep learning pipeline using TensorFlow/Keras")
        if 'pytorch' in req_lower:
            frameworks.append('PyTorch')
            architecture_notes.append("Neural network architecture built on PyTorch")
        if 'scikit-learn' in req_lower or 'sklearn' in req_lower:
            frameworks.append('Scikit-learn')
            architecture_notes.append("Machine learning models using Scikit-learn")
        if 'pandas' in req_lower and 'numpy' in req_lower:
            architecture_notes.append("Data processing pipeline with Pandas and NumPy")
        if 'streamlit' in req_lower:
            frameworks.append('Streamlit')
            architecture_notes.append("Interactive web application using Streamlit")
    
    # Check for Dockerfile
    dockerfile = get_file_content(repo_name, 'Dockerfile', default_branch)
    if dockerfile:
        architecture_notes.append("Containerized deployment using Docker")
    
    return primary_langs, frameworks, architecture_notes

def synthesize_abstract(repo, readme_content, languages, frameworks):
    """Generate a research-grade abstract based on available information"""
    name = repo['name']
    description = repo.get('description') or ''
    
    # Extract purpose from README or description
    purpose = description if description else f"Implementation focused on {name.replace('-', ' ').replace('_', ' ')}"
    
    # Infer domain from name and languages
    name_lower = name.lower()
    domain_context = ""
    
    if any(term in name_lower for term in ['ml', 'neural', 'cnn', 'lstm', 'detection', 'classification', 'prediction']):
        domain_context = "This project addresses challenges in machine learning and predictive analytics. "
    elif any(term in name_lower for term in ['web', 'api', 'server', 'client']):
        domain_context = "This system implements modern web architecture patterns. "
    elif any(term in name_lower for term in ['data', 'analysis', 'visualization']):
        domain_context = "This analytical framework focuses on data-driven insights. "
    elif any(term in name_lower for term in ['rl', 'agent', 'gym', 'control']):
        domain_context = "This project explores reinforcement learning and autonomous systems. "
    
    # Check for specific ML/AI keywords in README
    if readme_content:
        readme_lower = readme_content.lower()
        if 'deep learning' in readme_lower or 'neural network' in readme_lower:
            domain_context = "This research implements deep learning methodologies for pattern recognition. "
        elif 'computer vision' in readme_lower or 'image' in readme_lower:
            domain_context = "This computer vision system processes visual data for automated analysis. "
    
    # Build tech context
    tech_context = ""
    if 'Python' in languages and any(fw in ['TensorFlow/Keras', 'PyTorch', 'Scikit-learn'] for fw in frameworks):
        tech_context = "utilizing state-of-the-art machine learning frameworks"
    elif 'JavaScript' in languages or 'TypeScript' in languages:
        tech_context = "leveraging modern JavaScript ecosystem technologies"
    elif 'Python' in languages:
        tech_context = "built on Python's robust scientific computing stack"
    
    abstract = f"{domain_context}{purpose}. Implementation {tech_context}, demonstrating practical applications in software engineering and computational problem-solving."
    
    return abstract

def synthesize_technical_architecture(languages, frameworks, architecture_notes, repo_name):
    """Generate detailed technical architecture description"""
    if not languages:
        return "Technical architecture to be documented. Core implementation uses standard software engineering patterns."
    
    # Start with primary language
    primary_lang = languages[0] if languages else "General"
    
    arch_parts = []
    
    # Language and paradigm
    if 'Python' in languages:
        arch_parts.append(f"**Backend/Core:** Python-based implementation emphasizing scientific computing and data processing capabilities.")
    elif 'JavaScript' in languages or 'TypeScript' in languages:
        arch_parts.append(f"**Frontend/Runtime:** JavaScript/TypeScript enabling dynamic client-side interactions and modern web capabilities.")
    elif 'Jupyter Notebook' in languages:
        arch_parts.append(f"**Research Environment:** Interactive computational notebooks for exploratory analysis and visualization.")
    
    # Frameworks
    if frameworks:
        fw_str = ", ".join(frameworks)
        arch_parts.append(f"**Framework Stack:** {fw_str} providing structured development patterns and accelerated implementation.")
    
    # Architecture patterns from notes
    if architecture_notes:
        arch_parts.append(f"**Architecture Patterns:** {' '.join(architecture_notes)}")
    
    # Infer patterns from repo name
    name_lower = repo_name.lower()
    if 'api' in name_lower or 'server' in name_lower:
        arch_parts.append("**Design Pattern:** RESTful service architecture with modular endpoint design.")
    if 'agent' in name_lower:
        arch_parts.append("**Agent Architecture:** Autonomous decision-making system with state management and policy execution.")
    
    if not arch_parts:
        return f"**Core Stack:** {primary_lang}. Implementation follows industry-standard software development practices with modular architecture for maintainability and scalability."
    
    return "\n\n".join(arch_parts)

def main():
    print(f"Starting Deep Semantic Analysis for {USERNAME}...")
    
    all_repos = []
    page = 1
    while True:
        repos = fetch_repos(page)
        if not repos:
            break
        all_repos.extend(repos)
        page += 1
        
    print(f"Found {len(all_repos)} repositories.")
    
    projects_data = []
    
    for repo in all_repos:
        if repo['fork']:
            continue
            
        print(f"Deep analyzing {repo['name']}...")
        
        # Fetch data
        readme_content = get_readme_content(repo['name'], repo['default_branch'])
        languages_raw = get_languages(repo['name'])
        
        # Analyze
        tech_stack, frameworks, arch_notes = analyze_tech_stack(languages_raw, repo['name'], repo['default_branch'])
        
        # Synthesize
        abstract = synthesize_abstract(repo, readme_content, tech_stack, frameworks)
        technical_architecture = synthesize_technical_architecture(tech_stack, frameworks, arch_notes, repo['name'])
        
        project_entry = {
            "name": repo['name'],
            "description": repo['description'],
            "url": repo['html_url'],
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "languages": tech_stack,
            "frameworks": frameworks,
            "abstract": abstract,
            "technical_architecture": technical_architecture,
            "documentation": readme_content,
            "updated_at": repo['updated_at']
        }
        projects_data.append(project_entry)
        
        if not TOKEN:
            time.sleep(1)

    # Sort by impact
    projects_data.sort(key=lambda x: (x['stars'], x['updated_at']), reverse=True)
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects_data, f, indent=2)
        
    print(f"Deep analysis complete. Enhanced data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
