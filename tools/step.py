"""Step through one slide's fragments like a presenter and screenshot each state.

Usage: python tools/step.py _output/index.html shots/ <slide-index> <clicks> [settle-seconds]
Each capture is taken `settle` seconds after the click, once that beat's motion
has played. Set CHROMIUM to a browser binary to skip Playwright's bundled one.
"""
import os, sys, asyncio, pathlib
from playwright.async_api import async_playwright

deck = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
slide, clicks = int(sys.argv[3]), int(sys.argv[4])
settle = float(sys.argv[5]) if len(sys.argv) > 5 else 5.0

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROMIUM") or None)
        pg = await b.new_page(viewport={"width": 1600, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto(f"file://{deck}#/{slide}")
        await pg.reload()
        await pg.evaluate("document.fonts.ready")
        await pg.wait_for_timeout(int(settle * 1000))
        await pg.screenshot(path=str(out / f"step-00.png"))
        for i in range(1, clicks + 1):
            await pg.keyboard.press("ArrowRight")
            await pg.wait_for_timeout(int(settle * 1000))
            await pg.screenshot(path=str(out / f"step-{i:02d}.png"))
        state = await pg.evaluate("Reveal.getState()")
        print("final state:", {k: state[k] for k in ("indexh", "indexf")})
        print("page errors:", errs or "none")
        await b.close()

asyncio.run(main())
