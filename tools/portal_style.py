import sys,re
p=sys.argv[1];h=open(p).read()
css='''<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="/site.css">
<script src="/site.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Tinos&family=Open+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  .staticrypt-body, .staticrypt-body p, .staticrypt-body label, .staticrypt-body footer, .staticrypt-form input, .staticrypt-form button { font-family: 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif !important; }
  .staticrypt-page { width: min(820px, calc(100% - 2.5rem)) !important; }
  .staticrypt-form { background: #fcfaf6 !important; border-radius: 14px !important; box-shadow: 0 2px 14px rgba(29,35,39,0.08) !important; max-width: none !important; box-sizing: border-box; margin-bottom: 32px !important; }
  .staticrypt-form > *, .staticrypt-form form { max-width: 380px; margin-left: auto !important; margin-right: auto !important; }
  .staticrypt-form .staticrypt-instructions { text-align: left; }
  .staticrypt-form .staticrypt-instructions p { margin-left: 0 !important; margin-right: 0 !important; }
  html { font-size: 16px; }
  .staticrypt-body { font-weight: 300; line-height: 1.65; color: #1d2327; }
  .staticrypt-body p.staticrypt-title { font-family: 'Tinos', 'Times New Roman', Times, serif !important; font-size: 1.6rem !important; font-weight: 400 !important; color: #1d2327 !important; line-height: 1.65 !important; margin: 0 0 1.1rem !important; }
  .staticrypt-instructions p:not(.staticrypt-title), .staticrypt-remember, .staticrypt-form input[type=password], .staticrypt-form input[type=text] { font-size: 0.94rem !important; }
  @media (max-width: 640px) { html { font-size: 14.5px; } .staticrypt-form { padding: 1.5rem 1.25rem !important; border-radius: 12px !important; } }
  .staticrypt-instructions { color: #1d2327 !important; font-weight: 300 !important; }
  .staticrypt-hr { border-color: #eee9e0 !important; }
  .staticrypt-password-container { border-radius: 8px !important; background: #f3efe7 !important; overflow: hidden; }
  .staticrypt-decrypt-button { border-radius: 8px !important; text-transform: none !important; font-weight: 600 !important; letter-spacing: 0.02em; }
  .staticrypt-remember { color: #1d2327 !important; font-weight: 300 !important; }
  .sc-foot { text-align: center; color: #5f676b; font-size: 0.85rem; font-weight: 300; padding-bottom: 3rem; }
  .sc-foot a { color: #5f676b; text-decoration: none; }
  .sc-foot a:hover { color: #1f6f78; }
  nav.topnav { position: sticky; top: 0; z-index: 10; background: rgba(228,221,208,0.55); -webkit-backdrop-filter: blur(10px) saturate(1.1); backdrop-filter: blur(10px) saturate(1.1); border-bottom: 1px solid #ebe5da; }
  nav.topnav .nav-inner { max-width: 860px; margin: 0 auto; padding: 0.8rem 1.25rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; box-sizing: border-box; line-height: 1.65; }
  nav.topnav .nav-name { font-family: "Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif; font-weight: 400; font-size: 1.15rem; color: #1d2327; text-decoration: none; }
  nav.topnav .nav-name:hover { text-decoration: underline; text-underline-offset: 2px; }
  .staticrypt-body { margin: 0; }
  .staticrypt-page { padding-top: 6% !important; }
  nav.topnav .nav-links { display: flex; gap: 1.4rem; font-size: 1rem; }
  nav.topnav .nav-links a { color: #5f676b; text-decoration: none; font-family: "Open Sans","Helvetica Neue",Helvetica,Arial,sans-serif; font-weight: 300; }
  nav.topnav .nav-links a:hover { color: #1f6f78; }
  @media (max-width: 640px) { nav.topnav .nav-links { font-size: 0.92rem; } }
  .ficon svg { width: 0.8em; height: 0.8em; margin-right: 0.3em; vertical-align: -0.05em; }
  .ficon { white-space: nowrap; }
  .sc-foot .la-toggle { font: inherit; color: #5f676b; background: none; border: 0; padding: 0; cursor: pointer; white-space: nowrap; }
  .sc-foot .la-toggle:hover, .sc-foot .la-toggle[aria-expanded="true"] { color: #1f6f78; }
  .sc-foot .la-toggle::after { content: ""; display: inline-block; width: 0.38em; height: 0.38em; margin-left: 0.4em; vertical-align: 0.2em; border-right: 1.2px solid currentColor; border-bottom: 1.2px solid currentColor; transform: rotate(45deg); transition: transform 0.25s ease; }
  .sc-foot .la-toggle[aria-expanded="true"]::after { transform: translateY(0.15em) rotate(-135deg); }
  .sc-foot .land-ack { display: none; margin: 1rem 0 0; padding: 0 2.5rem; text-align: left; line-height: 1.55; }
  .sc-foot .land-ack.open { display: block; }
  .sc-foot .land-ack p { margin: 0 0 0.75em; text-align: justify; hyphens: auto; }
  @media (max-width: 640px) { .sc-foot .land-ack { padding: 0 1.25rem; } }
</style>
</head>'''
assert h.count('</head>')==1; h=h.replace('</head>','<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'+css,1)
foot='''                    </form>
                </div>
                <footer class="sc-foot">© 2026 Kevin C. K. Ma<span style="margin:0 0.5em">·</span><button class="la-toggle" type="button" aria-expanded="false" aria-controls="land-ack">Land acknowledgement</button><span style="margin:0 0.5em">·</span><a href="https://kevinckma.github.io/">kevinckma.github.io</a><span style="margin:0 0.5em">·</span><a class="ficon" href="https://kevinckma.github.io/research/" onclick="var i=document.getElementById('staticrypt-password');if(i){i.focus();return false}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 7V5a3.5 3.5 0 0 1 7 0v2" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/></svg>Login</a><div class="land-ack" id="land-ack"><p>I acknowledge that the University of British Columbia, where I currently work, is located on the traditional, ancestral, and unceded territory of the xʷməθkʷəy̓əm (Musqueam) People, and that I live and carry out research on the unceded territories of the Coast Salish Peoples, including the xʷməθkʷəy̓əm (Musqueam), Sḵwx̱wú7mesh (Squamish), and səlilwətaɬ (Tsleil-Waututh) Nations. I recognise their histories and cultures.</p></div><script>(function(){var b=document.querySelector('.sc-foot .la-toggle'),p=document.getElementById('land-ack');if(b)b.addEventListener('click',function(){var o=p.classList.toggle('open');b.setAttribute('aria-expanded',o);if(o)p.scrollIntoView({behavior:'smooth',block:'nearest'});});})();</script></footer>'''
h,n=re.subn(r'                    </form>\n                </div>',foot,h,count=1); assert n==1
h,n=re.subn(r'(<body class="staticrypt-body">\n)',lambda m:m.group(1)+'''<nav class="topnav"><div class="nav-inner"><a class="nav-name" href="https://kevinckma.github.io/">Kevin C. K. Ma</a><div class="nav-links"><a href="#" onclick="var i=document.getElementById('staticrypt-password');if(i){i.focus()}return false">Login</a></div></div></nav>\n''',h,count=1); assert n==1
open(p,'w').write(h)
