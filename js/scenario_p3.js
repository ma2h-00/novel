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
      { t: 'd', n: '雨宮蓮', v: 'お、また来たね。\n……今日は、ちょっと面白いものを見せようか。' },
      { t: 'd', n: '雨宮蓮', v: '社内ストレージの旧領域に、誰かが意図的に隠したフォルダがある。\nアクセス履歴を消した跡まで、わざわざ残してくれてた。素人仕事だ。' },
      { t: 'ev', v: 'ev_backup_folder' },
      { t: 'if', trustGE: { who: 'amamiya', v: 1 }, then: 'ch4_recording' },
      { t: 'goto', v: 'ch4_no_recording' },
    ],
  },

  ch4_no_recording: {
    events: [
      { t: 'd', n: '雨宮蓮', v: '中身までは、まだ渡せない。\n……君が本気か、もう少し見させてくれ。' },
      { t: 'goto', v: 'ch4_attack' },
    ],
  },

  ch4_recording: {
    events: [
      { t: 'd', n: '雨宮蓮', v: '中に、録音があった。\n……ノクス社の会議室で録られたやつだ。\n君のために復元した。聴く?' },
      { t: 'wait', v: 600 },
      { t: 'sfx', v: 'paper' },
      { t: 'd', n: '瀬川真理（録音）', v: '遠野葵の作品については、\n個人ではなく、ブランドの資産として処理してください。\n……名前は、出さない方向で。' },
      { t: 'd', n: '佐伯美澄', v: '……これだ。\nこれで、瀬川さんは決定的に動けなくなる。' },
      { t: 'ev', v: 'ev_aoi_recording' },
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
      { t: 'n', v: '一命は取り留めたが、意識は戻らない。\n――事件は、過去の復讐だけじゃない。\n現在進行形で、誰かが「証拠」そのものを消そうとしている。' },
      { t: 'goto', v: 'ch4_shiraishi' },
    ],
  },

  ch4_shiraishi: {
    events: [
      { t: 'bg', v: 'bg-cafe' },
      { t: 'bgm', v: 'sad' },
      { t: 'n', v: '外注イラストレーター、白石エリカ。\n葵と個人的に親しかった、唯一の人物。' },
      { t: 'd', n: '白石エリカ', v: '会社の人? 信用しないって決めてるんで。\n……でも、あなたは、ちょっと違うのかな。\nそう思わせるだけ、見させて。' },
      { t: 'choice', prompt: '何を伝える？', options: [
        { text: '「葵さんの名前を、世に出します」と約束する',
          trust: { shiraishi: 2 },
          goto: 'ch4_shiraishi_open' },
        { text: '「会社のことは私が処理します」と説得する',
          trust: { shiraishi: -1 },
          set: { obey6: true },
          goto: 'ch4_shiraishi_close' },
      ] },
    ],
  },

  ch4_shiraishi_open: {
    events: [
      { t: 'd', n: '白石エリカ', v: '……分かった。\n葵が私に預けてた、未公開のポートフォリオ。あれを見せる。' },
      { t: 'sfx', v: 'paper' },
      { t: 'n', v: '差し出された一冊。\n表紙には、葵の名前で「私のデザインを、私の名前で残したい」とだけ書かれていた。' },
      { t: 'ev', v: 'ev_aoi_portfolio' },
      { t: 'ev', v: 'ev_aoi_memo_dignity' },
      { t: 'goto', v: 'ch5_intro' },
    ],
  },

  ch4_shiraishi_close: {
    events: [
      { t: 'd', n: '白石エリカ', v: '……ああ、そう。\n会社の中では普通でも、外から見たら、それは搾取ですよ。' },
      { t: 'd', n: '白石エリカ', v: 'それに気づかないから、あなたたちは人を壊すんです。' },
      { t: 'n', v: '白石は、ポートフォリオを見せなかった。' },
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
      { t: 'd', n: '佐伯美澄', v: '校了前の最終チェックと同じ。\n小さな違和感を、ひとつずつ、潰していく。' },
      { t: 'goto', v: 'ch5_q1' },
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
          { text: '瀬川真理（クライアント側からの圧力）',
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
        correctGoto: 'ch5_close',
        wrongGoto: 'ch5_close',
      },
    ],
  },

  ch5_close: {
    events: [
      { t: 'd', n: '佐伯美澄', v: '事件には、二つの軸があった。' },
      { t: 'd', n: '佐伯美澄', v: '一つ目は、三年前の葵への裏切りに対する、復讐殺人。\n二つ目は、新ブランド案件と過去の責任を守るための、企業ぐるみの証拠隠滅。' },
      { t: 'd', n: '佐伯美澄', v: '殺したのは、隠したのと、別の人だ。' },
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
