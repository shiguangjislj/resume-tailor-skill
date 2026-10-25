# resume-tailor-skill

根据互联网岗位要求，从零撰写、改写或优化秋招/实习简历的Skill。侧重产品、AI产品、运营与增长等方向，通过每轮不超过3个问题挖掘真实经历，同时留下完整素材库和适配岗位的简历。

它保存可复用的方法；个人事实与偏好保存在本机。它不会自动获知过去聊天，也不保证通过筛选。

## 使用方式

安装后提供目标岗位JD（如有）和现有简历/本地素材路径。Skill只补缺失的选择：没给JD、也没说明是否有目标JD时询问；已有JD但没说研究范围时询问只按该JD适配，还是补充同类岗位调查。你已说明的选择不会反复确认。常见请求：

> 使用$resume-tailor，帮我从零写一份产品经理实习简历。我还没有JD，先根据目标方向挖掘经历并建立素材库，每轮最多问3个问题。

> 使用$resume-tailor，沿用我的本地素材与偏好，只按这份AI产品经理JD适配。只修改最近一段实习，最多四段；先给可用稿，只问影响写法的关键缺口。

> 使用$resume-tailor，把同一份经历改成产品运营方向。保留事实，重新选择重点，不把每个补充细节写进简历。

> 使用$resume-tailor，先访谈这段项目，只问问题，不改写；关注我没有写出来的判断、协同与落地工作。

> 使用$resume-tailor，只精简这四段到450字以内，不新增事实、不改变责任边界。

每次完成实质性撰写或改写，交付两份资料：完整经历素材库保留事实、证据、责任边界与纠正历史；投递简历只保留本次目标岗位需要的内容。附1—3个由简历正文引出的准备问题和核实重点。它不做模拟面试或通用面试训练。

在支持技能选择器的应用中也可直接选择“岗位适配简历”。具体显示方式取决于宿主；不支持原生写作面板的环境会提供其他可用格式。

## 安装到Codex

本仓库中的技能目录是`skills/resume-tailor`。可使用宿主的skill-installer，从本仓库该目录安装；也可把整个目录复制到宿主支持的用户技能目录。

当前官方文档列出`~/.agents/skills`作为Codex用户级目录。下面命令在仓库根目录运行，不覆盖已有同名技能：

```sh
mkdir -p "$HOME/.agents/skills"
if [ ! -e "$HOME/.agents/skills/resume-tailor" ]; then
  cp -R skills/resume-tailor "$HOME/.agents/skills/resume-tailor"
else
  printf '%s\n' '已有同名技能，请先比较内容再更新。'
fi
```

安装后可明确调用`$resume-tailor`；如果宿主未识别，刷新技能列表或重启后再检查。不会因上传GitHub自动安装到其他人的环境。

## 少重复沟通的关键

首次使用时，可要求将已经确认的经历与偏好保存到本机。优先读取用户指定位置，其次工作区`.resume-tailor/context.md`，再查看`${CODEX_HOME:-$HOME/.codex}/resume-tailor/context.md`。文件模板在[这里](skills/resume-tailor/references/context-template.md)。

素材库保留完整细节、来源、未确认项与修改历史；岗位简历另存具体版本，并关联入选事实。切换电脑或账号时需要自己迁移或重新提供素材，Skill不会上传或同步个人数据。

## 文件与职责

- [SKILL.md](skills/resume-tailor/SKILL.md)：触发范围、工作原则、输出与自查。
- [操作指南](skills/resume-tailor/references/workflow.md)：岗位研究、访谈、选材、压缩与增量修改。
- [经历框架与来源](skills/resume-tailor/references/frameworks.md)：PAR、STAR的权威来源、适用阶段与边界。
- [证据与表达规则](skills/resume-tailor/references/evidence.md)：量化、归因、术语与AI岗位易错点。
- [方法改进说明](docs/methodology.md)：为什么做这些设计，代价和适用条件。
- [发布前检查](docs/pre-release-review.md)：验证结果与待完成事项。
- [行为评估用例](evals/cases.md)：虚构案例及判定标准，不含真实履历。

## 可选机械检查

只输入一段经历的正文，每个模块以空行分开，不包含公司名和日期。检查只读文件，不改写内容，不访问网络。

```sh
python3 skills/resume-tailor/scripts/check_resume.py experience.txt --max-paragraphs 4 --max-chars 500
python3 -m unittest discover -s tests -v
```

脚本检查段数、可见字符数和中文/英文/数字间多余空格，包括常见加粗边界。它不判断事实真假、岗位匹配、因果关系或PDF视觉布局。复杂Markdown/HTML请另做视觉检查。

## 发布范围

GitHub发布的是Skill源码与文档，不等于已进入插件商店。个人素材、简历和真实案例不会随Skill发布。当前未附加开源许可证，后续由仓库所有者选择授权方式。

## 参考

技能发现、目录与安装说明依据[OpenAI官方Build skills文档](https://learn.chatgpt.com/docs/build-skills)，于2026-10-25查阅。技能结构依据[OpenAI技能构建文档](https://developers.openai.com/plugins/build/skills)。经历框架另参考[MIT关于PAR的简历指南](https://capd.mit.edu/resources/resumes-writing-about-your-skills/)及[哈佛职业中心的2026年行业简历建议](https://careerservices.fas.harvard.edu/blog/2026/09/15/resumes-for-industry-grad-student-edition-2026/)。本Skill把这些通用原则用于互联网岗位，是编辑方法，不是经实验证明能提高录用率的模型。
