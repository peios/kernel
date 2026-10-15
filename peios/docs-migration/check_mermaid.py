#!/usr/bin/env python3
"""Render standalone migration Mermaid with Trail's actual bundled renderer."""
import argparse
import json
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('diagrams',type=Path)
    ap.add_argument('--vendor',type=Path,required=True)
    ap.add_argument('--chromium',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=str(args.chromium),headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1600,'height':1200})
        page.set_content('<html><body style="background:white"><main id="diagram"></main></body></html>')
        page.add_script_tag(path=str(args.vendor))
        page.evaluate('mermaid.initialize({startOnLoad:false,securityLevel:"strict",theme:"default"})')
        for i,path in enumerate(sorted(args.diagrams.glob('*.mmd'))):
            result=page.evaluate('''async ({text,id}) => {
              try {
                const {svg} = await mermaid.render('diagram'+id, text);
                document.querySelector('#diagram').innerHTML=svg;
                const root=document.querySelector('#diagram svg');
                return {svg,nodes:root.querySelectorAll('.node').length,edges:root.querySelectorAll('.flowchart-link').length};
              } catch(e) {return {error:String(e)}}
            }''',{'text':path.read_text(),'id':i})
            if 'svg' in result:
                (args.out/(path.stem+'.svg')).write_text(result.pop('svg'))
                page.locator('#diagram').screenshot(path=str(args.out/(path.stem+'.png')))
            result['file']=path.name;results.append(result)
            print(json.dumps(result),flush=True)
        browser.close()
    (args.out/'report.json').write_text(json.dumps(results,indent=2)+'\n')
    if any('error' in r for r in results):raise SystemExit(1)


if __name__=='__main__':main()
