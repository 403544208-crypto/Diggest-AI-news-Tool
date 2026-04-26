---
name: ai-news-digest
description: AI每日情报技能。每天自动抓取Y Combinator/Product Hunt/Hacker News等来源的AI创投+技术动态，推送至飞书。触发词：AI情报 / 每日情报 / 跑情报
metadata:
  {
    "openclaw": {
      "emoji": "📡",
      "requires": {},
      "channels": ["feishu"],
      "cron": "0 9 * * * Asia/Shanghai"
    }
  }
---

# AI每日情报 · SKILL.md

## 触发词
- "AI情报" / "每日情报" / "跑情报" / "生成今日情报"

## 功能
每天收集AI创投+技术动态，发送至飞书。**特别注意：来源推荐和AI应用层动态占比不低于50%。**

## 信源优先级

| 优先级 | 来源 |
|--------|------|
| ⭐⭐⭐ | Y Combinator博客/Launch List/YC Podcast |
| ⭐⭐⭐ | Product Hunt（AI产品区） |
| ⭐⭐⭐ | Hacker News（AI/ML区） |
| ⭐⭐ | TechCrunch（AI创业） |
| ⭐⭐ | Lenny's Newsletter / First Round Review / a16z |
| ⭐⭐ | Stanford HAI / 机器之心 / 量子位 / 36氪 |
| ⭐ | GitHub Trending（AI相关项目） |
| ⭐ | 即刻 / 稀土掘金（国内AI应用社区） |

## 搜索方向（共18-22条，AI应用层+来源≥60%）

### 【AI应用层 · ≥12条，占总条数60%+】

1. **Y Combinator最新孵化的AI项目**（⭐必选，标注"YC"）
2. **Product Hunt当日/本周热门AI产品**（标注"PH"）
3. **GitHub Trending热门AI开源项目**（标注"GH"）
4. AI应用产品融资（种子轮/A轮/B轮）
5. AI Agent/工具调用产品落地进展
6. 国内外AI产品增长案例/用户数据
7. AI应用层技术栈创新（LLM Stack、推理优化等）
8. AI应用层技术栈创新（LLM Stack、推理优化等）
9. AI工具/平台产品更新（标注"工具"）
10. AI应用出海/全球化案例
11. AI+行业垂直应用（医疗/法律/教育/金融等）
12. AI Startup新品发布（标注"新品"）

### 【来源推荐 · ≥1条】
发现1个高质量AI应用层来源（Newsletter/GitHub/社区/公众号），附：
- 名称 + 一句话定位
- 为什么适合做AI产品
- 代表文章链接

### 【其他动态 · 补足至18-22条】
13. 国内大厂模型进展（阿里/字节/百度/智谱/MiniMax等）
14. 国际大模型更新（GPT/Claude/Gemini/Llama）
15. 芯片/基础设施动态
16. 华人AI顶级人才流动
17. AI开源社区重要更新
18. AI安全/对齐/治理新进展
19. 学术顶会重要论文（ NeurIPS/ICML/ICLR/ACL）

## 输出格式

```
🤖 AI每日情报 · [日期]
━━━━━━━━━━━━━━━━━━

🚀 AI应用层（≥60%）
1. 【YC/PH/GH 标题】
   📝 摘要
   🔗 链接：https://...
   🏷️ YC/PH/GH 标签 | 📅 日期

📦 来源推荐
【来源名称】
📍 定位：一句话说明
💡 为什么适合做AI产品
📖 代表文章：标题
🔗 链接：https://...

📬 其他动态
[每条简短]

━━━━━━━━━━━━━━━━━━
（共18-22条，AI应用层+来源≥60%）
来源：YC / PH / HN / TechCrunch / a16z / 机器之心 等
```

## 推送目标条数
- 每期 **20条**（AI应用层≥12条，占比≥60%）
- 严格按此标准执行，不足20条时需说明原因

用 `message` 工具发送至飞书：
- `action: send`
- `channel: feishu`
- `to: 飞书用户open_id（如 ou_xxx）`
- `message: 上述格式的完整内容`

## Cron 定时任务配置

如需设置每日自动推送，创建 Cron 任务：
- **表达式**: `0 9 * * *`
- **时区**: `Asia/Shanghai`
- **Session**: `isolated`
- **Timeout**: `300秒`
- **推送渠道**: 飞书（announce模式）
- **内容**: 本skill的系统提示词

## 依赖
- `batch_web_search` 工具（搜索）
- 飞书 channel（推送）
- nodemailer（可选，如需邮件通知）

## 注意事项
- 每条新闻必须含链接和日期
- YC/PH/GH项目单独标注
- 人才流动条目标注 ⭐
- 总条数严格控制在12-15条
