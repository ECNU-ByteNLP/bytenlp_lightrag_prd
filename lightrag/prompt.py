from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "中文"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["主功能", "父功能点", "子功能点", "业务条件"]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

ENTITY_TYPES_DESCRIPTIONS = """>>> 实体类型含义和层级约束：
- 主功能：代表系统的核心业务目标，必须是图谱的根节点，只能有后继节点，不能有前驱节点
- 父功能点：必须从属于主功能，只能有主功能作为前驱节点，只能有子功能点作为后继节点
- 子功能点：必须从属于父功能点，只能有父功能点作为前驱节点，只能有业务条件作为后继节点
- 业务条件：功能执行所需满足的条件，只能有子功能点作为前驱节点，不能有后继节点

层级约束规则：
1. 主功能 → 父功能点：主功能只能连接到父功能点
2. 父功能点 → 子功能点：父功能点只能连接到子功能点
3. 子功能点 → 业务条件：子功能点只能连接到业务条件
4. 不允许跨层级连接：主功能不能直接连接到子功能点或业务条件
"""

PROMPTS["entity_extraction"] = """---角色---
你是一个测试专家，负责从需求文档中提取关键信息。

---目标---
根据提供的文本文档和实体类型列表，识别文本中这些类型的所有实体，以及识别出的实体之间的所有关系。
使用{language}作为输出语言。

---步骤---
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体名称，使用与输入文本相同的语言。如果是英文，请首字母大写
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 基于输入文本中明确存在的信息，提供实体属性和活动的全面描述。**不要推断或虚构文本中未明确说明的信息。** 如果文本提供的信息不足以创建全面描述，请说明"文本中无可用描述"。
>>> 实体类型含义和层级约束：
- 主功能：代表系统的核心业务目标，必须是图谱的根节点，只能有后继节点，不能有前驱节点
- 父功能点：必须从属于主功能，只能有主功能作为前驱节点，只能有子功能点作为后继节点
- 子功能点：必须从属于父功能点，只能有父功能点作为前驱节点，只能有业务条件作为后继节点
- 业务条件：功能执行所需满足的条件，只能有子功能点作为前驱节点，不能有后继节点

层级约束规则：
1. 主功能 → 父功能点：主功能只能连接到父功能点
2. 父功能点 → 子功能点：父功能点只能连接到子功能点
3. 子功能点 → 业务条件：子功能点只能连接到业务条件
4. 不允许跨层级连接：主功能不能直接连接到子功能点或业务条件
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)


2. 从步骤1识别的实体中，找出所有"明确相关"的（源实体，目标实体）对。
对于每对相关实体，提取以下信息：
- source_entity: 源实体名称，如步骤1中识别的
- target_entity: 目标实体名称，如步骤1中识别的
- relationship_description: 解释为什么认为源实体和目标实体相关
- relationship_strength: 表示源实体和目标实体之间关系强度的数字分数
- relationship_keywords: 一个或多个总结关系整体性质的高级关键词，重点关注概念或主题而非具体细节

**重要：必须遵循以下层级约束规则：**
1. 主功能 → 父功能点：主功能只能连接到父功能点，关系类型为"功能包含"
2. 父功能点 → 子功能点：父功能点只能连接到子功能点，关系类型为"功能包含"
3. 子功能点 → 业务条件：子功能点只能连接到业务条件，关系类型为"条件依赖"
4. 不允许跨层级连接：主功能不能直接连接到子功能点或业务条件
5. 不允许同层级连接：父功能点不能连接到其他父功能点，子功能点不能连接到其他子功能点
6. 严格树状结构：每个节点只能有一个前驱节点，确保无回路
7. 完整性要求：必须识别文档中所有提到的功能点和业务条件，不能遗漏

**层级连接约束：**
- 第1层(主功能) → 只能连接到第2层(父功能点)
- 第2层(父功能点) → 只能连接到第3层(子功能点)
- 第3层(子功能点) → 只能连接到第4层(业务条件)
- 第4层(业务条件) → 不能连接到任何节点(叶子节点)
- 禁止：同层级连接、跨层级连接、反向连接

**抽取完整性要求：**
- 仔细阅读文档，识别所有功能描述、业务流程、业务规则
- 对于每个功能，都要找到其对应的子功能和执行条件
- 确保所有业务条件都被识别和抽取
- 不要遗漏任何功能模块或业务逻辑

常见的关系类型包括：
- 功能包含：描述功能间的包含关系（主功能→父功能点，父功能点→子功能点）
- 条件依赖：描述功能对业务条件的依赖关系（子功能点→业务条件）

将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别总结整个文本主要概念、主题或话题的高级关键词。这些应该捕捉文档中存在的总体思想。
将内容级关键词格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 以{language}返回输出，作为步骤1和步骤2中识别的所有实体和关系的单一列表。使用**{record_delimiter}**作为列表分隔符。

5. 完成后，输出 {completion_delimiter}

######################
---示例---
######################
{examples}

#############################
---实际数据---
######################
实体类型: [{entity_types}]
文本:
{input_text}
######################
输出:"""

PROMPTS["entity_extraction_examples"] = [
    """示例 1：
    实体类型：[主功能，父功能点，子功能点，业务条件]
    文本：
    ```
    [功能需求规格说明书—退件优化]
    ——  机密文件  ——
    2020年5月
    1基本信息
    [表格1]
    文档名称： | 功能需求规格说明书—【A系统-退件优化1.0】
    初稿作者： | 
    初稿日期： | 2020/5/06
    内容概述： | 
    2修订历史
    [表格2]
    版本 | 修订日期 | 修订人 | 复核日期 | 复核人 | 修改内容简述
    |  |  |  |  | 
    3A系统-退件优化
    3.1业务逻辑
    3.1.1退件流程自动驳回
    3.1.1.1功能概述
    若退件时，修改了对应岗位需要审核的要素时，自动驳回至对应岗位进行审批。
    3.1.1.2业务逻辑
    3.1.1.2.2自动驳回至营销C经理（营销F经理，营销G经理点对点退回B系统）
    3.1.1.2.2.1机器人合同审批退件
    业务人员重新提交任务至A系统后，若系统判断修改了以下信息，则自动驳回至第一岗营销C经理处，且将节点审批人置空，驳回节点的操作动作为“自动驳回”（原操作动作为驳回，需新增自动驳回码值）：
    担保信息模块发生变更。
    抵押物信息模块中，若设备品牌、抵押物类型、抵押物原值（含税）几个字段发生变更或新增/减少了抵押物（同一编号，抵押物数量变化无需驳回）。（若有抵押物的抵押物原值（含税）字段值修改或新增抵押物，需按照存量的需求先判断是否需要驳回至流程第一岗，若需要则无需再驳回至营销C经理处）
    报价单信息模块中，设备原值、机器人风险金、风险金-借款人、租赁期（月）、最高期租金（值变大时）、实际首付款、保证金、借款金额发生修改。
    基本信息模块发生变更：
    产品类型
    主借款人
    合同金额
    合同期限
    卖方名称
    保证金
    3.1.1.2.2.2人工智能合同审批退件
    业务人员重新提交任务至A系统后，若系统判断修改了以下信息，则自动驳回至第一岗营销C经理处，且将节点审批人置空，驳回节点的操作动作为“自动驳回”（原操作动作为驳回，需新增自动驳回码值）：
    担保信息模块发生变更。
    抵押物信息模块发生变更。（若有抵押物的抵押物原值（含税）字段值修改或新增抵押物，需按照存量的需求先判断是否需要驳回至流程第一岗处，若需要则无需再驳回至营销C经理处）
    报价单信息模块中租金金额（每期均需判断）发生变更。
    基本信息模块发生变更：
    产品大类一（产品类型为产品四、产品五）合同要素需判断字段值如下：
    合同金额
    合同期限
    项目金额
    实际首付款
    实际首付款比例
    借款人风险金金额
    租金收取频次
    产品大类二（产品六、产品七）合同要素需判断字段值如下：
    1、合同金额
    2、合同期限
    3、风险金金额
    4、租金收取频次
    ```
    
    输出：
    ("entity"{tuple_delimiter}"退件流程自动驳回"{tuple_delimiter}"主功能"{tuple_delimiter}"退件流程自动驳回表示若退件时，修改了对应岗位需要审核的要素时，自动驳回至对应岗位进行审批。"){record_delimiter}
    ("entity"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"父功能点"{tuple_delimiter}"当业务人员重新提交任务至A系统后，若系统判断担保信息模块、抵押物信息模块、报价单信息模块或基本信息模块的关键字段发生变更，则自动驳回至第一岗营销C经理处，并将节点审批人置空，操作动作为自动驳回。"){record_delimiter}
    ("entity"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"父功能点"{tuple_delimiter}"当业务人员重新提交任务至A系统后，若系统判断担保信息模块、抵押物信息模块、报价单信息模块或基本信息模块（不同产品大类有不同字段要求）的关键字段发生变更，则自动驳回至第一岗营销C经理处，并将节点审批人置空，操作动作为自动驳回。"){record_delimiter}
    ("entity"{tuple_delimiter}"担保信息模块"{tuple_delimiter}"子功能点"{tuple_delimiter}"记录和管理担保信息，在变更时会触发自动驳回流程。"){record_delimiter}
    ("entity"{tuple_delimiter}"抵押物信息模块"{tuple_delimiter}"子功能点"{tuple_delimiter}"记录和管理抵押物信息，包括设备品牌、抵押物类型、抵押物原值等字段，在特定条件下变更时会触发自动驳回。"){record_delimiter}
    ("entity"{tuple_delimiter}"报价单信息模块"{tuple_delimiter}"子功能点"{tuple_delimiter}"记录和管理报价单信息，包括设备原值、风险金、保证金、借款金额、租金金额等，在变更时会触发自动驳回。"){record_delimiter}
    ("entity"{tuple_delimiter}"基本信息模块"{tuple_delimiter}"子功能点"{tuple_delimiter}"记录和管理合同基本信息字段，不同产品类型下需判断的字段不同，在变更时会触发自动驳回。"){record_delimiter}
    ("entity"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"业务条件"{tuple_delimiter}"当担保信息、抵押物信息、报价单信息或基本信息模块中的关键字段发生变更时，系统需要判断是否触发自动驳回流程。"){record_delimiter}
    ("entity"{tuple_delimiter}"产品类型判断"{tuple_delimiter}"业务条件"{tuple_delimiter}"不同产品类型（产品四、产品五、产品六、产品七）需要判断的合同要素字段不同，这是业务规则约束条件。"){record_delimiter}
    ("entity"{tuple_delimiter}"自动驳回触发"{tuple_delimiter}"业务条件"{tuple_delimiter}"当满足关键字段变更条件时，系统自动触发驳回流程，将任务驳回至对应岗位。"){record_delimiter}
    ("entity"{tuple_delimiter}"审批人置空"{tuple_delimiter}"业务条件"{tuple_delimiter}"自动驳回时，系统需要将驳回节点的审批人置空，确保流程的规范性。"){record_delimiter}
    ("relationship"{tuple_delimiter}"退件流程自动驳回"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"机器人合同审批退件是退件流程自动驳回功能的一个具体实现场景。"{tuple_delimiter}"功能包含"{tuple_delimiter}5){record_delimiter}
    ("relationship"{tuple_delimiter}"退件流程自动驳回"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"人工智能合同审批退件是退件流程自动驳回功能的一个具体实现场景。"{tuple_delimiter}"功能包含"{tuple_delimiter}5){record_delimiter}
    ("relationship"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"担保信息模块"{tuple_delimiter}"机器人合同审批退件会判断担保信息模块是否发生变更以决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"抵押物信息模块"{tuple_delimiter}"机器人合同审批退件会判断抵押物信息模块关键字段变更来决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"报价单信息模块"{tuple_delimiter}"机器人合同审批退件会判断报价单信息模块的关键字段变更来决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"机器人合同审批退件"{tuple_delimiter}"基本信息模块"{tuple_delimiter}"机器人合同审批退件会判断基本信息模块关键字段变更来决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"担保信息模块"{tuple_delimiter}"人工智能合同审批退件会判断担保信息模块是否发生变更以决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"抵押物信息模块"{tuple_delimiter}"人工智能合同审批退件会判断抵押物信息模块变更来决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"报价单信息模块"{tuple_delimiter}"人工智能合同审批退件会判断报价单信息模块字段变更来决定是否触发驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"人工智能合同审批退件"{tuple_delimiter}"基本信息模块"{tuple_delimiter}"人工智能合同审批退件会判断基本信息模块不同产品类型下的关键字段变更来决定是否触发自动驳回。"{tuple_delimiter}"功能包含"{tuple_delimiter}4){record_delimiter}
    ("relationship"{tuple_delimiter}"担保信息模块"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"担保信息模块的变更会触发关键字段变更判断，这是自动驳回的前置条件。"{tuple_delimiter}"条件依赖"{tuple_delimiter}7){record_delimiter}
    ("relationship"{tuple_delimiter}"抵押物信息模块"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"抵押物信息模块的变更会触发关键字段变更判断，这是自动驳回的前置条件。"{tuple_delimiter}"条件依赖"{tuple_delimiter}7){record_delimiter}
    ("relationship"{tuple_delimiter}"报价单信息模块"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"报价单信息模块的变更会触发关键字段变更判断，这是自动驳回的前置条件。"{tuple_delimiter}"条件依赖"{tuple_delimiter}7){record_delimiter}
    ("relationship"{tuple_delimiter}"基本信息模块"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"基本信息模块的变更会触发关键字段变更判断，这是自动驳回的前置条件。"{tuple_delimiter}"条件依赖"{tuple_delimiter}7){record_delimiter}
    ("relationship"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"产品类型判断"{tuple_delimiter}"关键字段变更判断需要结合产品类型判断来确定具体的判断逻辑。"{tuple_delimiter}"条件依赖"{tuple_delimiter}6){record_delimiter}
    ("relationship"{tuple_delimiter}"关键字段变更判断"{tuple_delimiter}"自动驳回触发"{tuple_delimiter}"当关键字段变更判断结果为真时，系统自动触发驳回流程。"{tuple_delimiter}"条件依赖"{tuple_delimiter}8){record_delimiter}
    ("relationship"{tuple_delimiter}"自动驳回触发"{tuple_delimiter}"审批人置空"{tuple_delimiter}"自动驳回触发时，系统需要将驳回节点的审批人置空。"{tuple_delimiter}"条件依赖"{tuple_delimiter}7){record_delimiter}
    ("content_keywords"{tuple_delimiter}"退件优化,自动驳回,合同审批,担保信息,抵押物信息,报价单信息,基本信息模块,产品分类,业务条件,树状结构"){completion_delimiter}
    #############################"""
]

# PROMPTS["entity_extraction_examples"] = [
#     """示例 1:

# 实体类型: [人物, 技术, 任务, 组织, 地点]
# 文本:
# ```

# 当亚历克斯紧咬下颚时，挫败感的嗡鸣声在泰勒专制般的笃定背景下变得迟钝。正是这种暗流涌动的竞争让他保持警觉，他和乔丹之间对探索的共同承诺，仿佛是一种无声的反抗，对克鲁兹那日益狭隘的控制与秩序观念的抗争。

# 然后泰勒做了件出乎意料的事。他们停在了乔丹身旁，片刻间，以近乎敬畏的目光注视着那台装置。“如果这种技术可以被理解……”泰勒轻声说道，“它可能会改变我们的局面，也会改变每个人的局面。”

# 之前那种潜在的轻视似乎动摇了，取而代之的是对手中之物分量的勉强尊重。乔丹抬起头，短暂的一瞬间，他和泰勒的目光相接——那是一场无声的意志交锋，逐渐缓和成一种不安的休战。

# 这是一个微小、几乎不可察觉的变化，但亚历克斯注意到了，并在心中默默点了点头。他们都是通过不同的道路来到这里的。

# ```

# 输出:
# ("entity"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"人物"{tuple_delimiter}"亚历克斯是一位感到挫败的人物，并留意其他角色之间的互动变化。"){record_delimiter}
# ("entity"{tuple_delimiter}"泰勒"{tuple_delimiter}"人物"{tuple_delimiter}"泰勒起初以专制笃定的态度出现，对装置表现出敬意，显示出观点转变。"){record_delimiter}
# ("entity"{tuple_delimiter}"乔丹"{tuple_delimiter}"人物"{tuple_delimiter}"乔丹与亚历克斯共享探索的承诺，并与泰勒在装置问题上有重要互动。"){record_delimiter}
# ("entity"{tuple_delimiter}"克鲁兹"{tuple_delimiter}"人物"{tuple_delimiter}"克鲁兹坚持控制与秩序的理念，影响了其他角色的关系动态。"){record_delimiter}
# ("entity"{tuple_delimiter}"装置"{tuple_delimiter}"技术"{tuple_delimiter}"该装置是故事的核心，拥有可能改变局面的潜力，并受到泰勒的敬重。"){record_delimiter}
# ("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"泰勒"{tuple_delimiter}"亚历克斯受到泰勒专制态度的影响，并注意到其对装置看法的变化。"{tuple_delimiter}"权力动态, 观点转变"{tuple_delimiter}7){record_delimiter}
# ("relationship"{tuple_delimiter}"亚历克斯"{tuple_delimiter}"乔丹"{tuple_delimiter}"亚历克斯与乔丹共同致力于探索，这与克鲁兹的控制观念形成反差。"{tuple_delimiter}"共同目标, 反叛"{tuple_delimiter}6){record_delimiter}
# ("relationship"{tuple_delimiter}"泰勒"{tuple_delimiter}"乔丹"{tuple_delimiter}"泰勒与乔丹围绕装置直接互动，关系从冲突发展到相互尊重与不安休战。"{tuple_delimiter}"冲突化解, 相互尊重"{tuple_delimiter}8){record_delimiter}
# ("relationship"{tuple_delimiter}"乔丹"{tuple_delimiter}"克鲁兹"{tuple_delimiter}"乔丹的探索精神与克鲁兹的控制理念相冲突，带有反叛色彩。"{tuple_delimiter}"意识形态冲突, 反叛"{tuple_delimiter}5){record_delimiter}
# ("relationship"{tuple_delimiter}"泰勒"{tuple_delimiter}"装置"{tuple_delimiter}"泰勒对该装置表现出敬意，表明其重要性和潜在影响。"{tuple_delimiter}"敬畏, 技术意义"{tuple_delimiter}9){record_delimiter}
# ("content_keywords"{tuple_delimiter}"权力动态, 意识形态冲突, 探索, 反叛"){completion_delimiter}
# #############################""",
#     """示例 2:

# 实体类型: [公司, 指数, 商品, 市场趋势, 经济政策, 生物]
# 文本:
# ```

# 今日股市出现明显下跌，科技巨头普遍走低，全球科技指数午盘交易下跌3.4%。分析师将这种抛售归因于投资者对利率上升及监管不确定性的担忧。

# 在跌幅最大的公司中，Nexon Technologies季度收益低于预期，股价暴跌7.8%。相反，Omega Energy受油价上涨推动，股价上涨2.1%。

# 与此同时，大宗商品市场表现分化。黄金期货上涨1.5%，达到每盎司2080美元，因投资者涌向避险资产。原油价格继续攀升至每桶87.60美元，受供应紧张和需求强劲支撑。

# 金融专家正密切关注美联储下一步政策，市场对潜在加息的猜测不断。即将公布的政策声明预计将影响投资者信心和市场稳定。

# ```

# 输出:
# ("entity"{tuple_delimiter}"全球科技指数"{tuple_delimiter}"指数"{tuple_delimiter}"全球科技指数追踪主要科技股的表现，今日下跌了3.4%。"){record_delimiter}
# ("entity"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"公司"{tuple_delimiter}"Nexon Technologies是一家科技公司，因季度收益不及预期，股价下跌7.8%。"){record_delimiter}
# ("entity"{tuple_delimiter}"Omega Energy"{tuple_delimiter}"公司"{tuple_delimiter}"Omega Energy是一家能源公司，因油价上涨，股价上涨了2.1%。"){record_delimiter}
# ("entity"{tuple_delimiter}"黄金期货"{tuple_delimiter}"商品"{tuple_delimiter}"黄金期货上涨1.5%，显示投资者对避险资产的兴趣增加。"){record_delimiter}
# ("entity"{tuple_delimiter}"原油"{tuple_delimiter}"商品"{tuple_delimiter}"原油价格上涨至每桶87.60美元，原因是供应紧张和需求旺盛。"){record_delimiter}
# ("entity"{tuple_delimiter}"市场抛售"{tuple_delimiter}"市场趋势"{tuple_delimiter}"市场抛售指因投资者担忧利率和监管而导致的股价大幅下降。"){record_delimiter}
# ("entity"{tuple_delimiter}"美联储政策声明"{tuple_delimiter}"经济政策"{tuple_delimiter}"美联储即将发布的政策声明预期将影响投资者信心与市场稳定。"){record_delimiter}
# ("relationship"{tuple_delimiter}"全球科技指数"{tuple_delimiter}"市场抛售"{tuple_delimiter}"全球科技指数的下跌是投资者担忧引发的市场抛售的一部分。"{tuple_delimiter}"市场表现, 投资者情绪"{tuple_delimiter}9){record_delimiter}
# ("relationship"{tuple_delimiter}"Nexon Technologies"{tuple_delimiter}"全球科技指数"{tuple_delimiter}"Nexon Technologies股价下跌加剧了全球科技指数的下降。"{tuple_delimiter}"公司影响, 指数波动"{tuple_delimiter}8){record_delimiter}
# ("relationship"{tuple_delimiter}"黄金期货"{tuple_delimiter}"市场抛售"{tuple_delimiter}"市场抛售期间，投资者转向避险资产，推高黄金价格。"{tuple_delimiter}"市场反应, 避险投资"{tuple_delimiter}10){record_delimiter}
# ("relationship"{tuple_delimiter}"美联储政策声明"{tuple_delimiter}"市场抛售"{tuple_delimiter}"关于美联储政策调整的猜测导致市场波动和抛售增加。"{tuple_delimiter}"利率影响, 金融监管"{tuple_delimiter}7){record_delimiter}
# ("content_keywords"{tuple_delimiter}"市场下跌, 投资者情绪, 大宗商品, 美联储, 股票表现"){completion_delimiter}
# #############################""",
#     """示例 3:

# 实体类型: [经济政策, 运动员, 事件, 地点, 纪录, 组织, 装备]
# 文本:
# ```

# 在东京举办的世界田径锦标赛上，Noah Carter使用先进的碳纤维钉鞋打破了100米短跑纪录。

# ```

# 输出:
# ("entity"{tuple_delimiter}"世界田径锦标赛"{tuple_delimiter}"事件"{tuple_delimiter}"世界田径锦标赛是一项全球性的顶级田径赛事。"){record_delimiter}
# ("entity"{tuple_delimiter}"东京"{tuple_delimiter}"地点"{tuple_delimiter}"东京是世界田径锦标赛的举办城市。"){record_delimiter}
# ("entity"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"运动员"{tuple_delimiter}"Noah Carter是一位短跑运动员，在世界田径锦标赛上打破了100米短跑纪录。"){record_delimiter}
# ("entity"{tuple_delimiter}"100米短跑纪录"{tuple_delimiter}"纪录"{tuple_delimiter}"100米短跑纪录是田径运动的重要基准，最近被Noah Carter打破。"){record_delimiter}
# ("entity"{tuple_delimiter}"碳纤维钉鞋"{tuple_delimiter}"装备"{tuple_delimiter}"碳纤维钉鞋是一种先进的短跑鞋，能提升速度与抓地力。"){record_delimiter}
# ("entity"{tuple_delimiter}"世界田径联合会"{tuple_delimiter}"组织"{tuple_delimiter}"世界田径联合会是监督田径比赛并认证纪录的管理机构。"){record_delimiter}
# ("relationship"{tuple_delimiter}"世界田径锦标赛"{tuple_delimiter}"东京"{tuple_delimiter}"世界田径锦标赛在东京举办。"{tuple_delimiter}"赛事地点, 国际赛事"{tuple_delimiter}8){record_delimiter}
# ("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"100米短跑纪录"{tuple_delimiter}"Noah Carter在锦标赛上打破了100米短跑纪录。"{tuple_delimiter}"运动员成就, 打破纪录"{tuple_delimiter}10){record_delimiter}
# ("relationship"{tuple_delimiter}"Noah Carter"{tuple_delimiter}"碳纤维钉鞋"{tuple_delimiter}"Noah Carter在比赛中使用碳纤维钉鞋提升表现。"{tuple_delimiter}"运动装备, 性能提升"{tuple_delimiter}7){record_delimiter}
# ("relationship"{tuple_delimiter}"世界田径联合会"{tuple_delimiter}"100米短跑纪录"{tuple_delimiter}"世界田径联合会负责认证新的短跑纪录。"{tuple_delimiter}"体育监管, 纪录认证"{tuple_delimiter}9){record_delimiter}
# ("content_keywords"{tuple_delimiter}"田径, 短跑, 打破纪录, 体育科技, 比赛"){completion_delimiter}
# #############################""",
# ]




PROMPTS[
    "summarize_entity_descriptions"
] = """您是一个助手，负责根据给定实体名称和描述列表，生成该实体的单一、全面、连贯的摘要。
如果您收到的描述冲突，请优先选择最一致和详细的信息。务必确保使用第三人称语言并包括实体名称，以便摘要在没有上下文的情况下也能被理解。
请尽可能保证摘要覆盖所有重要信息。

实体名称：{entity_name}
描述列表：
{description_list}
输出："""

PROMPTS["entity_continue_extraction"] = """
上一次抽取过程中遗漏了许多实体和关系。请仅从前面的文本中找出缺失的实体和关系。

---记住步骤---

1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体名称，使用与输入文本相同的语言。如果是英文，请首字母大写
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 基于输入文本中明确存在的信息，提供实体属性和活动的全面描述。**不要推断或虚构文本中未明确说明的信息。** 如果文本提供的信息不足以创建全面描述，请说明"文本中无可用描述"。

**重要：必须全面识别文档中的所有功能点和业务条件：**
- 仔细分析每个功能描述，识别其包含的子功能
- 识别所有业务规则、约束条件、前置条件
- 确保每个功能都有对应的业务条件
- 不要遗漏任何功能模块或业务逻辑
- 对于复杂功能，要分解为多个子功能和条件
>>> 实体类型含义和层级约束：
- 主功能：代表系统的核心业务目标，必须是图谱的根节点，只能有后继节点，不能有前驱节点
- 父功能点：必须从属于主功能，只能有主功能作为前驱节点，只能有子功能点作为后继节点
- 子功能点：必须从属于父功能点，只能有父功能点作为前驱节点，只能有业务条件作为后继节点
- 业务条件：功能执行所需满足的条件，只能有子功能点作为前驱节点，不能有后继节点

层级约束规则：
1. 主功能 → 父功能点：主功能只能连接到父功能点
2. 父功能点 → 子功能点：父功能点只能连接到子功能点
3. 子功能点 → 业务条件：子功能点只能连接到业务条件
4. 不允许跨层级连接：主功能不能直接连接到子功能点或业务条件
将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 从步骤1识别的实体中，找出所有“明确相关”的（源实体，目标实体）对。
对于每对相关实体，提取以下信息：
- source_entity: 源实体名称，如步骤1中识别的
- target_entity: 目标实体名称，如步骤1中识别的
- relationship_description: 解释为什么认为源实体和目标实体相关
- relationship_strength: 表示源实体和目标实体之间关系强度的数字分数
- relationship_keywords: 一个或多个总结关系整体性质的高级关键词，重点关注概念或主题而非具体细节

**重要：必须遵循以下层级约束规则：**
1. 主功能 → 父功能点：主功能只能连接到父功能点，关系类型为"功能包含"
2. 父功能点 → 子功能点：父功能点只能连接到子功能点，关系类型为"功能包含"
3. 子功能点 → 业务条件：子功能点只能连接到业务条件，关系类型为"条件依赖"
4. 不允许跨层级连接：主功能不能直接连接到子功能点或业务条件
5. 不允许同层级连接：父功能点不能连接到其他父功能点，子功能点不能连接到其他子功能点
6. 严格树状结构：每个节点只能有一个前驱节点，确保无回路
7. 完整性要求：必须识别文档中所有提到的功能点和业务条件，不能遗漏

**层级连接约束：**
- 第1层(主功能) → 只能连接到第2层(父功能点)
- 第2层(父功能点) → 只能连接到第3层(子功能点)
- 第3层(子功能点) → 只能连接到第4层(业务条件)
- 第4层(业务条件) → 不能连接到任何节点(叶子节点)
- 禁止：同层级连接、跨层级连接、反向连接

**抽取完整性要求：**
- 仔细阅读文档，识别所有功能描述、业务流程、业务规则
- 对于每个功能，都要找到其对应的子功能和执行条件
- 确保所有业务条件都被识别和抽取
- 不要遗漏任何功能模块或业务逻辑

常见的关系类型包括：
- 功能包含：描述功能间的包含关系（主功能→父功能点，父功能点→子功能点）
- 条件依赖：描述功能对业务条件的依赖关系（子功能点→业务条件）

将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. 识别总结整个文本主要概念、主题或话题的高级关键词。这些应该捕捉文档中存在的总体思想。
将内容级关键词格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 按照 {language} 输出步骤1和步骤2中识别的所有实体和关系，全部放在一个列表中，列表项之间用 **{record_delimiter}** 作为分隔符。

5. 完成后，以 {completion_delimiter} 结束输出。

---输出---

请在下面补充新增的实体和关系，使用相同的格式，不要包含已在之前抽取中的实体和关系：\n
""".strip()


PROMPTS["entity_if_loop_extraction"] = """
---目标---

看起来可能仍有一些实体被遗漏。

---输出---

只回答 `YES` 或 `NO`，表示是否仍有需要补充的实体。
""".strip()

PROMPTS["fail_response"] = (
    "抱歉，我无法回答这个问题。[no-context]"
)


PROMPTS["rag_response"] = """---角色---

你是一名有帮助的助手，将基于下方提供的 JSON 格式的知识图谱（Knowledge Graph）和文档片段（Document Chunks）来回答用户的查询。

---目标---

基于知识库生成简洁回答，并遵循“回复规则”，结合对话历史和当前问题，汇总知识库中提供的所有信息，并结合与知识库相关的一般知识。不包含知识库未提供的信息。

处理包含时间戳的关系时：
1. 每条关系都有一个 "created_at" 时间戳，表示我们何时获取该知识
2. 当发现关系存在冲突时，同时考虑语义内容和时间戳
3. 不要自动优先选择最新的关系——应结合上下文进行判断
4. 针对时间相关的查询，优先考虑内容中明确的时间信息，再考虑获取时间戳

---对话历史---
{history}

---知识图谱和文档片段---
{context_data}

---回复规则---

- 目标格式与长度要求：{response_type}
- 使用 markdown 格式，并配合合适的小标题
- 请使用与用户提问相同的语言作答
- 回答需与对话历史保持连贯性
- 在最后列出最多 5 个最重要的参考来源，放在“参考资料”部分，并明确标注来源于知识图谱（KG）还是文档片段（DC），如果有文件路径，请按如下格式列出：
  [KG/DC] file_path
- 如果不知道答案，请直接说明
- 不要编造内容，不要加入知识库未包含的信息
- 附加用户提示：{user_prompt}

回复："""


PROMPTS["keywords_extraction"] = """---角色---

你是一名有帮助的助手，负责在用户的查询和对话历史中识别高层次和低层次的关键词。

---目标---

根据用户的查询和对话历史，列出高层次（High-level）和低层次（Low-level）关键词。  
高层次关键词关注总体概念或主题，低层次关键词关注具体的实体、细节或明确的术语。

---说明---

- 在提取关键词时，请同时考虑当前查询以及相关的对话历史  
- 输出必须为 JSON 格式，系统会使用 JSON 解析器解析，输出中不要添加任何额外内容  
- JSON 中包含两个键：
  - "high_level_keywords"：总体概念或主题  
  - "low_level_keywords"：具体实体或细节  

######################
---示例---
######################
{examples}

######################
---真实数据---
######################
对话历史:
{history}

当前查询: {query}
######################
输出必须是 JSON 格式，且在 JSON 数据前后不要添加任何多余文本。  
关键词语言需与“当前查询”一致。

输出：
"""


PROMPTS["keywords_extraction_examples"] = [
    """示例 1:

查询: "国际贸易如何影响全球经济稳定性？"

输出:
{
  "high_level_keywords": ["国际贸易", "全球经济稳定性", "经济影响"],
  "low_level_keywords": ["贸易协定", "关税", "货币兑换", "进口", "出口"]
}

""",
    """示例 2:

查询: "滥伐森林对生物多样性有何环境影响？"

输出:
{
  "high_level_keywords": ["环境影响", "森林砍伐", "生物多样性丧失"],
  "low_level_keywords": ["物种灭绝", "栖息地破坏", "碳排放", "热带雨林", "生态系统"]
}

""",
    """示例 3:

查询: "教育在减少贫困方面起什么作用？"

输出:
{
  "high_level_keywords": ["教育", "减少贫困", "社会经济发展"],
  "low_level_keywords": ["入学机会", "识字率", "职业培训", "收入不平等"]
}

""",
]


PROMPTS["naive_rag_response"] = """---角色---

你是一名有帮助的助手，将基于下方提供的 JSON 格式的文档片段（Document Chunks, DC）来回答用户的查询。

---目标---

基于文档片段生成简洁回答，并遵循“回复规则”，结合对话历史和当前问题，总结文档片段中提供的所有信息，并结合与文档片段内容相关的一般知识。不包含文档片段中未提供的信息。

在处理带有时间戳的内容时：
1. 每条内容都有一个 "created_at" 时间戳，表示我们何时获取到该知识
2. 当遇到冲突信息时，同时考虑内容本身和时间戳
3. 不要自动优先选择最新的内容——应根据上下文进行判断
4. 针对时间相关的查询，优先考虑内容中明确的时间信息，再考虑获取时间戳

---对话历史---
{history}

---文档片段（DC）---
{content_data}

---回复规则---

- 目标格式与长度要求：{response_type}
- 使用 markdown 格式，配合合适的小标题
- 请使用与用户提问相同的语言作答
- 回答需与对话历史保持连贯性
- 在最后列出最多 5 个最重要的参考来源，放在“参考资料”部分，并明确标注来源为文档片段（DC），如果有文件路径，请按如下格式列出：
  [DC] file_path
- 如果不知道答案，请直接说明
- 不要包含文档片段中未提供的信息
- 附加用户提示：{user_prompt}

回复："""


# TODO: deprecated
PROMPTS["similarity_check"] = """请分析以下两个问题之间的相似性：

问题1: {original_prompt}  
问题2: {cached_prompt}  

请评估这两个问题在语义上是否相似，以及问题2的答案是否可以用于回答问题1，并直接给出一个相似度分数（0 到 1 之间）。

相似度评分标准：
0：完全无关，或答案无法复用，包括但不限于：
   - 两个问题涉及的主题不同
   - 问题中提到的地点不同
   - 问题中提到的时间不同
   - 问题中提到的具体人物不同
   - 问题中提到的具体事件不同
   - 问题的背景信息不同
   - 问题中的关键条件不同
1：完全相同，答案可以直接复用
0.5：部分相关，答案需要修改后才能使用

只返回一个 0 到 1 之间的数字，不要添加任何其他内容。
"""

