/* =========================================================
   scenario_p3.js  ―  第四章「未校了データ」
                       第五章「デザインレビュー」
   ========================================================= */

Object.assign(SCENARIO.scenes, {

  /* ============== 第四章 ============== */
  ch4_intro: {
    events: [
      { t: 'bg', v: 'bg-server-room' },
      { t: 'bgm', v: 'mystery' },
      { t: 'chap', v: '第四章\n未校了データ' },
      { t: 'd', n: '雨宮蓮（社内SE）', v: 'お、また来たね。\n……今日は、ちょっと面白いものを見せようか。' },
      { t: 'd', n: '雨宮', v: '社内ストレージの旧領域に、誰かが意図的に隠したフォルダがある。\nアクセス履歴を消した跡まで残ってた。素人仕事だ。' },
      { t: 'ev', v: 'ev_backup_folder' },
      { t: 'if', trustGE: { who: 'amamiya', v: 1 }, then: 'ch4_recording' },
      { t: 'goto', v: 'ch4_no_recording' },
    ],
  },

  ch4_no_recording: {
    events: [
      { t: 'd', n: '雨宮', v: '中身までは、まだ渡せない。\n……君が本気か、もう少し見させてくれ。' },
      { t: 'goto', v: 'ch4_amamiya_logfix' },
    ],
  },

  ch4_recording: {
    events: [
      { t: 'd', n: '雨宮', v: '中に、録音があった。\n……ノクス社の会議室で録られたやつだ。\n君のために復元した。聴くよね？' },
      { t: 'wait', v: 600 },
      { t: 'sfx', v: 'paper' },
      { t: 'd', n: '瀬川真理（録音）', v: '遠野葵の作品については、\n個人ではなく、ブランドの資産として著作権処理してください。\n……名前は、出さない方向で。' },
      { t: 'd', n: '佐伯', v: '……これだ。\n瀬川さんが葵さんの名前を消した決定的な証拠。' },
      { t: 'ev', v: 'ev_aoi_recording' },
      { t: 'goto', v: 'ch4_amamiya_logfix' },
    ],
  },

  ch4_amamiya_logfix: {
    events: [
      { t: 'd', n: '雨宮', v: 'もうひとつ。\n君のアカウントが過去案件フォルダに「アクセスした」って記録、\nあれ、君じゃない誰かが、内側から手で書いた偽装ログだ。' },
      { t: 'd', n: '雨宮', v: '誰でもいいわけじゃない。\n社内システムの管理者権限と、君のID連番を知ってるやつ。\n――管理職か、それに準ずる立場の人間しか、書けない。' },
      { t: 'd', n: '佐伯', v: '私を、第一容疑者にするための工作……。' },
      { t: 'd', n: '雨宮', v: 'あと、事件当夜の通話履歴。\n「梶原 ⇄ 久我」の内線、最後の一本。あれも消されかけてた。\n――復元しといたよ。' },
      { t: 'ev', v: 'ev_kuga_argument' },
      { t: 'goto', v: 'ch4_alibi_trick' },
    ],
  },

  ch4_alibi_trick: {
    events: [
      { t: 'bg', v: 'bg-server-room' },
      { t: 'd', n: '雨宮', v: 'ついでに、もうひとつ。\n篠原さんのアカウント、事件の各時間帯に、ずっと「アクティブ」だった。\n……ように見える。' },
      { t: 'd', n: '雨宮', v: 'でも、操作の間隔が機械的すぎる。\n誰かが、自席のPCを遠隔で叩いて、「在席」を作ってた。' },
      { t: 'd', n: '雨宮', v: 'つまり――篠原さんのアリバイは、ハリボテだ。\n本人は、その時間、社内にいなかった可能性が高い。' },
      { t: 'ev', v: 'ev_alibi_trick' },
      { t: 'd', n: '佐伯', v: 'アリバイを、自分で作ってた。\n……篠原さん。' },
      { t: 'goto', v: 'ch4_kuga_data' },
    ],
  },

  ch4_kuga_data: {
    events: [
      { t: 'bg', v: 'bg-office-night' },
      { t: 'bgm', v: 'tense' },
      { t: 'n', v: '深夜、誰もいないクリエイティブ部のフロア。\n久我玲司の私物ロッカー。鍵は、彼が最近、合鍵を篠原に渡している。' },
      { t: 'd', n: '佐伯', v: '篠原さんに、ロッカーの鍵を貸してもらった。\n――「もう、終わらせて」って、言われた。' },
      { t: 'sfx', v: 'paper' },
      { t: 'n', v: 'ロッカーの一番奥、二重底。\n出てきたのは、葵が三年前に提出した、NOXの初期コンセプト原本一式。' },
      { t: 'n', v: '「遠野 葵」の署名は、すべて黒いマジックで塗り潰されていた。\nその上から、誰のものでもない筆跡で「TRICERA Creative」とだけ書かれている。' },
      { t: 'ev', v: 'ev_kuga_nox_originals' },
      { t: 'd', n: '佐伯', v: '名前を消したのは、書類の段階だった。\n――久我さんが、自分の手で、葵さんの署名を、塗り潰してた。' },
      { t: 'goto', v: 'ch4_mitsue_warning' },
    ],
  },

  ch4_mitsue_warning: {
    events: [
      { t: 'bg', v: 'bg-corridor' },
      { t: 'bgm', v: 'mystery' },
      { t: 'd', n: '三枝', v: '佐伯さん。\n――久我のロッカー、開けましたね。' },
      { t: 'd', n: '佐伯', v: '取締役。\nこれは、私の――' },
      { t: 'd', n: '三枝', v: '責めていません。\nむしろ、よく、ここまで来ました。' },
      { t: 'd', n: '三枝', v: '今夜、私は役員フロアで、最後の決裁書を整理します。\n――三年前、私が決裁印を押した書類の、本物の方を。' },
      { t: 'd', n: '三枝', v: '明日の朝、もし、私が会議に来なかったら。\n机の右下、二重底に、コピーがあります。' },
      { t: 'n', v: '三枝はそれだけ言うと、エレベーターに乗って消えた。\n――それが、彼女が美澄に話した、最後の言葉になった。' },
      { t: 'goto', v: 'ch4_attack' },
    ],
  },

  ch4_attack: {
    events: [
      { t: 'bg', v: 'bg-corridor' },
      { t: 'bgm', v: 'dread' },
      { t: 'wait', v: 500 },
      { t: 'sfx', v: 'shock' },
      { t: 'flash' },
      { t: 'shake' },
      { t: 'n', v: '深夜の役員フロア。\n取締役・三枝透子が、何者かに襲撃された。' },
      { t: 'n', v: '一命は取り留めたが、意識は戻っていない。\n――犯人の目的は、過去の復讐？\nそれとも、証拠の隠滅だろうか？' },
      { t: 'goto', v: 'ch4_mitsue_aftermath' },
    ],
  },

  ch4_mitsue_aftermath: {
    events: [
      { t: 'bg', v: 'bg-office-night' },
      { t: 'bgm', v: 'mystery' },
      { t: 'n', v: '取締役室。\n机の右下――三枝が示していた、二重底。' },
      { t: 'sfx', v: 'paper' },
      { t: 'n', v: '中には、三年前のNOX案件の決裁書のコピーが残されていた。\n発議者の欄は「遠野 葵」のまま。\n承認者の欄に並んでいるのは――久我玲司、瀬川真理、そして、決裁印を押した三枝透子。' },
      { t: 'd', n: '佐伯', v: '三枝さんは、葵さんの名前のまま、決裁を通そうとしていた。\n――それを後から塗り潰したのは、現場の人間。' },
      { t: 'd', n: '佐伯', v: '三枝さんが意識を失えば、書類の真偽を証言できる人間が、また一人減る。\n……そういう順番で、消されている。' },
      { t: 'goto', v: 'ch4_shirakawa' },
    ],
  },

  ch4_shirakawa: {
    events: [
      { t: 'bg', v: 'bg-cafe' },
      { t: 'bgm', v: 'sad' },
      { t: 'n', v: '外注イラストレーター、白河エリカ。\n葵と個人的に親しかった、唯一の人物。' },
      { t: 'd', n: '白河エリカ（イラストレーター）', v: 'トリケラ社の人? 信用しないって決めてるんで。\n……でも、あなたは、ちょっと違うのかな。\nどうなの？' },
      { t: 'choice', prompt: '何を伝える？', options: [
        { text: '「葵さんの名前を、世に出します」と約束する',
          trust: { shirakawa: 2 },
          goto: 'ch4_shirakawa_open' },
        { text: '「会社のことは私が処理します」と説得する',
          trust: { shirakawa: -1 },
          set: { obey6: true },
          goto: 'ch4_shirakawa_close' },
      ] },
    ],
  },

  ch4_shirakawa_open: {
    events: [
      { t: 'd', n: '白河エリカ', v: '……分かった。\n葵が私に預けてた、未公開のポートフォリオ。あれを見せるわ。' },
      { t: 'sfx', v: 'paper' },
      { t: 'n', v: '差し出された一冊。\n表紙には、葵の名前で「私のデザインを、私の名前で残したい」とだけ書かれていた。' },
      { t: 'ev', v: 'ev_aoi_portfolio' },
      { t: 'ev', v: 'ev_aoi_memo_dignity' },
      { t: 'goto', v: 'ch5_intro' },
    ],
  },

  ch4_shirakawa_close: {
    events: [
      { t: 'd', n: '白河エリカ', v: '……ああ、そう。\n会社の中では普通でも、外から見たら、それは搾取ですよ。' },
      { t: 'd', n: '白河エリカ', v: 'それに気づかないから、あなたたちは人を壊すんです。' },
      { t: 'n', v: '白河は、失望した顔で席を立ってしまった。' },
      { t: 'goto', v: 'ch5_intro' },
    ],
  },

  /* ============== 第五章：推理パート ============== */
  ch5_intro: {
    events: [
      { t: 'bg', v: 'bg-office-night' },
      { t: 'bgm', v: 'tense' },
      { t: 'chap', v: '第五章\nデザインレビュー' },
      { t: 'n', v: '集めた資料を、机に並べる。\n赤字、メール、録音、ラフ、手帳。\n――全てが、一枚の絵として読み解かれるのを待っている。' },
      { t: 'd', n: '佐伯', v: '校了前の最終チェックと同じ。\n小さな違和感を、ひとつずつ、潰していく。' },
      { t: 'goto', v: 'ch5_confront_hub' },
    ],
  },

  ch5_confront_hub: {
    events: [
      { t: 'd', n: '佐伯', v: 'プレゼン前の、最後の確認。\n――三人だけ、もう一度、顔を見ておきたい。' },
      { t: 'choice', prompt: '誰から話す？', options: [
        { text: '久我 玲司（直属上司）',     goto: 'ch5_confront_kuga' },
        { text: '雨宮 蓮（社内システム）',   goto: 'ch5_confront_amamiya' },
        { text: '篠原 千尋（先輩デザイナー）', goto: 'ch5_confront_shinohara' },
      ] },
    ],
  },

  ch5_confront_kuga: {
    events: [
      { t: 'bg', v: 'bg-corridor' },
      { t: 'd', n: '佐伯', v: '久我さん。\nロッカーの中身、見ました。' },
      { t: 'd', n: '久我', v: '……。' },
      { t: 'd', n: '久我', v: '俺は、葵を殺してない。\n俺がやったのは、名前を、消したことだけだ。' },
      { t: 'd', n: '久我', v: '梶原さんとは、事件の夜、確かに揉めた。\nあの人は、黒瀬の脅迫に応じる気だった。\n――会社を巻き添えにする気だった。' },
      { t: 'd', n: '久我', v: '俺は止めた。\nそれだけだ。机に伏せた梶原さんを、見てない。' },
      { t: 'goto', v: 'ch5_confront_back' },
    ],
  },

  ch5_confront_amamiya: {
    events: [
      { t: 'bg', v: 'bg-server-room' },
      { t: 'd', n: '雨宮', v: 'さて、最終確認。\n君の質問に、僕が答えられる範囲で答える。一回だけ。' },
      { t: 'd', n: '雨宮', v: '篠原さんのアリバイ偽装、使われたPCは、彼女自身の自席のじゃない。\n――梶原さんの席のPCだ。' },
      { t: 'd', n: '雨宮', v: '梶原さんが死んだ夜、彼の席は「アクティブ」のままだった。\n誰かが、わざとそう見せた。\n……篠原さんの体は、その時間、別の場所にいた。' },
      { t: 'goto', v: 'ch5_confront_back' },
    ],
  },

  ch5_confront_shinohara: {
    events: [
      { t: 'bg', v: 'bg-rooftop' },
      { t: 'bgm', v: 'sad' },
      { t: 'd', n: '篠原', v: '美澄ちゃん。\n……明日、プレゼンだね。' },
      { t: 'd', n: '篠原', v: '私はね、もう、自分のことを、信じてないの。\nだから、美澄ちゃんに、ぜんぶ預けるね。' },
      { t: 'd', n: '篠原', v: '……ひとつだけ、お願い。\n久我さんと瀬川さんを、私と一緒には、絶対に並べないで。' },
      { t: 'd', n: '篠原', v: '彼らは、葵の名前を消しただけ。\n――私は、葵が「消されていく」のを、横で見てた人間だから。\n罪は、別にしてほしいの。' },
      { t: 'goto', v: 'ch5_confront_back' },
    ],
  },

  ch5_confront_back: {
    events: [
      { t: 'choice', prompt: 'もう一人と話す？', options: [
        { text: '久我 玲司',     goto: 'ch5_confront_kuga' },
        { text: '雨宮 蓮',       goto: 'ch5_confront_amamiya' },
        { text: '篠原 千尋',     goto: 'ch5_confront_shinohara' },
        { text: '推理を始める', goto: 'ch5_q1' },
      ] },
    ],
  },

  ch5_q1: {
    events: [
      { t: 'n', v: '梶原の手帳には、事件当日「NOX／赤字確認」とあった。\n――この「赤字」とは、何のことだ？' },
      { t: 'reason',
        prompt: '梶原の言う「赤字」とは？',
        options: [
          { text: '通常のデザイン修正指示',
            evRequired: 'ev_kajihara_message' },
          { text: '営業上の赤字（売上不足）',
            evRequired: 'ev_kajihara_message' },
          { text: '三年前のNOX案件で、改ざんした記録の最終チェック',
            evRequired: 'ev_chatlog_nox',
            correct: true },
        ],
        correctSet: { reason1: true },
        correctGoto: 'ch5_q2',
        wrongGoto: 'ch5_q2',
      },
    ],
  },

  ch5_q2: {
    events: [
      { t: 'n', v: '黒瀬は、誰に何を売ろうとしていた？' },
      { t: 'reason',
        prompt: '黒瀬の脅迫対象は？',
        options: [
          { text: '篠原千尋ひとりに対してだけ',
            evRequired: 'ev_kurose_zip' },
          { text: '梶原・立花・瀬川・久我――関係者ほぼ全員',
            evRequired: 'ev_kurose_zip',
            correct: true },
          { text: '美澄に対して',
            evRequired: 'ev_kurose_zip' },
        ],
        correctSet: { reason2: true },
        correctGoto: 'ch5_q3',
        wrongGoto: 'ch5_q3',
      },
    ],
  },

  ch5_q3: {
    events: [
      { t: 'n', v: '葵を最も追い詰めた、構造的な人物は？' },
      { t: 'reason',
        prompt: '葵の名前を「最初に」消す決定をしたのは？',
        options: [
          { text: '篠原千尋',
            evRequired: 'ev_aoi_recording' },
          { text: '瀬川真理',
            evRequired: 'ev_aoi_recording',
            correct: true },
          { text: '久我玲司',
            evRequired: 'ev_aoi_recording' },
        ],
        correctSet: { reason3: true },
        correctGoto: 'ch5_q4',
        wrongGoto: 'ch5_q4',
      },
    ],
  },

  ch5_q4: {
    events: [
      { t: 'n', v: '事件現場のメッセージ。\n赤字修正のような筆跡。\n――書いた人物は、誰だ？' },
      { t: 'reason',
        prompt: '赤字メッセージを書いた人物は？',
        options: [
          { text: '久我玲司',
            evRequired: 'ev_shinohara_redink' },
          { text: '瀬川真理',
            evRequired: 'ev_shinohara_redink' },
          { text: '篠原千尋',
            evRequired: 'ev_shinohara_redink',
            correct: true },
          { text: '雨宮蓮',
            evRequired: 'ev_shinohara_redink' },
        ],
        correctSet: { reason4: true },
        correctGoto: 'ch5_q5',
        wrongGoto: 'ch5_q5',
      },
    ],
  },

  ch5_q5: {
    events: [
      { t: 'n', v: '梶原は、亡くなる直前、誰かと内線で揉めていた。\n――その相手は？' },
      { t: 'reason',
        prompt: '梶原と最後に通話した社内の相手は？',
        options: [
          { text: '篠原千尋',
            evRequired: 'ev_kuga_argument' },
          { text: '久我玲司',
            evRequired: 'ev_kuga_argument',
            correct: true },
          { text: '雨宮蓮',
            evRequired: 'ev_kuga_argument' },
        ],
        correctSet: { reason5: true },
        correctGoto: 'ch5_q6',
        wrongGoto: 'ch5_q6',
      },
    ],
  },

  ch5_q6: {
    events: [
      { t: 'n', v: '篠原は、事件の各時間帯、社内システム上では「在席」していた。\n――それは、本当か？' },
      { t: 'reason',
        prompt: '篠原のアリバイの正体は？',
        options: [
          { text: '本人が自席で作業していた',
            evRequired: 'ev_alibi_trick' },
          { text: '梶原のPCを使った遠隔操作で、在席を偽装していた',
            evRequired: 'ev_alibi_trick',
            correct: true },
          { text: '雨宮が代わりに操作していた',
            evRequired: 'ev_alibi_trick' },
        ],
        correctSet: { reason6: true },
        correctGoto: 'ch5_q7',
        wrongGoto: 'ch5_q7',
      },
    ],
  },

  ch5_q7: {
    events: [
      { t: 'n', v: '三年前。\n葵の署名が消された、その「物理的な手」は、誰のものだ？' },
      { t: 'reason',
        prompt: '書類上の「遠野葵」の署名を塗り潰したのは？',
        options: [
          { text: '瀬川真理（クライアント）',
            evRequired: 'ev_kuga_nox_originals' },
          { text: '久我玲司（直属上司）',
            evRequired: 'ev_kuga_nox_originals',
            correct: true },
          { text: '篠原千尋（同じ現場）',
            evRequired: 'ev_kuga_nox_originals' },
          { text: '黒瀬直人（外注）',
            evRequired: 'ev_kuga_nox_originals' },
        ],
        correctSet: { reason7: true },
        correctGoto: 'ch5_close',
        wrongGoto: 'ch5_close',
      },
    ],
  },

  ch5_close: {
    events: [
      { t: 'd', n: '佐伯', v: '事件には、二つの軸があった。' },
      { t: 'd', n: '佐伯', v: '一つ目は、三年前の葵への裏切りに対する、復讐殺人。\n二つ目は、新ブランド案件と過去の責任を守るための、企業ぐるみの証拠隠滅。' },
      { t: 'd', n: '佐伯', v: '殺人者は、三年前の隠蔽者とは、別の人だ。' },
      { t: 'goto', v: 'ch6_branch_check' },
    ],
  },

  /* 「会社に従う」を多く選んだ場合は、最終プレゼン前に異動 */
  ch6_branch_check: {
    events: [
      { t: 'if',
        someFlags: ['obey1','obey2','obey3','obey4','obey5','obey6'],
        min: 3,
        then: 'ending_c_path' },
      { t: 'goto', v: 'ch6_intro' },
    ],
  },

  ending_c_path: {
    events: [
      { t: 'bg', v: 'bg-office-day' },
      { t: 'bgm', v: 'sad' },
      { t: 'n', v: '最終プレゼン前日。\n美澄は、辞令を受け取る。\n別部署への、異動。' },
      { t: 'd', n: '三枝透子（代理）', v: 'これは、あなたを守るための判断です。\n……何が「守る」か、いつか、自分で決められるようになりますように。' },
      { t: 'n', v: 'プレゼンの場には、もう美澄の席はなかった。' },
      { t: 'ending', v: 'C' },
    ],
  },

});
