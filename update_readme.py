import os

EXCLUDE_DIRS = {
    'archive',
    '.git',
    '.github',
    '__pycache__',
    'images',
    'Algorithm',
    'Certificate',
    'DataStructure',
    'MLOps',
    'RegularExpression'
}

# 특정 단어에 대해 커스텀 케이싱 설정
SPECIAL_CASING = {
    'dns': 'DNS'
}

def format_dir_name(name):
    # PascalCase → 공백 + 대문자 처리 (e.g. ModelEvaluation → Model Evaluation)
    return ''.join([' ' + c if c.isupper() else c for c in name]).strip().title()

def format_title(filename):
    base = filename[:-3].replace('_', ' ')
    words = base.split()
    formatted = []

    for word in words:
        lower = word.lower()
        if lower in SPECIAL_CASING:
            formatted.append(SPECIAL_CASING[lower])
        else:
            formatted.append(word.capitalize())

    return ' '.join(formatted)

def generate_readme(root='.'):
    lines = ['# 📘 Today I Learned\n']

    for topic in sorted(os.listdir(root)):
        topic_path = os.path.join(root, topic)
        if topic in EXCLUDE_DIRS or not os.path.isdir(topic_path):
            continue

        pretty_topic = format_dir_name(topic)
        lines.append(f"## 📂 {pretty_topic}\n")

        for file in sorted(os.listdir(topic_path)):
            if file.endswith('.md'):
                title = format_title(file)
                path = f"{topic}/{file}"
                lines.append(f"- [{title}]({path})")

        lines.append('')

    with open('README.md', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    generate_readme()