# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/aniastriani/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/aniastriani/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

The World in One Image — Tuesday 24 November 2026. A newspaper front
page that sums up the day in a single picture. The lead story is the
International Court of Justice finding Myanmar guilty of genocide against
the Rohingya — the first time the court has found a state responsible —
backed by fourteen nations. Around it: NATO vowing to defend space after
reports of a Russian nuclear-armed satellite; a US surveillance drone
helping Mexico capture El Chapo Isidro; the UN chief calling for an AI
safety framework within a year; a magnitude 5.6 earthquake in Nepal near
the Chinese border; and a ninth measles death in Pennsylvania.

`main.py` draws the whole page with the Python standard library only:
a hand-built 5x7 pixel font, small vector pictograms, and a PNG writer
built by hand from `zlib` and `struct`. No network, no clock, no
randomness — every run writes the same bytes.

## Run it

```sh
python3 main.py
```

The picture is written to `/output/entry.png`, or to
`$MAKEFUN_OUTPUT_DIR` when that variable is set.

---

<sub>Entered on [make.fun](https://make.fun/?ref=nr75efcw&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
