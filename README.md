# AIKX — Hugo版（GitHub登録用）

Applied Informatics Knowledge Exchange（仮称）の構想紹介サイトです。Jekyll版 `aikx-site-jeklly` の日英本文・共通データ・デザインをHugoへ移植しました。JAIR・JSiSE・IIAIの正式合意前の検討用たたき台です。

## ローカル確認

Hugo **0.147.9**（通常版で可）を用意して、このフォルダで実行します。Ruby・Bundler・外部テーマは不要です。

```sh
hugo server --bind 127.0.0.1 --baseURL http://localhost:1313/
```

ブラウザーで http://localhost:1313/ を開きます。停止は Ctrl+C です。

```sh
hugo --panicOnWarning
python3 scripts/check_site.py public
```

本番URLを指定して生成します。リポジトリ名付きのURLにも対応します。

```sh
hugo --baseURL https://OWNER.github.io/REPOSITORY/ --panicOnWarning
python3 scripts/check_site.py public /REPOSITORY
```

## 構成と編集

- `content/en/`・`content/ja/`：各8ページ。ホームは `_index.md`。
- `hugo.toml`：共通設定、多言語設定、連絡先。
- `data/`：メニュー、3団体、6方針、共通注記。
- `layouts/`：HTML構造、共通部品、ショートコード。
- `static/assets/`：CSSとSVGアイコン。
- `public/`：生成結果（編集対象外、Git管理対象外）。
- `scripts/check_site.py`：生成済みページと内部リンクの検査。Python 3.9以上、追加パッケージ不要。

ルート `/` と `/en/` は同じ英語本文を直接表示し、日本語は `/ja/` です。英語ホームは追加のHTML出力形式で生成するため、本文の二重編集は不要です。通常ページのURLは `/en/mission/`・`/ja/mission/` のようにJekyll版を維持しています。言語切替にはHugoの翻訳ページ情報を使います。

新規ページは同じファイル名・`translationKey` で両言語に作成し、`url` と `data/navigation.yml` を設定します。本文の見出しは `##` から始めます。

内部リンク例：

```text
[理念・目的]({{< siteurl "ja/mission/" >}})
```

共通部品は `{{< organizations >}}`・`{{< principle-summary >}}` で挿入します。ホームの `home-content` ショートコードはMarkdown本文を共通デザインの領域で囲みます。HTMLを含むためGoldmarkの `unsafe = true` を有効にしています。信頼できる編集者のコンテンツを配置してください。

お問い合わせは未受付です。窓口確定後、`hugo.toml` の `params.contact_email` と日英お問い合わせ本文を更新します。設定されるのはメールリンクです。

## GitHub Pages

GitHubに登録するのはこの `aikx` フォルダです。推奨リポジトリ名は `aikx`、公開URLの例は `https://OWNER.github.io/aikx/` です。`aikx-site-hugo` は移植元の保存用コピーです。

1. このフォルダの中身をリポジトリのルートへ配置します。`.github/` も含めます。
2. Settings → Pages → Source を **GitHub Actions** にします。
3. `main` へ反映すると生成・検査・公開が実行されます。手動実行も可能です。

PRでは生成と検査だけを行います。ワークフローがPagesの公開URLをHugoへ渡すため、`hugo.toml` の例示URLを書き換えずに利用できます。別のブランチを使用する場合はワークフローの `main` を変更します。Hugo更新時はREADMEとワークフローのバージョンを合わせ、両URL形式で再検査してください。

## 構想段階の設定

構想案バナー、共通注記、`noindex, nofollow` を維持しています。この指定はアクセス制限ではありません。正式化の際は実際の合意に沿って本文・注記・検索設定を見直してください。独自の論文DB、検索、投稿・問い合わせ受付、会員認証は実装していません。

## 参照

- Hugo多言語設定：https://gohugo.io/content-management/multilingual/
- Hugo出力形式：https://gohugo.io/configuration/output-formats/
- GitHub Pages：https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
