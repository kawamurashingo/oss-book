# 参考資料

本書のリリース日、配布記録、脆弱性、モジュールの引き継ぎについて、公開情報を確認する際に参照した主な資料をまとめた。特に断りのない限り、2026年11月3日までに確認した情報をもとにしている。

公開記録から確認できることと、著者自身が経験したことは、必ずしも同じではない。例えば、Alpine Linuxのパッケージ更新日は公開履歴で確認できるが、著者がその掲載を見つけた日は確定していない。

## JQ-Liteの公開と配布（第1〜3章）

- [JQ-Lite：ソースコードと開発履歴](https://github.com/kawamurashingo/JQ-Lite)
- [CPAN配布アーカイブ：SHINGO](https://www.cpan.org/authors/id/S/SH/SHINGO/) — 初期版0.01の配布記録。2025年3月28日21:14（UTC）は日本時間で3月29日。
- [Alpine Linux：jq-lite パッケージ](https://pkgs.alpinelinux.org/package/edge/community/x86/jq-lite) — 別の配布経路に掲載されていることを確認できる。
- [Alpine aports：2026年8月5日のjq-lite 2.49更新](https://github.com/alpinelinux/aports/commit/8e536614ca3e597c38c9a13606928f4556c7810a) — この更新日は初回採用日を意味しない。

## 脆弱性への対応（第4章）

- [JQ-Lite：危険な正規表現コンパイルの修正コミット](https://github.com/kawamurashingo/JQ-Lite/commit/c461721ae3d5a90d6d94dbb234c1b8dfee5c1769)
- [MetaCPAN：JQ-Lite 2.51の公開記録・変更履歴](https://metacpan.org/release/SHINGO/JQ-Lite-2.51) — 2026年9月11日23:04（UTC）、日本時間では9月12日に公開。
- [CPAN Security Group：CVE-2026-78497の公告](https://www.openwall.com/lists/oss-security/2026/10/18/3) — 2026年10月18日付。影響対象はJQ-Lite 2.51未満。

## CPAN Rescueとモジュールの引き継ぎ（第7〜9章）

- [CPAN Rescue：プロジェクトと活動記録](https://github.com/kawamurashingo/cpan-rescue)
- [Issue #1：Dist::CheckConflictsの未定義VERSIONへの対応](https://github.com/kawamurashingo/cpan-rescue/issues/1) — 上流への提案とテスト記録。
- [Issue #3：Devel::CallCheckerの引き継ぎと0.010の公開](https://github.com/kawamurashingo/cpan-rescue/issues/3) — 2026年9月15日の権限移転と、9月19日の公開。
- [CPAN Rescue：メンテナへの道筋と責任の境界](https://github.com/kawamurashingo/cpan-rescue/blob/main/MAINTAINER_PATH.ja.md)
- [Issue #37：初めて参加する人向けの保守タスク](https://github.com/kawamurashingo/cpan-rescue/issues/37)

## 技術的配当とAI（第10章）

- [「AI時代に必要なのは『リライト』ではなく、暗黙知を形式知へ変換しながら近代化すること」](https://qiita.com/pannakoota/items/ad070f0b1027d536ab66)（Qiita、2026年9月22日）

ここに挙げた資料は、本書に登場する技術的事実をたどるための手がかりである。出典のない内心や会話を、公開記録から推測して補う意図はない。
