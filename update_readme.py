import os

EXCLUDE_DIRS = {'archive', '.git', '.github', '__pycache__'}

def generate_readme(root='.'):
    lines = ['# 📘 Today I Learned\n']
    lines.append('---\n')

    for topic in sorted(os.listdir(root)):
        topic_path = os.path.join(root, topic)
        if topic in EXCLUDE_DIRS or not os.path.isdir(topic_path):
            continue

        lines.append(f"## 📂 {topic}\n")
        for file in sorted(os.listdir(topic_path)):
            if file.endswith('.md'):
                title = file[:-3].replace('_', ' ').capitalize()
                path = f"{topic}/{file}"
                lines.append(f"- [{title}]({path})")
        lines.append('')  # 줄 바꿈

    with open('README.md', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    generate_readme()
