"""Screenshot each slide of the rendered deck at given moments (seconds) into its motion.

Usage: python tools/shoot.py _output/index.html shots/ <n_slides> 0.2,1.6,3.6
Set CHROMIUM to a browser binary to skip Playwright's bundled one.
"""
import os, sys, asyncio, pathlib
from playwright.async_api import async_playwright
deck = pathlib.Path(sys.argv[1]).resolve(); out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
slides = int(sys.argv[3]); moments = [float(t) for t in sys.argv[4].split(",")]
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        pg = await b.new_page(viewport={"width":1600,"height":900})
        errs=[]; pg.on("pageerror", lambda e: errs.append(str(e)))
        for i in range(slides):
            await pg.goto(f"file://{deck}#/{i}"); await pg.reload()
            await pg.evaluate("document.fonts.ready"); 
            elapsed=0.0
            for t in moments:
                await pg.wait_for_timeout(int((t-elapsed)*1000)); elapsed=t
                await pg.screenshot(path=str(out/f"s{i+1}-t{t:g}.png"))
        fonts = await pg.evaluate("[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)")
        print("loaded fonts:", sorted(set(fonts))); print("page errors:", errs or "none")
        await b.close()
asyncio.run(main())
