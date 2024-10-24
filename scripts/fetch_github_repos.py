import requests
import os

owner = "melvinhqb"

github_api_url = f"https://api.github.com/users/{owner}/repos"

response = requests.get(github_api_url)
repos = response.json()

if response.status_code != 200:
    print(f"Error: Unable to retrieve repositories (code {response.status_code})")
    exit(1)

output_dir = "./content/projects/github"
os.makedirs(output_dir, exist_ok=True)

for repo in repos:
    repo_name = repo['name']
    repo_description = repo['description'] or "Pas de description disponible."
    repo_url = repo['html_url']
    repo_created_at = repo['created_at']
    repo_updated_at = repo['updated_at']
    repo_topics = repo['topics']

    readme_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    readme_response = requests.get(readme_url)

    if readme_response.status_code == 200:
        readme_data = readme_response.json()
        readme_content_url = readme_data['download_url']
        readme_content = requests.get(readme_content_url).text
        print
    else:
        readme_content = ""

    hugo_content_path = os.path.join(output_dir, f"{repo_name}.md")
    with open(hugo_content_path, 'w', encoding='utf-8') as f:
        f.write(f"---\n")
        f.write(f"title: \"{repo_name}\"\n")
        f.write(f"description: \"{repo_description}\"\n")
        f.write(f"summary: \"{repo_description}\"\n")
        f.write(f"categories: {repo_topics}\n")
        f.write(f"date: \"{repo_created_at}\"\n")
        f.write(f"lastmod: \"{repo_updated_at}\"\n")
        f.write(f"links:\n")
        f.write(f"  github_link:\n")
        f.write(f"    text: \"Open with GitHub\"\n")
        f.write(f"    name: \"github\"\n")
        f.write(f"    href: \"{repo_url}\"\n")
        f.write(f"---\n\n")
        f.write(readme_content)

    print(f"The file for {repo_name} has been generated in {hugo_content_path}")

    