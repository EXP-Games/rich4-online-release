"""Render the checked-in design manifest as static, no-JS-required gallery HTML."""
import html
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
START='<!-- UI_GALLERY -->'
END='<!-- /UI_GALLERY -->'

def render():
    manifest=json.loads((DOCS/'images/ui/manifest.json').read_text(encoding='utf-8'))
    assert manifest['kind']=='design-concept' and manifest['implemented'] is False
    assert len(manifest['screens'])==7
    sections=[]
    for group in manifest['screens']:
        assert len(group['devices'])==3
        e=html.escape
        cards=[]
        for device in group['devices']:
            name=device['file']
            assert Path(name).name==name and (DOCS/'images/ui'/name).is_file()
            title=group['title']+' · '+device['label']+' · 设计效果图'
            cards.append(f'<figure class="device-card" data-device="{e(device["id"])}"><a class="preview-link" href="images/ui/{e(name)}" data-title="{e(title)}"><div class="preview-image"><img loading="lazy" decoding="async" src="images/ui/{e(name)}" width="{device["width"]}" height="{device["height"]}" alt="{e(title)}"></div><figcaption><b>{e(device["label"])}</b><span>设计稿 · 点击放大 ↗</span></figcaption></a></figure>')
        note=f'<p class="group-note">{e(group["note"])}</p>' if group['id']=='board' else ''
        sections.append(f'<section id="screen-{e(group["id"])}" class="screen-group" aria-labelledby="title-{e(group["id"])}"><div class="group-heading"><h3 id="title-{e(group["id"])}">{e(group["title"])}</h3><p>{e(group["note"])}</p></div><div class="device-grid">{"".join(cards)}</div>{note}</section>')
    page=DOCS/'index.html'
    text=page.read_text(encoding='utf-8')
    assert text.count(START)==1
    before,rest=text.split(START,1)
    after=rest.split(END,1)[1] if END in rest else rest
    page.write_text(before+START+'\n'+'\n'.join(sections)+'\n'+END+after,encoding='utf-8',newline='\n')
    print('Rendered 7 groups / 21 design previews.')
if __name__=='__main__':
    render()
