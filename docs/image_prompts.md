# 画像生成プロンプト集

「レイアウト・オブ・デス ― 白紙の校了日」用 16 点の AI 画像生成プロンプトです。

---

## 0. 大原則（全画像に適用）

### 画像仕様

| 項目 | 値 |
|---|---|
| 解像度 | 1920 × 1080（16:9） |
| 用途 | サウンドノベル背景 |
| 文字スペース | 画面下部 30 % は暗化／低情報量に |

### シルエット仕様

- **すべての人物は半透過のシルエットのみ**（顔・肌・髪のディテールなし）
- **男性 = 半透過の青系**（navy / cool blue, 約 65–75 % 不透明）
- **女性 = 半透過の赤系**（crimson / wine red, 約 65–75 % 不透明）
- 背景がうっすら透けて見える程度の透過率
- 輪郭はわずかにぼけたソフトエッジ
- 影はキャラの足元に薄く落とす

### 共通ネガティブプロンプト

すべてのプロンプトに、ネガティブとして以下を必ず指定してください：

```
photorealistic faces, anime characters, visible facial features, eyes,
skin texture, hair detail strands, manga style, cartoon characters,
realistic people, portrait painting of people, text, captions, watermark,
signature, logo, ui elements, japanese text, english text, letters,
characters, words, blurry low quality, jpeg artifacts, distorted anatomy,
extra limbs, opaque solid black silhouettes
```

### 共通ポジティブ・スタイル ブロック

各シーンプロンプトの末尾に、必ず次のブロックを足してください：

```
cinematic atmospheric Japanese sound novel background art, painterly,
soft focus, subtle film grain, restrained color palette, lower third
visibly darker for text overlay, flat translucent silhouette characters
only with no facial features, men rendered as semi-transparent navy
blue silhouettes ~70% opacity, women rendered as semi-transparent
crimson red silhouettes ~70% opacity, background visible faintly
through silhouette bodies, soft outline, no anime, no manga, no realism,
16:9 aspect ratio, 1920x1080
```

---

## 1. キャラクター・シルエット辞典

各キャラを **同じフレーズ**で書くことが一貫性の最重要ポイントです。プロンプト内で必ず固有のキーワード（"Misumi-shape"のような）を使い、同じシーンで複数のキャラが居る場合はそれぞれを区別します。

### 女性キャラ（赤系シルエット）

| 名前 | 識別キー | 描写 |
|---|---|---|
| 佐伯 美澄（主人公・25歳） | `Misumi-shape` | translucent crimson silhouette, slim young woman, **shoulder-length straight hair**, loose blouse and slim pants, slightly cautious posture, often holding a tablet or thin portfolio |
| 篠原 千尋（先輩・29歳） | `Shinohara-shape` | translucent crimson silhouette, average-height woman, **short bob hair**, layered cardigan over loose shirt with straight pants, composed straight posture, hands often folded near waist |
| 三枝 透子（取締役・41歳） | `Mitsue-shape` | translucent crimson silhouette, tall woman, **hair tied up in a chignon**, sharp tailored blazer + pencil skirt, very upright authoritative posture |
| 瀬川 真理（黒幕・33歳） | `Segawa-shape` | translucent crimson silhouette, slim woman, **tight low ponytail**, fitted power suit jacket and pencil skirt, heels, arms crossed, chin slightly raised |
| 白河 エリカ（外注絵師・31歳） | `Shirakawa-shape` | translucent crimson silhouette, average build woman, **loose messy ponytail**, oversized denim jacket over tee and jeans, slouchy artistic stance, hands in pockets |

### 男性キャラ（青系シルエット）

| 名前 | 識別キー | 描写 |
|---|---|---|
| 久我 玲司（CD・38歳） | `Kuga-shape` | translucent navy silhouette, tall lean man, **short cropped hair**, slim dark turtleneck under fitted jacket, no tie, confident standing posture, one hand often in pocket |
| 梶原 誠（営業部長・45歳） | `Kajihara-shape` | translucent navy silhouette, **stocky middle-aged man**, slightly receding hairline, traditional business suit with tie, briefcase or bulging document folder visible |
| 雨宮 蓮（エンジニア・27歳） | `Amamiya-shape` | translucent navy silhouette, slim young man, **messy mid-length hair**, oversized hoodie over t-shirt with jeans, slight slouch, hands in hoodie pocket, often headphones around neck |
| 立花 祐介（クライアント担当・36歳） | `Tachibana-shape` | translucent navy silhouette, average build man, neatly combed short hair, **standard business suit with tie**, ID badge lanyard around neck, polite tense posture, often holding clipboard |
| 黒瀬 直人（コピーライター・34歳） | `Kurose-shape` | translucent navy silhouette, lean man, **longer side-parted hair**, leather jacket over open-collar shirt, casual cynical lean, often a tumbler glass in hand |

### 故人・回想のみ

| 名前 | 描写 |
|---|---|
| 遠野 葵（直接登場しない） | 直接描かない。葵を示す場合は **小さなラフスケッチ／写真パネル／後ろ姿の輪郭のみ** |

---

## 2. 一貫性を高めるコツ

1. **最初に「キャラ単体」のレファレンス画像を 1 枚ずつ作る**  
   各キャラの記述を使って、白背景で正面・後ろ姿の単体画像を生成し、参照画像（Midjourney `--cref` / SD 系の i2i / DALL-E 連続会話）として保持する。

2. **同じシーンに同じキャラを描き直すときは、同じフレーズをそのまま貼る**  
   例：常に `Misumi-shape: translucent crimson silhouette of slim young woman with shoulder-length straight hair, loose blouse and slim pants` を一字一句変えない。

3. **複数人を描くときは「左から順に列挙」**  
   `From left to right: Tachibana-shape (navy male, suit with tie, lanyard), Segawa-shape (crimson female, ponytail, power suit), Misumi-shape (crimson female, shoulder-length hair, loose blouse)`

4. **半透過は「opacity 65-75%」「background visible through body」と数値・現象の双方で書く**

5. **顔は禁止語で確実に潰す**：`no faces, no facial features, faceless silhouettes`

---

## 3. シーン別プロンプト

各セクションには、**Setting／Characters／Prompt（コピペ用）／Notes** を記載しています。Prompt の末尾に「共通ポジティブ・スタイル ブロック」（§0）を必ず連結してください。

---

### #1 — `title.jpg` （タイトル画面）

**Setting**: 暗い部屋。中央上部に薄い暗赤の光。床に散らばる校正紙、赤入れの跡。  
**Characters**: なし

**Prompt**:
```
A dark moody title-screen background. Pitch-black space with a single
soft crimson red glow softly illuminating the upper center, like blood
seeping through paper. Across the lower half of the frame, dozens of
scattered overlapping torn proofread papers with faint horizontal ruled
lines and occasional red ink correction marks. The papers are slightly
crumpled, photographed from a steep top-down-ish angle, partially in
shadow. The center of the frame is left empty for a title. Very desaturated,
almost monochrome except for the red glow and a few red marker strokes.
Heavy vignette. Subtle film grain.
```

**Notes**: 文字を載せる中央に余白を残す。中央〜下部は暗化。

---

### #2 — `office_day.jpg` （日常のオフィス）

**Setting**: 中堅デザイン制作会社のフロア、午後。暖色光。窓は描かない。  
**Characters**: 主人公（手前デスク・後ろ姿）、遠景に同僚 1 人

**Prompt**:
```
A creative design agency office in late afternoon, warm beige and amber
tones, slightly desaturated. Rows of identical desks recede into shallow
depth. On each desk a dark monitor with a subtle blue screen glow.
Cubicle dividers, scattered Pantone books and proofread sheets, a couple
of takeout coffee cups. Soft warm ceiling lighting from above.

Foreground center-left, behind a foreground desk:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a slim
young woman with shoulder-length straight hair, loose blouse and slim
pants, seen from behind, slightly hunched over a glowing monitor. Her
back and head are visible above the desk, her body softly lit by the
monitor. The background shows faintly through her body.

Middle distance, far right, seated at a back desk:
A small distant Tachibana-shape or generic male colleague — translucent
navy blue silhouette ~70% opacity, only head and shoulders visible above
the back desk row.

Composition: low-mid camera angle, lots of headroom. Lower 30% darker
for text overlay.
```

---

### #3 — `meeting_room.jpg` （NOX案件の説明）

**Setting**: 会議室。プロジェクタの薄明かり、長机、ホワイトボード。  
**Characters**: 立って説明する久我（中央奥）、長机の手前側に座る数人（梶原、篠原、美澄）

**Prompt**:
```
A dim corporate meeting room lit only by a projector beam from behind
the camera. Long dark conference table running diagonally toward the
back. Whiteboard at the back wall faintly lit. The table surface
catches a soft warm projector reflection.

Standing at the back of the table, presenting toward camera:
Kuga-shape — translucent navy blue silhouette ~70% opacity, tall lean
man with short cropped hair, slim dark turtleneck under fitted jacket,
one hand resting on the table edge, the other gesturing to the screen
behind. Confident composed posture.

Seated around the table, from left to right (head and shoulders visible
above the table line, the rest hidden by the table):
- Kajihara-shape — translucent navy silhouette of a stocky middle-aged
  man, slightly receding hair, suit and tie, leaning back arms crossed.
- Shinohara-shape — translucent crimson silhouette of a woman with
  short bob hair, cardigan layered look, hands folded on the table.
- Misumi-shape — translucent crimson silhouette of a slim young woman
  with shoulder-length straight hair, loose blouse, slightly leaning
  forward taking notes.
- One generic navy male silhouette as additional staff.

The silhouettes are translucent so the table edge and projector light
behind them shows faintly through their bodies. No facial features at
all. Lower third darker for text.
```

---

### #4 — `office_night.jpg` （深夜の社内・主人公独り）

**Setting**: 深夜のオフィス、雨の窓、青いモニタ光。  
**Characters**: 美澄ひとり

**Prompt**:
```
A deserted nighttime office floor, deep navy and cool teal palette.
Rows of dark desks with a few monitors still glowing cold cyan-blue.
A row of windows in the upper background shows faint streaks of rain
against the city night, with distant scattered building lights diffused
through the wet glass. Most of the room is in shadow. A slightly green
emergency exit sign glows faintly far down the aisle.

In the foreground at one of the desks, seen from slightly behind and
to the side:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, seated alone, facing the monitor. Her back and head softly
lit by the cold monitor glow. The empty desks of her absent colleagues
recede behind her. The background visibly shows through her translucent
body.

Composition: a quiet, lonely, almost sacred mood. The whole image
should feel still. Heavy atmospheric grain, deep vignette. Lower 30%
darker for text overlay.
```

---

### #5 — `meeting_crime.jpg` （第一の殺人現場）

**Setting**: 深夜の会議室、机に伏した梶原、散らばった書類、机に書かれた赤字メッセージ。  
**Characters**: 梶原（伏した姿）

**Prompt**:
```
A nighttime meeting room crime scene, deeply oxblood-red and pitch-black
palette. The only light is a weak overhead lamp directly above the long
table, casting a dramatic pool of warm light onto the table surface and
fading into total black at the edges. The walls are not visible.

Slumped face-down across the table, partially center-left:
Kajihara-shape — translucent navy blue silhouette ~70% opacity of a
stocky middle-aged man with slightly receding hair, business suit and
tie, collapsed motionless across the table top, one arm extended, head
turned to the side resting on the wood. Not graphic, no blood — just
silhouette. The background table grain shows faintly through his body.

On the table around him: scattered overlapping printed proofread sheets
with horizontal ruled lines and red correction marks, a tipped-over
ceramic coffee mug with a dark coffee stain spreading across the table,
a few index cards. In the empty space between the papers, written
directly on the table top with a thick fresh red felt-tip marker, in a
hurried scrawl, abstract horizontal red marker strokes that suggest
hand-written Japanese text but are NOT readable letters — pure marker
gesture only, no actual characters.

Heavy vignette, deep shadows on all four edges, strong film grain.
Lower 30% even darker for text. The mood is hushed, finished, terrible.
```

**Notes**: 文字（日本語）は描かせない。AIが「日本語っぽい記号」を勝手に作ると不自然になるので、**赤いマーカーの手書きストロークだけ**を要求する。

---

### #6 — `corridor.jpg` （社内廊下・汎用）

**Setting**: 社内の細長い廊下。グレーグリーンの蛍光灯。一点透視。  
**Characters**: 美澄ひとり（向こうから歩いてくる、または立っている）  
**用途**: ch1_shinohara, ch1_kuga, ch2_archive, ch3_tachibana, ch4_attack 等で使い回し

**Prompt**:
```
A long narrow corporate corridor in cool fluorescent lighting,
desaturated grey-green palette. Strict one-point perspective with
a vanishing point at the center. Walls and ceiling painted off-white,
floor in dark grey carpet tiles. A row of evenly spaced ceiling
fluorescent panel lights recedes into the distance. A single closed
door at the far end. A few unmarked gray office doors on each side.
Slightly oppressive atmosphere, completely empty of decoration.

Mid-distance, slightly off center to the right, walking toward camera:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, walking toward the viewer, holding a slim portfolio at
her side. Her body is small enough that the corridor dominates the
frame; the corridor visibly shows through her translucent body.

Composition: very symmetrical, claustrophobic, lots of negative space
above her. Lower 30% darker for text. Subtle grain, mild vignette.
```

**バリエーションのヒント**: 同じ構図で、人物を以下に差し替えると流用しやすい：

- ch1_kuga 用 → 美澄の代わりに `Kuga-shape` を遠くで対面させる
- ch4_attack 用 → 廊下に `Mitsue-shape` を倒れた状態で配置（暗い赤色がさらに濃く）

---

### #7 — `server_room.jpg` （サーバ室）

**Setting**: 暗いサーバ室。緑の LED が点々と灯る。中央通路。  
**Characters**: 雨宮（中央通路に立つ）、美澄（手前、後ろ姿、対話中）

**Prompt**:
```
A small dim server room. Two parallel walls of black server racks line
the left and right of the frame in dramatic perspective. Rows and rows
of small green and amber LED lights blink softly along the rack faces,
the only light sources besides a faint cool green ambient haze pooling
in the central aisle deep in the back. The floor is dark raised mesh.
Loose cables drape between the racks. A subtle green-teal glow fills
the depth, leaving the foreground in deep shadow.

Standing at the end of the central aisle, facing camera, leaning against
a server rack with one shoulder:
Amamiya-shape — translucent navy blue silhouette ~70% opacity of a
slim young man with messy mid-length hair, oversized hoodie and jeans,
hands in hoodie pocket, headphones around neck, casual relaxed slouch.
The green LED light shows faintly through his translucent body.

Foreground left, with her back to the camera, smaller in frame:
Misumi-shape — translucent crimson red silhouette ~70% opacity, slim
young woman with shoulder-length hair, loose blouse, holding a tablet,
just talking, only her back and head visible.

Composition: tight, two-character conversation. Heavy vignette except
for the central green pool. Lower 30% darker for text.
```

---

### #8 — `bar.jpg` （第二章・バー）

**Setting**: 暗いカウンターバー。琥珀色の照明。背景の棚にボトルが並ぶ。  
**Characters**: 黒瀬（カウンター越しに対面）、美澄（手前、後ろ姿）

**Prompt**:
```
An intimate dimly-lit Tokyo back-alley bar at night. Deep amber and
sepia palette. Long polished wooden counter dominating the lower
foreground. Behind the counter, two long wooden shelves with rows of
warm-glass whisky and liquor bottles backlit by a soft amber glow.
A single low pendant lamp casts a small pool of warm light onto the
counter at the center of the frame. Hazy cigarette smoke drifts subtly
in the background. Mood is conspiratorial, slightly sleazy.

Across the counter, facing the camera, only head and shoulders visible
above the counter:
Kurose-shape — translucent navy blue silhouette ~70% opacity of a lean
man with longer side-parted hair, leather jacket over open-collar
shirt, leaning forward on the counter with both arms, holding a tumbler
of whisky in his right hand, casual cynical posture.

In the foreground left, with her back to camera, head and shoulders only:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse,
seated at the counter, listening, her back to the viewer.

On the counter between them: two glasses, an ashtray, a folded napkin.
The bottle wall behind shows faintly through both translucent
silhouettes. Lower 30% darker for text.
```

---

### #9 — `client_office.jpg` （第三章・ノクスビューティー本社）

**Setting**: 高層階のブランドルーム。広い窓の向こうにビル群。冷たい白とネイビー。  
**Characters**: 瀬川（中央、立って腕を組む）、立花（少し下がった位置）、美澄（手前右、後ろ姿）

**Prompt**:
```
A high-floor corporate brand showroom, very cold and pristine. Floor-
to-ceiling windows fill the upper two thirds of the frame, framed in
thin dark steel mullions, looking out over a hazy daytime Tokyo
skyline of distant high-rises in cool grey-blue. Polished pale concrete
floor reflects the windows softly. Minimal furniture: a single
glass conference table at the lower foreground, a tall white display
plinth in the back left. The room has zero warmth.

Standing center of the frame, just in front of the windows, facing
camera:
Segawa-shape — translucent crimson red silhouette ~70% opacity of a
slim woman with tight low ponytail, fitted power suit jacket and pencil
skirt with heels, arms crossed in front of her chest, chin slightly
raised, completely still. Authoritative posture.

Slightly behind her and to her left, half a step back:
Tachibana-shape — translucent navy blue silhouette ~70% opacity of an
average build man with neat short hair, business suit with tie, ID
badge lanyard around neck, hands clasped low in front of him, polite
tense posture.

Foreground right, only head and back visible, facing into the room
(back to camera):
Misumi-shape — translucent crimson silhouette of a slim young woman
with shoulder-length straight hair, loose blouse, slightly smaller in
frame than Segawa.

Composition: the windows dominate, the people are placed against the
bright skyline so their translucent bodies have the city showing
through. Lower 30% darker for text.
```

---

### #10 — `rooftop.jpg` （第三章・屋上の打ち明け）

**Setting**: 雑居ビル屋上、夜。鉄柵、貯水槽。地平線に都市の灯。月。  
**Characters**: 篠原（右、手すりの方を向き、横顔気味）、美澄（左、距離をあけて立つ）

**Prompt**:
```
The rooftop of a nondescript Tokyo office building at night. Deep navy
sky with a small soft white moon high in the upper right corner. Below
the moon, the city skyline stretches across the horizon at the lower
third — countless distant building windows scattered as small warm
yellow squares of light, their glow bleeding faintly into the orange-
red haze just above the horizon line. A waist-high steel safety
railing runs across the foreground. To the left, the dark silhouette
of a rooftop water tank rises like a square pillar. The rooftop floor
is dark grey concrete.

Standing on the right side, leaning forward with both hands on the
railing, facing the city, body slightly turned in profile to camera:
Shinohara-shape — translucent crimson red silhouette ~70% opacity of
a woman with short bob hair, layered cardigan look with straight pants.
Her shoulders are subtly slumped, head turned toward the city, the
posture of someone unburdening a long-held secret. The city lights
behind show faintly through her body.

Standing on the left side, several meters away, facing toward
Shinohara, listening, hands at her sides:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, slightly smaller in frame.

Both women are crimson silhouettes — emphasize that with two
distinguishable hair shapes (bob vs shoulder-length straight) so the
viewer can tell them apart by silhouette alone.

Composition: wide horizontal frame, the city skyline anchoring the
middle, lots of sky above. Quiet, melancholic. Lower 30% darker for
text. Slight wind feeling.
```

**Notes**: 「両方女性 → 両方赤」になるので、**髪の輪郭差**で識別可能なよう明確に書く。

---

### #11 — `cafe.jpg` （第四章・白河との対話）

**Setting**: 個人経営の小さなカフェ。木のテーブル。ペンダントライト。  
**Characters**: 白河（左、横顔気味）、美澄（右、横顔気味）

**Prompt**:
```
A small independent café interior at late afternoon. Warm sepia and
amber palette, very intimate. A single dark wood table dominates the
lower foreground. A round black pendant lamp hangs above the center of
the table casting a small pool of warm light directly on the table
top, fading off into shadow at the corners. Background: a wood-paneled
wall, a window upper-left letting in soft outdoor amber light through
white curtains, a small framed picture on the wall.

Seated on the left side of the table, body turned in 3/4 toward the
camera:
Shirakawa-shape — translucent crimson red silhouette ~70% opacity of
an average build woman with loose messy ponytail, oversized denim
jacket over t-shirt, slouchy artistic stance, leaning back, one arm
on the table.

Seated on the right side of the table, body turned in 3/4 toward the
camera (mirroring Shirakawa but smaller):
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse,
slightly forward-leaning, both hands on the table.

Two crimson female silhouettes facing each other across the table.
Distinguish them clearly by hair shape (loose ponytail vs straight
shoulder-length) and posture (slouchy vs upright).

On the table between them: two ceramic mugs of dark coffee with steam,
a small open sketchbook, a pen.

Composition: warm cocoon-like, lower 30% darker for text. The window
light contrasts gently with the lamp light.
```

---

### #12 — `presentation.jpg` （第六章・最終プレゼン／告発）

**Setting**: 暗くした大会議室。スクリーンに最終キービジュアル。観客席のシルエット。  
**Characters**: 美澄（中央前方、立って告発するポーズ）、観客席に久我・篠原・瀬川・立花・三枝代理・白河

**重要**：これが「告発」シーン。**美澄のポーズが「真犯人を指差す／資料を突きつける」と一目でわかる**ようにする。

**Prompt**:
```
The climactic accusation scene of a mystery sound novel. A large dim
corporate presentation room, the only strong light is a wide cinematic
projector beam from behind the camera onto a giant screen at the back
center of the frame. The screen shows an abstract minimalist key visual:
a large hand-drawn red ellipse over a thin diagonal black line on a
warm cream background — clearly a "brand key visual" but no readable
text. Around the screen: deep velvety blackness, the rest of the room
dissolves into shadow. A faint warm spotlight on the floor lights a
podium center-stage.

Standing at the center podium, body squared to camera, one arm raised
and rigidly extended forward toward the audience pointing with index
finger toward the right side of the audience, the other hand clutching
a thin folder of documents at her side. Head held high. This is an
unmistakable accusatory pose:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, illuminated from behind by the projector glow so her
silhouette is lit on its edges.

Audience seated in the foreground, facing the back (the screen and
Misumi), heads and shoulders only visible in deep shadow against the
projector light. From left to right (in order of seating from camera):
- Kuga-shape (navy male, short cropped hair, slim turtleneck, leaning
  forward intently)
- Shinohara-shape (crimson female, short bob hair, head bowed slightly
  in resignation, hands clasped on lap)
- Tachibana-shape (navy male, neat hair, suit and tie, lanyard, body
  visibly tense)
- Segawa-shape (crimson female, tight ponytail, fitted suit, sitting
  perfectly upright, arms crossed, jaw lifted, refusing to react —
  the one Misumi is pointing toward)
- Shirakawa-shape (crimson female, loose ponytail, oversized jacket,
  sitting at the edge of the row arms folded protectively)

Misumi's pointing finger is unmistakably aimed in the direction of
Segawa's seat. Segawa's posture (upright, chin up, arms crossed)
radiates rejection.

Heavy chiaroscuro: stage area is rim-lit warm, audience silhouettes
are deep shadow, the rest is black. Cinematic dramatic film grain.
Lower 30% darker for text overlay.
```

**Notes**:
- 「告発」を視覚化する核は **腕を伸ばして指差すポーズ＋瀬川の頑なな着席姿勢**。
- 「pointing with index finger toward the audience」「unmistakable accusatory pose」など、**ポーズを最低 2 回は明示**するとブレにくい。

---

### #13 — `ending_a.jpg` （A：校了 ― ギャラリー）

**Setting**: 半年後、小さなギャラリー。葵の作品が並ぶ。朝の柔らかい光。  
**Characters**: 美澄ひとり（後ろ姿、作品の前に立つ）

**Prompt**:
```
A small intimate art gallery at quiet morning. Warm gold and cream
palette, soft natural daylight pouring in from the upper right. A long
gallery wall fills the background, beige off-white plaster. Mounted on
the wall in a row, four identical dark-wood-framed artworks at eye
level. Each frame contains the same minimalist abstract design: a
hand-drawn crimson red ellipse over a thin diagonal black line on a
cream background — the original Aoi key visual, finally credited. Below
each frame, a small museum label card. Polished hardwood floor.

Standing center foreground, with her back to the camera, head slightly
bowed, looking at the artworks:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, alone in the gallery, hands clasped behind her back. The
warm wall behind shows faintly through her body.

Composition: wide quiet symmetrical frame, the artworks elevated
slightly above her head height. Soft mood, melancholic but redemptive.
Lower 30% slightly darker for text overlay. Mild grain.
```

---

### #14 — `ending_b.jpg` （B：差し戻し ― 雨の夜街）

**Setting**: 雨の夜、改名された会社のビル正面。傘をさす美澄、後ろ姿。  
**Characters**: 美澄ひとり（後ろ姿、傘）

**Prompt**:
```
A rainy Tokyo night street in front of a corporate office tower. Cold
slate-gray and deep navy palette. The tall building dominates the
upper two thirds of the frame, its glass windows scattered with cold
white office lights in irregular patterns. At the very top of the
building, a horizontal lit-up signboard with the new company name —
shown only as a horizontal band of indistinct soft glowing white shapes,
not readable text. Heavy diagonal rain streaks across the entire frame.
Wet asphalt sidewalk reflects the lights as elongated streaks. A single
streetlamp pool of cold blue light puddles to the left.

Standing center foreground with her back to the camera, holding a
black umbrella over her head:
Misumi-shape — translucent crimson red silhouette ~70% opacity of a
slim young woman with shoulder-length straight hair, loose blouse and
slim pants, motionless, looking up at the building. The umbrella is
opaque black. The rain falls around her.

Composition: cinematic somber wide shot, dwarfing her against the
tower. Lower 30% darker for text. Strong rain texture, atmospheric
haze, deep vignette. Mood: cold, defeated, unfinished.
```

---

### #15 — `ending_c.jpg` （C：非公開案件 ― 別部署）

**Setting**: 別部署の整然としたオフィス、誰もいない。中央の PC に匿名ファイルの通知。  
**Characters**: なし（無人）

**Prompt**:
```
A late-night empty corporate office of a completely anonymous
department. Cold neutral gray and pale beige palette, almost colorless.
Identical desk cubicles arranged in symmetric rows, perfectly tidy, no
personal items at all. Each desk has the same dark monitor showing the
same generic blue desktop. Cubicle dividers, soft overhead fluorescent
panels casting flat even light. Polished gray floor.

The frame is centered on one specific monitor in the middle of the
front row. On its screen, in the center, a single small white system
notification popup, barely readable — just a thin horizontal band of
text shapes (NOT real letters, just suggestion of a filename) and a
small file icon. The popup is the only point of focus in the otherwise
sterile composition.

Absolutely no people anywhere in the frame. Empty rolling chairs at
each desk, slightly askew. The whole scene feels abandoned, surveilled.

Composition: dead-center symmetric, lower 30% darker for text overlay.
Cool color cast, very subtle grain. Mood: institutional, suppressed,
the silence after defeat.
```

**Notes**: 通知ポップアップは「ファイル名らしき横帯」だけにとどめる。実際の英数字を AI に書かせると `NOX_final_final_really_final.ai` を再現できないため、形だけ示唆。

---

### #16 — `ending_d.jpg` （D：白紙 ― 真っ白な空間）

**Setting**: 何もない真っ白な空間。中空に赤字メッセージのストロークだけが浮く。  
**Characters**: 美澄ひとり（小さく中央下、立ち尽くす）

**Prompt**:
```
A vast featureless almost completely white void, extremely overexposed
soft cream-white. The faintest possible suggestion of a horizon line
crossing the lower third, but otherwise no walls, no floor, no ceiling
— just bone-white space. The whiteness is slightly grainy, like blank
paper at extreme close-up.

Floating in the upper left third of the frame, two horizontal rows of
broken handwritten red felt-tip marker strokes, suggesting two lines
of frantic Japanese handwriting but NOT readable letters — just rapid
abstract crimson red marker dashes hovering as if written on invisible
glass, the same color crimson that the silhouettes use.

In the lower center of the frame, very small in the empty space:
Misumi-shape — translucent crimson red silhouette ~50% opacity (more
faint than other scenes — she is fading) of a slim young woman with
shoulder-length straight hair, loose blouse and slim pants, standing
motionless facing the camera, arms hanging straight at her sides, head
tilted slightly down. She is dwarfed by the white void.

Composition: minimalist, off-center, oppressive emptiness. Almost
entirely white image. Lower 30% slightly darker for text overlay. No
vignette. Faint paper grain. Mood: total dissociation, the everything-
that-was-erased.
```

---

## 4. 制作順の推奨

1. **キャラ・レファレンス画像**（10 体 × 1 枚ずつ、白背景・正面・後ろ姿）  
   各キャラの記述だけを使い、`white plain background, full body, front view AND back view, two figures of the same character side by side` で生成。これを以後の i2i / `--cref` 入力にする。

2. **タイトル**（#1）  
   キャラ不要、最も自由度が高いので最初に作って雰囲気を確定させる。

3. **無人シーン**（#15 ending_c, #4 office_night, #5 meeting_crime）  
   キャラの一貫性問題が小さいので早期に。

4. **2 人シーン**（#7 server, #8 bar, #10 rooftop, #11 cafe, #14 ending_b）  
   キャラ参照を活用しながら生成。

5. **大人数シーン**（#3 meeting_room, #12 presentation）  
   最後に挑戦。AI は大人数の整列が苦手なので、何度かガチャを回す前提。

6. **必要に応じて corridor の差分版**（襲撃／対峙）を作る。

---

## 5. プロンプト適用の注意

- **opacity の数値**は AI ツールによっては読まれないので、`semi-transparent`, `translucent`, `background visible through body`, `ghostly`, `frosted glass effect` のように **言い換えを 2-3 個並べる**と通りやすい。
- **顔禁止**は強めに：positive 側にも `faceless silhouettes, no facial features, no eyes, no mouth, no skin` と書く。
- **構図ロック**：Midjourney なら `--ar 16:9 --style raw`、SDXL なら 1920x1080 (ratio) で固定。
- 1 ショットで完成しなくても、**シルエットだけ別レイヤーで生成 → Photoshop 等で合成**するワークフローが最も安定。

