const urlParams = new URLSearchParams(window.location.search);

function mapGetElementById(id, map) {
	var x = document.getElementById(id);
	if (x !== null) {
		return map(x);
	}
}

function setDarkMode() {
	const dark = urlParams.get('dark') == '1';

	const DARK_BG = '#101510';
	const LIGHT_BG = '#ded';
	const DARK_TEXT = '#993';
	const LIGHT_TEXT = '#000';

	document.body.style.backgroundColor = dark? DARK_BG : LIGHT_BG;
	document.body.style.color = dark? DARK_TEXT : LIGHT_TEXT;
	mapGetElementById('posts', posts => {
		for (p of posts.children) {
			for (c of p.children) {
				if (c.tagName == 'A') {
					c.style.color = dark? DARK_TEXT : LIGHT_TEXT;
					c.href = c.href.split('?')[0] + document.location.search;
				}
			}
		}
	});
	mapGetElementById('return', x => { 
		x.href = x.href.split('?')[0] + document.location.search;
		x.style.color = dark? '#559' : '#33d';
	});
	mapGetElementById('setting-darkmode', x => { x.style.display = dark? 'none' : '' });
	mapGetElementById('setting-lightmode', x => { x.style.display = dark? '' : 'none' });
	mapGetElementById('menu', x => { x.style.backgroundColor = dark? '#aaaaaa19' : '#bbb5' });
}

window.onload = () => setDarkMode()