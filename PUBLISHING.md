# 書籍プレビューの生成

このリポジトリの編集上の正本は `manuscript/*.md`。PDF/EPUBは派生物であり、編集のために直接修正しません。

## 必要なツール

- Python 3.10以上
- Pandoc（MarkdownからHTML/EPUB3を生成）
- WeasyPrint 68.0（HTML/CSSからA5判PDFを生成）
- 日本語フォント（Noto Serif CJK JP / Noto Sans CJK JP）

Ubuntu/Debianなら、まず以下で導入できます。

```sh
sudo apt-get install pandoc fonts-noto-cjk
python3 -m pip install -r requirements-build.txt
```

## ビルド

リポジトリのルートで実行してください。

```sh
python3 scripts/build_release.py
```

生成物は `output/` に置かれます。

- `manuscript.md`: 題名ページと巻末の参考資料を含めた**全章の編集用結合原稿**
- `body.md`: 題名ページのMarkdownを除いた組版入力（参考資料を含む、自動生成）
- `oss-book.html`: PDF組版用のHTML
- `oss-book.pdf`: **A5判PDFプレビュー**
- `oss-book.epub`: **EPUB3プレビュー**

表紙のテキストとEPUBメタデータは `book.yaml` から生成します。タイトルのMarkdown（`manuscript/00-title.md`）は保存しますが、組版では二重表紙を避けるため本文から除外します。目次は章タイトルから自動生成されます。巻末の `manuscript/14-references.md` は**読者向け**の出典一覧としてPDF・EPUBに含まれ、`notes/` の内部編集メモは含まれません。

## GitHub Actions

`.github/workflows/build-preview.yml` がPR・mainへのpush・手動実行時にPDF/EPUBを生成し、**ActionsのArtifacts**からダウンロードできるようにします。実行環境が変わるとPDFのページ数や改ページ位置が変わる場合があります。

## この段階での位置付け

これらは**執筆・校正用プレビュー**です。完成版の表紙、奥付、著作者表記、引用確認、頒布条件などは未確定であり、いま生成するPDF/EPUBは完成刊行物とは扱いません。

2026-11-03に旧v0.1原稿を使ったローカル動作試験ではA5判64ページのPDFと正常に展開できるEPUB3を生成できました。これは**v0.2の正式ページ数ではありません**。現行v0.2のプレビューは2026-11-03のGitHub Actionsで**79ページ**と実測され、EPUB3の整合性チェックも通過しました（[実行記録](https://github.com/kawamurashingo/oss-book/actions/runs/41562732832)）。編集後には必ず再計測してください。

2026-11-03の[校正PR #5の自動生成](https://github.com/kawamurashingo/oss-book/actions/runs/41596668775)では、読者向け参考資料を追加したv0.3候補のPDFがA5判**82ページ**となり、EPUB3のZIP整合性も確認できました。これは校正用プレビューであり、最終刊行版のページ数を保証するものではありません。
