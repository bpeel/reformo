Jen la bildoj kaj skriptoj uzataj por krei [ĉi tiun filmeton](https://www.youtube.com/watch?v=9eI54A94j2U) en YouTube.

La enhavo kaj la filmo mem estas havebla laŭ la permesilo [CC-BY](https://creativecommons.org/licenses/by/3.0/legalcode).

La bildoj de la video estas en slides/*.svg. Ĉiu tavolo en ĉiu SVG-dosiero kreas unu folion en la video.

Oni povas rekrei la filmeton per la jena skripto:

```bash
./make-video.sh
```

Por tio oni bezonas ffmpeg, inkscape kaj ImageMagick.

Se oni volas ŝanĝi la tempojn por la bildoj, oni povas uzi la programon maketiming. Ekzemple:

```bash
make
./maketiming > timing.txt
```

Vi povas ŝanĝi la bildon per la spaco-butono kaj ĝi registros la tempojn. Tiuj estos uzataj por rekrei la filmon se vi denove rulas `make-video.sh`.
