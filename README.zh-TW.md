# workingclass

[简体中文](README.md) · [English](README.en.md) · **繁體中文** · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Deutsch](README.de.md)

> 站在勞動者一邊的 AI 工具集。
> AI tools that stand on the side of workers.

這個倉庫收錄服務於勞動者的 agent skills 和工具。第一個，也是核心的，是 **勞動者AI助手 / Laborer's Companion**——一個幫你看穿職場話術、做出對自己最好的決定的工具。

---

## 為什麼存在這個項目

在職場上，公司、HR、老闆都有大量資源來管理你：HR 顧問、操控話術培訓、績效管理系統、法律團隊、招聘心理學顧問。他們說的每一句話都經過精心設計，目的不一定是讓你看清，而是讓你做出對公司最有利的決定。

而你只有你自己。

AI 時代讓這個不對稱更嚴重——公司用 AI 蒸餾你的工作、AI 替代你、AI 監控你。這個項目把 AI 反過來用：**讓 AI 站在你這邊**。

---

## 目前包含

### 1. `skills/laborer-companion/` — 勞動者AI助手

9 個核心模組 + 4 個入口工具，覆蓋職場全景：

| 模組 | 用途 |
|------|------|
| 工具 0a 分診入口 | 不知道該用哪個模組時的路由器 |
| 工具 0b 紅旗掃描 | 60秒判斷你的處境是否危險 |
| 工具 0c 被裁72小時 | 剛被裁的時候做什麼、不做什麼 |
| 工具 0d 隱私與OPSEC | 怎麼安全地使用本工具 |
| 模組1 話術解碼 | 翻譯老闆/HR的話真正在說什麼 |
| 模組2 加班決策 | 真實成本-效益分析 |
| 模組3 績效review解讀 | 看穿review背後的意圖 |
| 模組4 跳槽留任決策 | 基於真實利益做選擇 |
| 模組5 歷史視角 | 從150年勞工運動史中找參考 |
| 模組6 勞動法地圖 | 8個法域條目，覆蓋9個具名法域/地區（不是法律建議）|
| 模組7 薪資談判 | 完整 playbook |
| 模組8 PIP應對 | 從識別預警到談 severance |
| 模組9 找工作和面試 | 求職全生命週期 |

詳細見 [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md)。

---

## 安裝

```bash
# clone 這個倉庫
git clone https://github.com/workingclass-ai/workingclass.git
cd workingclass

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/laborer-companion "${CODEX_HOME:-$HOME/.codex}/skills/"

# Claude Code（如果你使用 legacy Claude skills）
mkdir -p ~/.claude/skills
cp -R skills/laborer-companion ~/.claude/skills/
```

然後在 agent 裡描述你的職場情況，skill 會自動啟動。或者用 slash 命令：

```
/triage      - 不知道用哪個模組時，從這裡開始
/scan        - 60秒紅旗掃描
/decode      - 解碼老闆/HR的話術
/overtime    - 加班決策
/review      - 解讀績效review
/jump        - 跳槽決策
/history     - 歷史視角
/law         - 勞動法查詢
/salary      - 薪資談判
/pip         - PIP應對
/jobsearch   - 找工作和面試
```

---

## 勞動法覆蓋範圍

模組6目前有 **8個法域條目**，覆蓋 **9個具名法域/地區**：

| 法域條目 | 說明 |
|---|---|
| 中國大陸 | 獨立檔案 |
| 香港 / 台灣 | 兩個地區/法域，放在同一個檔案下；回答時不能混用規則，也不能標成國家 |
| 美國 | 聯邦 + 加州/紐約重點 |
| 加拿大 | 聯邦 + 省級差異提示 |
| 澳洲 | Fair Work / Award / unfair dismissal |
| 英國 | UK employment / ACAS / tribunal |
| 歐盟 | 區域總覽，含德國、法國、荷蘭提示；不是27國完整細則 |
| 印度 | 四部 Labour Codes + IT行業常見問題 |

所以如果把香港和台灣分開數，是 **9個法域/地區名稱**；如果按 reference 檔案／法域條目數，是 **8個**。香港和台灣在本項目裡必須標註為 **地區/法域**，不是國家。

---

## 多語言支援

目前支援：

- 簡體中文
- 繁體中文
- English
- Español / Spanish
- Français / French
- Português / Portuguese
- Deutsch / German

預設規則：用戶用什麼語言提問，skill 就用同一語言回答；法律名稱、政府機構、合約條款等會保留官方原文，並在必要時加簡短解釋。繁體中文場景會盡量使用香港/台灣更自然的術語。

---

## 範例與教程

更多完整範例在 [`skills/laborer-companion/README.md`](skills/laborer-companion/README.md)。建議從這些用法開始：

```text
/triage
我感覺經理最近態度不對，但說不清。幫我判斷該用哪個模組。
```

```text
/law
我在香港兼職，每週17小時，HR說香港最低工資只覆蓋部分行業。這個說法對嗎？
```

```text
/review
這是我的績效review：[貼上脫敏後的內容]
我去年是 exceeds，今年是 meets。這是不是危險信號？
```

歡迎貢獻更多教程和真實案例，尤其是：

- 不同國家/地區/法域的勞動法例子
- PIP / 裁員 / severance 談判 walkthrough
- 薪資談判腳本
- 面試反操控示例
- 已脫敏的 HR / manager 郵件樣本
- 西班牙語、法語、葡萄牙語、德語的真實使用示例

---

## 重要原則

1. **不號召集體行動**——這是給單個勞動者的清醒工具
2. **承認現實約束**——不會給"立刻辭職"這種魯莽建議
3. **保持智識誠實**——不會因為"政治正確"而給建議
4. **用戶隱私至上**——見 `skills/laborer-companion/references/privacy-and-opsec.md`
5. **不冒充律師**——提供框架和應該問的問題，不替代專業法律諮詢

---

## 隱私警告 ⚠️

- 這個 skill 不會把你的對話上傳到任何第三方
- 但你和 AI 服務商的對話可能會被平台記錄，取決於帳號和隱私設定
- **不要在公司設備 / 公司網路下使用這個工具**
- **不要把公司機密資料貼給 AI 分析**——脫敏後再用

詳細見 [`skills/laborer-companion/references/privacy-and-opsec.md`](skills/laborer-companion/references/privacy-and-opsec.md)。

---

## 靈感來源

- Koki Xu 的 anti-distillation skill（2026年4月）
- Karl Marx 關於勞動價值與異化理論
- E.P. Thompson 《英國工人階級的形成》
- 過去150年全球工人運動的具體案例
- 當代勞動經濟學和職場社會學

這個工具不創造任何新東西。是把工人階級150年來的集體智慧，翻譯成2026年AI時代可用的形式。

---

## 貢獻

見 [CONTRIBUTING.md](CONTRIBUTING.md)。我們特別歡迎：

- 新的職場話術案例（讓模組1更完整）
- 你所在國家/地區/法域的勞動法補充
- 成功的薪資談判 / severance 談判案例
- PIP 經歷（匿名化後）
- 多語言翻譯

---

## 許可

Apache 2.0 — 見 [LICENSE](LICENSE)。

唯一的請求：**保持工具的核心使命，服務於勞動者**。

---

## 一段話

清醒地看清你的處境，不會讓你的處境改變。但清醒是改變的前提。而且很多時候，清醒地接受現實（包括"我現在還不能離開"），比假裝不清醒地忍受，要好得多。

至少你知道自己在做什麼。
