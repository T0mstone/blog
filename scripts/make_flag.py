import sys

def get_flag(code):
	code = code.lower()
	if code == 'en':
		code = 'gb'
	# this makes use of unicode's flag handling to translate literally any country code into a unicode flag emoji
	code_a = 127462
	return ''.join([chr(code_a + ord(c) - ord('a')) for c in code])

if __name__ == '__main__':
	if len(sys.argv) > 1 and sys.argv[1] != '':
		print(get_flag(sys.argv[1]), end="")