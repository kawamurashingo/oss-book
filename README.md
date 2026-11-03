# OSSを作る、OSSに育てられる

**副題：JQ-LiteからCPAN Rescueへ、ひとりの開発者の旅**

技術書典向けのOSS活動体験記。現在は**全章を通した改稿版 v0.2（校正・組版中）**です。

## 原稿

- [章別の原稿](manuscript/)
- [v0.1の全文原稿](archive/v0.1/original-manuscript.md)
- [事実確認メモ](notes/fact-check.md)
- [執筆・編集方針](notes/editorial-guide.md)
- [今後の作業](notes/next-steps.md)
- [読者向け参考資料](manuscript/14-references.md)

Markdown原稿を正本とし、章単位で変更履歴を管理します。

```sh
python3 scripts/build_manuscript.py
```

このコマンドで `output/manuscript.md` に全章を連結できます。

PDF・EPUBのプレビュー生成手順は [PUBLISHING.md](PUBLISHING.md) にあります。GitHub Actionsによる自動生成にも対応しています。

```sh
python3 scripts/build_release.py
```

## 注意事項

ここは**Publicリポジトリ**です。編集中の本文と事実確認メモも公開されます。公開されたことは文章の自由な再利用を許諾することを意味しません。本文のライセンス、引用、著作権表示は頒布前に確認します。

## 状態

- 現行原稿: v0.2（2026年11月、校正中）
- 旧版: v0.1を `archive/v0.1/` に保存
- 目標: A5判 約80ページ（v0.2プレビューの実測は**79ページ**。校正前で変動あり）
- 全10章、はじめに、プロローグ、エピローグ、参考資料
