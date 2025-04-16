import os

EXCLUDE_DIRS = {'archive', '.git', '.github', '__pycache__', 'images'}

def format_dir_name(name):
    # PascalCase → 공백 + 대문자 처리 (e.g. ModelEvaluation → Model Evaluation)
    return ''.join([' ' + c if c.isupper() else c for c in name]).strip().title()

def generate_readme(root='.'):
    lines = ['# 📘 Today I Learned\n']

    for topic in sorted(os.listdir(root)):
        topic_path = os.path.join(root, topic)
        if topic in EXCLUDE_DIRS or not os.path.isdir(topic_path):
            continue

        # 디렉토리명 보기 좋게 포맷
        pretty_topic = format_dir_name(topic)
        lines.append(f"## 📂 {pretty_topic}\n")

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
