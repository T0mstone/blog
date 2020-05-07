const urlParams = new URLSearchParams(window.location.search);

function mapGetElementById(id, map) {
	var x = document.getElementById(id);
	if (x !== null) {
		return map(x);
	}
}

function mapGetElementsByClass(cls, map) {
	var x = document.getElementsByClassName(cls);
	if (x !== null) {
		for (elt of x) {
			map(elt);
		}
	}
}

function setDarkModeFromUrl() {
	let dark = urlParams.get('dark');
	if (dark == '1') {
		setDarkMode(true);
	} else if (dark == '0') {
		setDarkMode(false);
	}
}

function setDarkMode(dark) {
	window.localStorage.setItem('dark', dark.toString());
	applyDarkMode();
}

function applyDarkMode() {
	let dark = {"true": true, "false": false, null: false}[window.localStorage.getItem('dark')];

	const VARS = {
		'background-color': ['#ded', '#101510'],
		'text-color': ['#000', '#993'],
		'special-link-color': ['#33d', '#559'],
		'faint': ['#888', '#555'],
		'menu-bg': ['#bbb5', '#aaaaaa19'],
		'boxed-bg': ['#aaa4', '#aaa2'],
		'boxed-stripe': ['rgba(0, 0, 0, 0.05)', 'rgba(255, 255, 255, 0.1)'],
	};

	let html = document.getElementsByTagName('html')[0];
	for (var key in VARS) {
		console.log(VARS, VARS[key], VARS[key][+dark]);
		html.style.setProperty('--' + key, VARS[key][+dark]);
	}

	mapGetElementById('posts', posts => {
		for (p of posts.children) {
			for (c of p.children) {
				if (c.tagName == 'A') {
					c.href = c.href.split('?')[0] + '?dark=' + (+dark).toString();
				}
			}
		}
	});
	mapGetElementsByClass('return', x => { 
		x.href = x.href.split('?')[0] + '?dark=' + (+dark).toString();
	});
	mapGetElementById('setting-darkmode', x => { x.style.display = dark? 'none' : '' });
	mapGetElementById('setting-lightmode', x => { x.style.display = dark? '' : 'none' });
}

window.addEventListener('load', () => {
	setDarkModeFromUrl();
	applyDarkMode();
});