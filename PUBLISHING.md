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

## 表紙・奥付の仕組み（試作）

`assets/cover.svg` が**編集可能な表紙の正本**です。ビルド時にCairoSVGで `output/cover.png` に変換し、同じPNGをA5 PDFの表紙とEPUBのカバーとして使用します。表紙の日本語文字はNoto CJKフォントを使用します。**フォントファイルをリポジトリへコピーしたり再配布したりしないでください。**

`publication/imprint.json` に、正式に確定した著者・発行者・発行日・著作権表示を入力します。未確定の段階では値は空欄のままにします。**必須4項目（author / publisher / publication_date / copyright）が揃うまで、奥付はPDF・EPUBに挿入しません。** `contact` は任意です。

著者名が決まると、表紙とEPUBメタデータにも自動挿入されます。書名や副題を変更する場合は `book.yaml` と `assets/cover.svg` を揃えて更新してください。

これは頒布開始の操作ではありません。値を入力した後も、著者の最終確認・校正・権利処理と実際の技術書典への登録が必要です。

## 版面の修正と正しいページ計測（PR #6）

2026-11-03に表紙付きPDFの視覚確認を行った結果、PandocのHTMLテンプレートに含まれる`body`の50px余白がA5判のページ余白に**二重適用**されていたことが判明しました。`styles/book.css`でテンプレート由来の余白と最大幅を明示的に上書きし、本文サイズ11pt・A5の所定余白で再組版しました。

この修正後、[GitHub Actionsのビルド](https://github.com/kawamurashingo/oss-book/actions/runs/41599901837)で得られた**実測は58ページ**（表紙・目次・本文・参考資料を含む）です。これまでの79/82ページは重複余白による過去の計測値で、現在の正しい版面のページ数として使わないでください。

表紙はPDFの1ページ目にフルページで収まり、EPUBの`content.opf`でも`cover-image`として登録されることを確認しました。内容を増やして80ページに近づけるかどうかは、実体験を加筆する価値がある場合に限って検討します。

## EPUBCheckと正式頒布前のチェック

GitHub ActionsではPDF/EPUBの生成・ZIP整合性確認に加え、W3Cが案内する公式 **EPUBCheck 5.4.0** をダウンロードしてEPUB3の適合性を検証します。これは [EPUBCheck 公式配布](https://github.com/w3c/epubcheck/releases/tag/v5.4.0) を使用しており、第三者製Pythonの同名ツールとは別物です。バージョンを更新する際は検証結果の差を確認してください。

ローカルでの例：

```sh
curl -fL https://github.com/w3c/epubcheck/releases/download/v5.4.0/epubcheck-5.4.0.zip -o epubcheck.zip
unzip epubcheck.zip
java -jar epubcheck-5.4.0/epubcheck.jar output/oss-book.epub
```

奥付の未確定項目は次のコマンドで確認します。

```sh
python3 scripts/check_release_readiness.py
python3 scripts/check_release_readiness.py --enforce
```

通常モードは**校正中の警告のみ**で、ビルドを止めません。`--enforce` は必要な奥付情報が未確定なら終了コード1で停止します。現時点では著者名と発行者名が確定しましたが、発行日と著作権表示は未確定です。

**奥付の項目が揃っただけでは刊行できません。** 著者による校了、内容の権利確認、表紙の確認、販売条件と技術書典登録は別途必要です。GitHub Actionsが成功しても完成版として自動公開しません。

2026-11-03の[PR #7検証ジョブ](https://github.com/kawamurashingo/oss-book/actions/runs/41602831747)では、EPUBCheck 5.4.0が**0 fatals / 0 errors / 0 warnings / 0 infos**と報告し、A5判PDFは58ページでした。奥付は発行日・著作権表示が空欄のため意図どおり未挿入です。最終原稿に変更があれば再検証してください。

奥付の出力判定も、未確定項目の監査と同じ検査関数を使います。空欄だけでなく、`TBD`・`未確定`などの仮文字列も検出して、プレビューに未完成の奥付が入らないようにします。
