import random
import re
from pathlib import Path

def maybe_get(d, k):
	return d[k] if k in d else None

def extract_post_metatdata(s):
	def inner(line):
		spl = tuple(s.strip() for s in line.split(' ', 1))
		return spl if len(spl) == 2 else (spl[0], None)

	return dict(inner(line[1:]) for line in s.split('\n') if line.startswith('!'))

def process(s):
	s = '\n'.join(line for line in s.split('\n') if not line.startswith('!'))
	s = s.replace('\\\n', '')
	
	s = re.sub(r'#(\d)(.+?)(?:\n|$)', r'<h\1>\2</h\1>', s)
	s = re.sub(r'\[([^\s(]+)(?:\(([^)]+?)\))?(?:\s)*([^\]]*?)\]', r'<\1 \2>\3</\1>', s)
	s = re.sub(r'(\n|^)> ([^\n]+)(?:\n)?', r'\1<div class="boxed">\2</div>', s)

	s = s.replace('\n\n', '<p class="vspace"></p>')
	s = s.replace('\n', '<br />')
	return s

def add_boilerplate(cont, meta):
	indent1 = ' '*8
	indent2 = ' '*12

	title = meta['title']
	subtitle = maybe_get(meta, 'subtitle')
	tabtitle = maybe_get(meta, 'tabtitle')

	subtitle = "" if subtitle is None else f"\n{indent1}<center class=\"faint\">\n{indent2}{subtitle}\n{indent1}</center>"
	template = open('post_src.html', 'r').read()
	return template.replace('%tabtitle', title if tabtitle is None else tabtitle) \
		.replace('%title', title) \
		.replace('%subtitle', subtitle) \
		.replace('%content', cont)

def list_post_srcs(include_unfinished=False):
	return [path for path in Path('src').iterdir() if path.name != '.DS_Store' and (include_unfinished or not path.name.startswith('_'))]

def make_hub():
	def make_entry(filename, meta):
		title = meta['title']
		flag = get_flag(meta['lang'])
		n = meta['n']

		return f'<p class="post-link">[{flag}] ({n}) <a href="post/{filename}">{title}</a></p>'

	quotes = Path('quotes.txt').read_text().split('\n')
	selected_quotes = [line[2:] for line in quotes if line.startswith('> ')]
	if len(selected_quotes) == 0:
		quote = quotes[random.randrange(len(quotes))]
	else:
		quote = selected_quotes[0]
	
	with open('index_src.html', 'r') as f:
		template = f.read()

	posts = [(path.stem + '.html', extract_post_metatdata(path.read_text())) for path in list_post_srcs()]
	posts = sorted(posts, key=lambda t: int(t[1]['n']), reverse=True)
	post_str = ('\n' + ' '*8).join(make_entry(filename, meta) for filename, meta in posts)

	return template.replace('%quote', quote).replace('%posts', post_str)

def get_flag(code):
	code = code.lower()
	if code == 'en':
		code = 'gb'
	# this makes use of unicode's flag handling to translate literally any country code into a unicode flag emoji
	code_a = 127462
	return ''.join([chr(code_a + ord(c) - ord('a')) for c in code])

def main():
	for path in list_post_srcs(include_unfinished=True):
		print(f'compiling {path.name}...')
		text = path.read_text()
		meta = extract_post_metatdata(text)
		for (k, e) in {'title': 'title', 'lang': 'language annotation', 'n': 'post number'}.items():
			if k not in meta:
				print(f'"{path.stem}" is missing a {e}')
				continue
		res = add_boilerplate(process(text), meta)
		filename = path.stem + '.html'
		path2 = Path('post') / filename
		path2.write_text(res)
	print('compiling index.html...')
	index = make_hub()
	Path('index.html').write_text(index)


if __name__ == '__main__':
	main()