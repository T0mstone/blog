import sys
from pathlib import Path

def process(s):
	s = s.replace('\\\n', '').replace('\n', '<br />')
	return s

def add_boilerplate(cont, title, subtitle=None):
	indent1 = ' '*8
	indent2 = ' '*12

	subtitle = "" if subtitle is None else f"\n{indent1}<center class=\"faint\">\n{indent2}{subtitle}\n{indent1}</center>"
	return f"""<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8" />
	<title> {title} - Tom's Blog</title>
	<link rel="stylesheet" type="text/css" href="../style.css">
</head>
<body>
	<div class="title">
		<h2>{title}</h2>{subtitle}
	</div>
	<div class="content">
		{cont}
	</div>
</body>
</html>"""

def split_post_src(s):
	spl = tuple(s.split('\n', 1))
	head, text = spl if len(spl) == 2 else (spl[0], '')
	spl = tuple(s.strip() for s in head.split('--', 1))
	title, subtitle = spl if len(spl) == 2 else (spl[0], None)
	return title, subtitle, text

def list_post_srcs():
	return [path for path in Path('src').iterdir() if path.name not in ['.DS_Store', 'index_src.html']]

def make_hub():
	def inner(template, quote, posts):
		post_str = ('\n' + ' '*8).join(f'<a href="post/{filename}">{title}</a>' for filename, title in posts)
		return template.replace('%quote', quote).replace('%posts', post_str)

	posts = [(path.stem + '.html', split_post_src(path.read_text())[0]) for path in list_post_srcs()]
	quote = Path('quote.txt').read_text()
	with open('src/index_src.html', 'r') as f:
		template = f.read()
	return inner(template, quote, posts)

def main():
	for path in list_post_srcs():
		print(f'compiling {path.name}...')
		title, subtitle, text = split_post_src(path.read_text())
		res = add_boilerplate(process(text), title, subtitle)
		filename = path.stem + '.html'
		path2 = Path('post') / filename
		path2.write_text(res)
	print('compiling index.html...')
	index = make_hub()
	Path('index.html').write_text(index)


if __name__ == '__main__':
	main()