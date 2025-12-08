import urllib.request
import urllib.error
import json
import os
import sys
import time

# Configuration
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
        if e.code == 403:
            print("Rate limit exceeded. Please provide GITHUB_TOKEN.")
        return []

def get_readme_content(repo_name, default_branch):
    # Try fetching README.md, Readme.md, README.txt etc.
    # Standard GitHub API for README
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/readme"
    try:
        req = urllib.request.Request(url, headers=get_headers())
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # Content is base64 encoded
            import base64
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

def analyze_tech_stack(languages):
    # Sort by bytes and return top list
    sorted_langs = sorted(languages.items(), key=lambda item: item[1], reverse=True)
    return [l[0] for l in sorted_langs]

def generate_virtual_readme(repo, languages):
    stack = analyze_tech_stack(languages)
    stack_str = ", ".join(stack)
    
    return f"""# {repo['name']}

## Abstract
{repo['description'] or "No description provided."}

## Technical Architecture
**Stack:** {stack_str}

This project utilizes {stack[0] if stack else 'standard technologies'}.

## Installation & Usage
```bash
git clone {repo['html_url']}
cd {repo['name']}
# See source code for specific build instructions
```
"""

def main():
    print(f"Starting Deep Audit for {USERNAME}...")
    
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
            continue # Optionally skip forks or include them
            
        print(f"Analyzing {repo['name']}...")
        
        # 1. Fetch README
        readme_content = get_readme_content(repo['name'], repo['default_branch'])
        
        # 2. Fetch Languages
        languages = get_languages(repo['name'])
        tech_stack = analyze_tech_stack(languages)
        
        is_virtual = False
        final_doc = readme_content
        
        # 3. Audit
        if not readme_content or len(readme_content) < 200:
            print(f"  -> Weak documentation detected. Generating Virtual README.")
            is_virtual = True
            final_doc = generate_virtual_readme(repo, languages)
        
        project_entry = {
            "name": repo['name'],
            "description": repo['description'],
            "url": repo['html_url'],
            "stars": repo['stargazers_count'],
            "forks": repo['forks_count'],
            "languages": tech_stack,
            "has_good_readme": not is_virtual,
            "documentation": final_doc,
            "updated_at": repo['updated_at']
        }
        projects_data.append(project_entry)
        
        # Sleep briefly to be nice to API if no token
        if not TOKEN:
            time.sleep(1)

    # Sort: Impact (Stars) then Date
    projects_data.sort(key=lambda x: (x['stars'], x['updated_at']), reverse=True)
    
    # Save
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects_data, f, indent=2)
        
    print(f"Audit complete. Data saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
