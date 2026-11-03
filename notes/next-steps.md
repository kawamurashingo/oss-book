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
- [ ] 発行日・著作権表示・頒布条件を確定

## 現行A5プレビューの正しいページ数

- [x] PR #6の組版検証で、Pandoc標準CSSとの二重余白を修正
- [x] [GitHub Actions](https://github.com/kawamurashingo/oss-book/actions/runs/41599901837)でPDF・EPUB両方のビルド成功。A5判の実測は**58ページ**
- [ ] 残りの加筆は必要な実体験や資料をもとに検討し、無理な字数合わせはしない

## EPUBの正式検証と頒布可否の検査（PR #7）

- [x] [PR #6](https://github.com/kawamurashingo/oss-book/pull/6) をマージ、表紙・著者名・発行者名をmainへ反映
- [x] W3C公式EPUBCheck 5.4.0のCI実行手順を追加
- [x] 奥付の未確定情報を表示し、`--enforce` ではブロックする検査を追加
- [ ] PR #7のCIで実際のEPUBCheck結果を確認し、必要なら修正
- [ ] 発行日と著作権表示を著者が決定（未確定値は入れない）
- [ ] 頒布前に公開名義・引用・校了・価格・ライセンス・見本一致を確認
