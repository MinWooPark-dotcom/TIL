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
    'dns': 'DNS',
    'aws': 'AWS',
    'rds': 'RDS',
    'iam': 'IAM',
    'cloudfront': 'CloudFront',
    'tls': 'TLS',
    'ec2': 'EC2',
    'ami': 'AMI'
}

def format_dir_name(name):
    lower = name.lower()
    if lower in SPECIAL_CASING:
        return SPECIAL_CASING[lower]
    
    # PascalCase → 공백 + 대문자 처리 (e.g. ModelEvaluation → Model Evaluation)
    return ''.join([' ' + c if c.isupper() else c for c in name]).strip().title()

def format_title(filename):
    base = filename[:-3].replace('_', ' ')
    words = base.split()
    formatted = []

    for word in words:
        lower = word.lower()
        print(lower)
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

        lines.append(f"## 📂 {format_dir_name(topic)}\n")

        # 하위 디렉토리가 있는 경우 (예: AWS/Storage/)
        subdirs = [d for d in os.listdir(topic_path) if os.path.isdir(os.path.join(topic_path, d))]
        if subdirs:
            for sub in sorted(subdirs):
                sub_path = os.path.join(topic_path, sub)
                md_files = [f for f in sorted(os.listdir(sub_path)) if f.endswith('.md')]
                if md_files:
                    lines.append(f"### {format_dir_name(sub)}")
                    for f in md_files:
                        title = format_title(f)
                        path = f"{topic}/{sub}/{f}"
                        lines.append(f"- [{title}]({path})")
                    lines.append("")

        # 루트 디렉토리 내 .md 파일 처리
        root_md_files = [f for f in sorted(os.listdir(topic_path)) if f.endswith('.md')]
        for f in root_md_files:
            title = format_title(f)
            path = f"{topic}/{f}"
            lines.append(f"- [{title}]({path})")

        lines.append('')

    with open('README.md', 'w') as f:
        f.write('\n'.join(lines))

if __name__ == "__main__":
    generate_readme()