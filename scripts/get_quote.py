import random
from pathlib import Path

def get_quote():
	quotes = Path('quotes.txt').read_text().split('\n')
	selected_quotes = [line[2:] for line in quotes if line.startswith('> ')]
	if len(selected_quotes) == 0:
		return quotes[random.randrange(len(quotes))]
	else:
		return selected_quotes[0]

if __name__ == '__main__':
	print(get_quote(), end="")