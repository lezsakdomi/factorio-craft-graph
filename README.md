# factorio-craft-graph
A good graph about crafting recipes

## Building
Run the following command in the factorio directory:
```
$REPO/generate-dot.py | dot -Tsvg
```
This would output the SVG. You can redirect it's output (`>factoriograph.svg`) or pipe through some other programs (`| bcat -h`).
