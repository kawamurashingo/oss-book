# 次の作業（v0.3の校正・出版準備）

## マージ済み

- [x] [PR #1](https://github.com/kawamurashingo/oss-book/pull/1)：第2・8・9章の具体化
- [x] [PR #2](https://github.com/kawamurashingo/oss-book/pull/2)：第3・4章の具体化

## 第3回の改稿：PR #3マージ済み

- [x] 第10章：仕事から生まれた技術的配当とOSS体験を結ぶ
- [x] はじめに・プロローグ・第5〜7章・エピローグ：重複を整理し、章の役割を明確化
- [x] `notes/v0.2-structure-review.md` に構成レビューと根拠を記録
- [x] 著者レビュー完了、[PR #3](https://github.com/kawamurashingo/oss-book/pull/3)をmainへ反映

## 校正と出典整理（PR #5、マージ済み）

- [x] 全章を通読し、客観的な事実を公開記録と照合
- [x] 第3章の小見出しと第4章の公告日の表記を修正
- [x] 読者向けの「参考資料」章を追加（PDF/EPUBに含める）
- [x] `notes/proofreading-2026-11-03.md` に照合内容を記録
- [x] `notes/imprint-plan.md` に奥付・頒布条件の未確定項目を整理
- [x] 著者確認後に[PR #5](https://github.com/kawamurashingo/oss-book/pull/5)をmainへマージ
- [x] [GitHub Actions](https://github.com/kawamurashingo/oss-book/actions/runs/41596668775)で追加した参考資料を含むA5判82ページのPDF・EPUBを生成・確認

## 刊行までの残件

- [ ] 職務上の具体例（公開可能な範囲）の加筆。現時点では推測で補わない
- [x] 全章の一次通読と、主な時系列・参照先の公開記録照合
- [ ] 著者自身による最終通読・表現と実体験の確認
- [ ] 第3・4章で記録したAlpine側パッケージ版と修正版の差について別途確認
- [ ] 目次・奥付・著作権表記・ライセンス方針
- [ ] 文章の分量と組版後の実ページ数を再計測し、80ページ目標を再検討
- [x] A5判PDF／EPUBのプレビュービルド手順を用意（PR #4）
- [x] [GitHub Actions](https://github.com/kawamurashingo/oss-book/actions/runs/41562732832)で現行v0.2のPDF／EPUB生成を確認。A5判**79ページ**、EPUB3の整合性チェック合格
- [ ] 頒布用PDF／EPUBの最終確認

## 表紙・奥付の準備（PR #6）

- [x] 表紙案をSVGで用意し、PDF・EPUBで共有できる生成手順を作成
- [x] 書誌・奥付の入力欄を用意（実在しない名前や出版日を入れない）
- [x] 技術書典向けの頒布情報の下書きと公式要件のメモを作成
- [x] PR #6を著者承認後にマージ（表紙デザインの最終決定・校了は別途確認）
- [x] 著者表記 `kawamurashingo` と発行者・サークル名 **知つなぐ舎** を確定
- [x] 初版発行**予定**日・著作権表示を設定（PR #10でmainに反映）
- [ ] 実発行日・頒布価格・利用許諾・サークル参加状況・校了を確認

## 現行A5プレビューの正しいページ数

- [x] PR #6の組版検証で、Pandoc標準CSSとの二重余白を修正
- [x] [GitHub Actions](https://github.com/kawamurashingo/oss-book/actions/runs/41599901837)でPDF・EPUB両方のビルド成功。A5判の実測は**58ページ**
- [ ] 残りの加筆は必要な実体験や資料をもとに検討し、無理な字数合わせはしない

## EPUBの正式検証と頒布可否の検査（PR #7）

- [x] [PR #6](https://github.com/kawamurashingo/oss-book/pull/6) をマージ、表紙・著者名・発行者名をmainへ反映
- [x] W3C公式EPUBCheck 5.4.0のCI実行手順を追加
- [x] 奥付の未確定情報を表示し、`--enforce` ではブロックする検査を追加
- [x] [PR #7のCI](https://github.com/kawamurashingo/oss-book/actions/runs/41602831747)でEPUBCheck 5.4.0を実行：**0 fatal / 0 errors / 0 warnings**
- [x] [PR #10](https://github.com/kawamurashingo/oss-book/pull/10)をマージ、2026年11月21日を発行**予定**日、© 2026 kawamurashingoを著作権表示に設定。実発行は未完了
- [ ] 頒布前に公開名義・引用・校了・価格・ライセンス・見本一致を確認

## 印刷用PDFの奥付レイアウト（PR #11）

- [x] PR #10 のPDF 58ページ目を確認。参考資料の最終段落と奥付が同じページに混在する課題を特定
- [x] 奥付の見出しから強制改ページするCSSを追加（EPUBの独立した奥付章は維持）
- [x] PDF最終ページとEPUB奥付の実テキストが発行予定・著作権表記に一致するか自動検証
- [x] [PR #11のCI](https://github.com/kawamurashingo/oss-book/actions/runs/41608759525)でPDF **59ページ**・奥付の独立ページ・EPUBCheck **0 errors / 0 warnings**を確認。試し読みワークフローも[成功](https://github.com/kawamurashingo/oss-book/actions/runs/41608759546)
- [ ] 最終版の表紙・奥付・本文は著者が校了する

## 技術書典21の参加状況（2026-11-03確認）

- [x] [PR #11](https://github.com/kawamurashingo/oss-book/pull/11) をmainにマージし、奥付独立ページを反映
- [x] 著者から**技術書典21はまだサークル参加登録していない**と確認
- [x] 公式の申込締切 **2026年7月29日 23:59** が過ぎていることを確認
- [ ] 運営へ締切後のオンライン参加・追加募集の可否を問い合わせる（現時点で不明）
- [ ] 参加が不可なら、イベントに依存しない頒布方法か次回開催を決める
- [ ] 発行予定日の11月21日を維持するか、頒布経路に合わせて見直す
- [ ] 価格・本文と表紙の利用許諾・最終校了を決める

注意：2026年11月21日は**暫定的な書籍発行目標日**であり、技術書典21への出展日ではない。`publication_status` は `planned` のまま維持。
