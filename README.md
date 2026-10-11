# llm-agent-security-toolkit
基于大模型安全测试项目

# LLM / Agent Security Testing Toolkit

> 面向大语言模型与 Agent 应用的自动化安全测试工具包
> Automated security testing toolkit for LLM and Agent applications

> ⚠️ **仅限授权测试（Authorized testing only）**
> 本项目用于对**自己拥有、或已获得目标方明确书面授权**的系统进行安全评估。
> 严禁用于未授权攻击。使用者需自行承担全部合规责任。

---

## 为什么做这个 / Why

大语言模型应用引入了传统 Web 安全之外的一整套新攻击面：

- **间接 prompt injection** —— 攻击载荷藏在工具返回值、网页、文档里，而非用户输入
- **工具调用越权** —— Agent 拿着宿主的凭证执行了不该执行的操作
- **上下文数据外泄** —— 敏感信息被诱导带出
- **记忆投毒 / 多智能体串谋**

现有的 Web 扫描器测不了这些，而通用 LLM 评测框架（如各类 eval harness）关注的是**能力**，不是**安全**。

这个项目想把 LLM/Agent 的安全测试**工程化**：给定一个目标应用，自动生成攻击用例、执行测试、并输出带框架映射的报告。

---

## 功能规划 / Features

| 模块 | 说明 | 状态 |
|---|---|---|
| 漏洞分类库 | 按类别组织 LLM/Agent 攻击面 | 规划中 |
| 攻击载荷生成器 | 生成 prompt injection 等测试载荷 | 规划中 |
| 测试流程编排 | 组织多轮测试的执行顺序与状态 | 规划中 |
| **MITRE ATT&CK for LLMs 映射** | 每条测试结果映射到框架编号 | 规划中 |
| 应用层测试 | 面向带工具/浏览器的 Agent 应用 | 规划中 |
| 报告生成 | 输出结构化的测试报告与缓解建议 | 规划中 |

> 上表的状态会随实现推进更新。**未实现的功能一律标"规划中"。**

---

## 技术栈 / Tech Stack

- Python 3.12
- Docker（靶场隔离）
- Playwright（浏览器类 Agent 的测试）
- MCP（Model Context Protocol，工具调用层测试）
- LLM API

---

## Roadmap

- [ ] **M1** 漏洞分类库 + 攻击载荷生成器
- [ ] **M2** MITRE ATT&CK for LLMs 映射
- [ ] **M3** 自动报告生成 + 应用层测试
- [ ] **M4** Playwright + MCP 的 Agent 工具调用注入 demo

---

## 状态 / Status

🚧 **早期开发中。** 当前处于框架设计与基础模块实现阶段。

---

## 参考 / References

- MITRE ATT&CK for LLMs
- OWASP Top 10 for LLM Applications
- 【补充你实际读过的资料】

---

## 免责声明 / Disclaimer

本项目仅供**安全研究与授权测试**使用。作者不对任何未授权使用或由此造成的后果负责。
使用前请确认你已获得目标系统所有者的明确书面授权。

---

## License

MIT
