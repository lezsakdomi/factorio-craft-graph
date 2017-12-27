# factorio-craft-graph
A good graph about crafting recipes

## Download
A lot of builds could be found and is publicly accessible at [CircleCI](https://circleci.com/gh/lezsakdomi/factorio-craft-graph).

The most important releases could be downloaded here, in github. Those are rendered with more care than the automateds.

## Building
Run the following command in the factorio directory:
```
$REPO/generate-dot.py | dot -Tsvg
```
This would output the SVG. You can redirect it's output (`>factoriograph.svg`) or pipe through some other programs (`| bcat -h`).

Otherwise, there is a make script created, so you can run just simply `make` if you don't want to care about nuances.

This document could be outdated, in that case please see `.circleci/config.yml`
