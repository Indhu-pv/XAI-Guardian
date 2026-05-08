import glob
for f in glob.glob('*_engine.py'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content.replace('\\"\\"\\"', '\"\"\"'))
