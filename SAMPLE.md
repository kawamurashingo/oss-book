# 試し読み用PDFの作成

このPDFは書籍を知ってもらうための**販促用の抜粋**です。技術書典の運営者に提出する「見本誌」や、頒布する完全版とは**別物**です。登録手順や見本誌の提出要件は申込時点の案内で再確認してください。

## 掲載範囲

以下の4セクションを、**正本のMarkdownから全文そのまま**抽出します。

1. はじめに（`01-introduction.md`）
2. プロローグ（`02-prologue.md`）
3. 第1章（`03-chapter-01.md`）
4. 第2章（`04-chapter-02.md`）

表紙は完成版と同じ `output/cover.png` を使用しますが、**「試し読み」**の表示を重ねます。末尾に出版情報を推測で書き足したり、サンプルのために本文を変更したりしません。

## 作り方

```sh
python3 scripts/build_release.py
python3 scripts/build_sample.py
python3 -m unittest discover -s tests -p 'test_sample.py' -v
```

生成物：

- `output/oss-book-sample.pdf`（試し読み用A5判PDF）
- `output/sample-body.md`（抜粋に使用したMarkdown）
- `output/oss-book.pdf`, `output/oss-book.epub`（比較対象の全文プレビュー）

GitHub Actionsの [Build promotional reader sample](.github/workflows/build-sample.yml) がPRやmain更新時に全文と試し読みを同じコミットから作成します。PDFのページ数が**全文より少ない**ことをCIで検証します。

## 公開前の注意

- 現状は**校正用**。このファイルの自動生成はWebでの公開や頒布登録を意味しません。
- 配布前に著者が全文・抜粋・表紙を確認し、見本の範囲が適切か決定してください。
- 書籍の最終校正後に同じコミットから再生成し、販売する本と文章・図が食い違わないことを確認してください。
- 公式の[技術書典オンラインマーケット利用規約](https://techbookfest.org/market-terms-of-use.html)は、書籍と見本の内容の一致を求めています。ただし、本ファイルを運営提出用の正式な「見本誌」とみなしてよいかは、**その時点の登録画面・案内で確認**してください。

## CIでの初回計測（2026-11-03）

[PR #8の試し読みビルド](https://github.com/kawamurashingo/oss-book/actions/runs/41603736701)で、全文がA5判**58ページ**、試し読みが**12ページ**でした。抜粋の原文一致テスト3件が合格しています。表紙・目次・最終ページを画像化し、表示を確認しました。ページ数は原稿や組版の変更で変わります。
