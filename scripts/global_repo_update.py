#!/usr/bin/env python3
"""
Global Repository Documentation Automation Script
Architect Mode: Full Control Granted
"""
import urllib.request
import urllib.error
import json
import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

# Configuration
USERNAME = "vaishnavak2001"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
TEMP_WORKSPACE = Path("C:/temp/repo_automation")
LOG_FILE = Path("C:/temp/repo_automation_log.txt")

class RepoUpdater:
    def __init__(self):
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0
        }
        self.log_messages = []
        
    def log(self, message):
        """Log to console and file"""
        # Replace Unicode symbols with ASCII equivalents for Windows console
        message = message.replace('→', '->').replace('✗', 'X').replace('✓', 'OK')
        print(message)
        self.log_messages.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        
    def save_log(self):
        """Save log to file"""
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.log_messages))
    
    def get_headers(self):
        """Get headers for GitHub API"""
        headers = {"User-Agent": "Portfolio-Update-Agent"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"token {GITHUB_TOKEN}"
        return headers
    
    def fetch_repos(self):
        """Fetch all user repositories"""
        self.log(f"Fetching repositories for {USERNAME}...")
        all_repos = []
        page = 1
        
        while True:
            url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}"
            try:
                req = urllib.request.Request(url, headers=self.get_headers())
                with urllib.request.urlopen(req) as response:
                    repos = json.loads(response.read().decode())
                    if not repos:
                        break
                    all_repos.extend(repos)
                    page += 1
            except urllib.error.HTTPError as e:
                self.log(f"Error fetching repos: {e}")
                break
        
        # Filter out forks (optional - you can remove this if you want to update forks too)
        repos = [r for r in all_repos if not r['fork']]
        self.log(f"Found {len(repos)} repositories (excluding forks)")
        return repos
    
    def analyze_tech_stack(self, repo_path):
        """Analyze repository to determine tech stack"""
        stack = []
        frameworks = []
        
        # Check for common files
        checks = {
            'package.json': ('JavaScript/Node.js', ['Express', 'React', 'Vue', 'Next.js']),
            'requirements.txt': ('Python', ['Flask', 'Django', 'FastAPI', 'TensorFlow', 'PyTorch']),
            'Gemfile': ('Ruby', ['Rails', 'Sinatra']),
            'pom.xml': ('Java/Maven', ['Spring Boot']),
            'build.gradle': ('Java/Gradle', ['Spring Boot']),
            'go.mod': ('Go', []),
            'Cargo.toml': ('Rust', []),
            'composer.json': ('PHP', ['Laravel', 'Symfony']),
            'Dockerfile': ('Docker', []),
            '.ipynb': ('Jupyter Notebook', [])
        }
        
        for file, (tech, possible_frameworks) in checks.items():
            if (repo_path / file).exists() or list(repo_path.glob(f"**/{file}")):
                stack.append(tech)
                # Try to detect frameworks
                try:
                    if file == 'package.json':
                        with open(repo_path / file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                            for fw in possible_frameworks:
                                if fw.lower() in [k.lower() for k in deps.keys()]:
                                    frameworks.append(fw)
                    elif file == 'requirements.txt':
                        with open(repo_path / file, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                            for fw in possible_frameworks:
                                if fw.lower() in content:
                                    frameworks.append(fw)
                except:
                    pass
        
        # Check file extensions
        extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin'
        }
        
        for ext, lang in extensions.items():
            if list(repo_path.glob(f"**/*{ext}")) and lang not in stack:
                stack.append(lang)
        
        return stack, frameworks
    
    def generate_readme(self, repo_info, repo_path):
        """Generate comprehensive README content"""
        name = repo_info['name']
        description = repo_info.get('description') or 'A project by vaishnavak2001'
        tech_stack, frameworks = self.analyze_tech_stack(repo_path)
        
        # Read existing README to preserve any unique content
        existing_readme = ""
        readme_path = repo_path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    existing_readme = f.read()
            except:
                pass
        
        # Only generate new README if existing one is weak (<300 chars)
        if existing_readme and len(existing_readme) > 300:
            self.log(f"  → README exists and is comprehensive, skipping generation")
            return None
        
        # Generate README
        tech_stack_str = ', '.join(tech_stack) if tech_stack else 'General'
        frameworks_str = ', '.join(frameworks) if frameworks else ''
        
        readme_content = f"""# {name}

{description}

## 📋 Abstract

This project demonstrates {description.lower() if description != 'A project by vaishnavak2001' else 'practical implementation of software engineering principles'}.

## 🛠️ Technical Architecture

**Primary Stack:** {tech_stack_str}
"""
        
        if frameworks_str:
            readme_content += f"**Frameworks & Libraries:** {frameworks_str}\n"
        
        readme_content += f"""
## 🚀 Installation & Usage

### Prerequisites

"""
        
        # Add specific prerequisites based on stack
        if 'Python' in tech_stack:
            readme_content += "- Python 3.7 or higher\n"
        if 'JavaScript' in tech_stack or 'Node.js' in tech_stack:
            readme_content += "- Node.js 14 or higher\n"
        if 'Docker' in tech_stack:
            readme_content += "- Docker and Docker Compose\n"
        
        readme_content += f"""
### Setup

```bash
# Clone the repository
git clone https://github.com/{USERNAME}/{name}.git
cd {name}
"""
        
        # Add stack-specific setup
        if 'Python' in tech_stack:
            if (repo_path / 'requirements.txt').exists():
                readme_content += """
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```
"""
            else:
                readme_content += """
# Install dependencies (if any)
# Run the application
python *.py
```
"""
        elif 'JavaScript' in tech_stack or 'Node.js' in tech_stack:
            readme_content += """
# Install dependencies
npm install

# Run the application
npm start
```
"""
        else:
            readme_content += """
# Follow project-specific instructions in source files
```
"""
        
        readme_content += f"""
## 📖 Documentation

For detailed implementation specifics, please refer to the source code and inline comments.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is part of the portfolio by [vaishnavak2001](https://github.com/{USERNAME}).

---

**Note:** This README was auto-generated by the Portfolio Documentation Agent. For latest updates, visit the [project repository](https://github.com/{USERNAME}/{name}).
"""
        
        return readme_content
    
    def update_repository(self, repo_info):
        """Clone, update, and push a single repository"""
        repo_name = repo_info['name']
        self.log(f"\n{'='*60}")
        self.log(f"Processing: {repo_name}")
        self.log(f"{'='*60}")
        
        # Skip the portfolio repo itself
        if repo_name == "vaishnavak2001.github.io":
            self.log(f"  → Skipping portfolio repository")
            self.stats['skipped'] += 1
            return
        
        repo_path = TEMP_WORKSPACE / repo_name
        
        try:
            # Clone repository
            clone_url = f"https://{GITHUB_TOKEN}@github.com/{USERNAME}/{repo_name}.git"
            self.log(f"  → Cloning repository...")
            
            if repo_path.exists():
                shutil.rmtree(repo_path)
            
            result = subprocess.run(
                ['git', 'clone', clone_url, str(repo_path)],
                capture_output=True,
                text=True,
                cwd=str(TEMP_WORKSPACE)
            )
            
            if result.returncode != 0:
                self.log(f"  ✗ Clone failed: {result.stderr}")
                self.stats['failed'] += 1
                return
            
            # Generate README
            self.log(f"  → Analyzing tech stack...")
            readme_content = self.generate_readme(repo_info, repo_path)
            
            if readme_content is None:
                self.stats['skipped'] += 1
                return
            
            # Write README
            self.log(f"  → Writing README.md...")
            with open(repo_path / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # Git operations
            self.log(f"  → Committing changes...")
            subprocess.run(['git', 'add', 'README.md'], cwd=str(repo_path), check=True)
            subprocess.run(
                ['git', 'commit', '-m', 'docs(auto): generated comprehensive documentation via portfolio-agent'],
                cwd=str(repo_path),
                check=True
            )
            
            self.log(f"  → Pushing to GitHub...")
            result = subprocess.run(
                ['git', 'push', 'origin', repo_info['default_branch']],
                cwd=str(repo_path),
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                self.log(f"  ✗ Push failed: {result.stderr}")
                self.stats['failed'] += 1
            else:
                self.log(f"  ✓ Successfully updated {repo_name}")
                self.stats['success'] += 1
            
            # Cleanup
            shutil.rmtree(repo_path)
            
        except Exception as e:
            self.log(f"  ✗ Error: {str(e)}")
            self.stats['failed'] += 1
            if repo_path.exists():
                try:
                    shutil.rmtree(repo_path)
                except:
                    pass
    
    def run(self):
        """Main execution function"""
        self.log("="*60)
        self.log("GLOBAL REPOSITORY UPDATE - INITIATED")
        self.log("="*60)
        
        if not GITHUB_TOKEN:
            self.log("ERROR: GITHUB_TOKEN environment variable not set!")
            return
        
        # Create workspace
        TEMP_WORKSPACE.mkdir(parents=True, exist_ok=True)
        
        # Fetch repositories
        repos = self.fetch_repos()
        self.stats['total'] = len(repos)
        
        # Process each repository
        for repo in repos:
            self.update_repository(repo)
            time.sleep(2)  # Rate limiting
        
        # Final report
        self.log("\n" + "="*60)
        self.log("OPERATION COMPLETE")
        self.log("="*60)
        self.log(f"Total Repositories: {self.stats['total']}")
        self.log(f"Successfully Updated: {self.stats['success']}")
        self.log(f"Skipped (Good README): {self.stats['skipped']}")
        self.log(f"Failed: {self.stats['failed']}")
        self.log("="*60)
        
        self.save_log()
        self.log(f"\nFull log saved to: {LOG_FILE}")

if __name__ == "__main__":
    updater = RepoUpdater()
    updater.run()
