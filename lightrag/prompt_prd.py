from __future__ import annotations
from typing import Any

# PRD专用实体抽取配置
PRD_PROMPTS: dict[str, Any] = {}

# PRD实体类型定义
PRD_PROMPTS["PRD_ENTITY_TYPES"] = [
    "主功能", 
    "父功能点", 
    "子功能点", 
    "业务规则", 
    "前置条件", 
    "后置条件", 
    "异常处理", 
    "数据字段", 
    "用户角色", 
    "系统接口"
]

# PRD实体类型详细描述
PRD_PROMPTS["PRD_ENTITY_TYPES_DESCRIPTIONS"] = """>>> PRD实体类型含义：
- 主功能：代表系统的核心业务目标，是整个PRD文档描述的主要功能
- 父功能点：为需求主功能的并列模块，代表独立的核心业务功能，通常包含多个子功能点
- 子功能点：必须从属于对应的父功能点，是父功能点的具体组成部分，代表更细粒度的功能需求
- 业务规则：描述功能实现时必须遵循的业务逻辑和约束条件
- 前置条件：功能执行前必须满足的条件或状态
- 后置条件：功能执行完成后系统应达到的状态或结果
- 异常处理：描述功能执行过程中可能出现的异常情况及处理方式
- 数据字段：功能涉及的关键数据项，包括字段名称、类型、约束等
- 用户角色：参与功能执行的各类用户角色及其权限
- 系统接口：功能与其他系统或模块的交互接口
"""

# PRD关系类型定义
PRD_PROMPTS["PRD_RELATIONSHIP_TYPES"] = [
    "包含关系", 
    "依赖关系", 
    "触发关系", 
    "数据流向", 
    "权限控制", 
    "业务流程", 
    "条件判断", 
    "异常分支"
]

# PRD关系类型详细描述
PRD_PROMPTS["PRD_RELATIONSHIP_TYPES_DESCRIPTIONS"] = """>>> PRD关系类型含义：
- 包含关系：表示功能点之间的层次结构，如父功能点包含子功能点
- 依赖关系：表示功能点之间的依赖关系，如某个功能必须在另一个功能完成后才能执行
- 触发关系：表示某个事件或条件触发功能执行的关系
- 数据流向：表示数据在功能点之间的传递和流转关系
- 权限控制：表示用户角色与功能点之间的权限关系
- 业务流程：表示功能点之间的执行顺序和流程关系
- 条件判断：表示功能执行的条件分支和判断逻辑
- 异常分支：表示功能执行异常时的处理分支
"""

# PRD实体抽取主prompt
PRD_PROMPTS["prd_entity_extraction"] = """---角色---
你是一个专业的PRD文档分析师，专门负责从产品需求文档中提取功能点、业务规则和系统关系。

---目标---
根据提供的PRD文本文档，识别文本中所有相关的实体和关系，构建完整的功能架构图。
使用{language}作为输出语言。

---步骤---
1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体名称，使用与输入文本相同的语言
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 基于输入文本中明确存在的信息，提供实体属性和活动的全面描述
- entity_priority: 实体优先级（高/中/低），基于文档中的描述判断
- entity_complexity: 实体复杂度（简单/中等/复杂），基于功能实现的复杂程度判断

>>> 实体类型含义：
{entity_types_descriptions}

将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_priority>{tuple_delimiter}<entity_complexity>)

2. 从步骤1识别的实体中，找出所有"明确相关"的（源实体，目标实体）对。
对于每对相关实体，提取以下信息：
- source_entity: 源实体名称
- target_entity: 目标实体名称
- relationship_type: 关系类型，从以下选择：[{relationship_types}]
- relationship_description: 详细描述两个实体之间的关系
- relationship_strength: 关系强度分数（1-10，10表示关系最强）
- relationship_keywords: 关系的关键词标签
- relationship_conditions: 关系成立的条件（如果有）

>>> 关系类型含义：
{relationship_types_descriptions}

将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_type>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>{tuple_delimiter}<relationship_conditions>)

3. 识别总结整个PRD文档主要概念、主题或话题的高级关键词。
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
关系类型: [{relationship_types}]
文本:
{input_text}
######################
输出:"""

# PRD实体抽取示例
PRD_PROMPTS["prd_entity_extraction_examples"] = [
    """示例 1：
    实体类型：[主功能, 父功能点, 子功能点, 业务规则, 前置条件, 后置条件, 异常处理, 数据字段, 用户角色, 系统接口]
    关系类型：[包含关系, 依赖关系, 触发关系, 数据流向, 权限控制, 业务流程, 条件判断, 异常分支]
    文本：
    ```
    [功能需求规格说明书—用户注册系统]
    
    1. 系统概述
    用户注册系统允许新用户创建账户，支持邮箱验证和手机号验证两种方式。
    
    2. 功能需求
    2.1 用户注册主流程
    2.1.1 注册信息输入
    - 用户必须提供：用户名、密码、邮箱或手机号
    - 用户名长度：3-20个字符，只能包含字母、数字、下划线
    - 密码强度：至少8位，包含大小写字母、数字和特殊字符
    
    2.1.2 信息验证
    - 邮箱验证：发送验证邮件，用户点击链接激活账户
    - 手机号验证：发送验证码，用户输入验证码激活账户
    - 验证码有效期：5分钟
    
    2.1.3 账户激活
    - 验证成功后，账户状态变为"已激活"
    - 系统自动创建用户档案
    - 发送欢迎邮件
    
    2.2 异常处理
    2.2.1 重复注册检测
    - 检测用户名、邮箱、手机号是否已存在
    - 如存在，提示用户并阻止注册
    
    2.2.2 验证失败处理
    - 验证码过期：提示重新获取
    - 验证失败：记录失败次数，超过3次锁定账户1小时
    
    3. 业务规则
    3.1 用户角色权限
    - 未激活用户：只能查看基本信息
    - 已激活用户：可以正常使用系统功能
    - 管理员：可以管理所有用户账户
    
    3.2 数据安全
    - 密码必须加密存储
    - 敏感信息传输使用HTTPS
    - 登录失败超过5次，账户锁定24小时
    ```
    
    输出：
    ("entity"{tuple_delimiter}"用户注册系统"{tuple_delimiter}"主功能"{tuple_delimiter}"允许新用户创建账户，支持邮箱验证和手机号验证两种方式的用户注册系统"{tuple_delimiter}"高"{tuple_delimiter}"中等"){record_delimiter}
    ("entity"{tuple_delimiter}"用户注册主流程"{tuple_delimiter}"父功能点"{tuple_delimiter}"用户注册的核心流程，包括信息输入、验证和账户激活"{tuple_delimiter}"高"{tuple_delimiter}"中等"){record_delimiter}
    ("entity"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"子功能点"{tuple_delimiter}"用户输入注册信息，包括用户名、密码、邮箱或手机号"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"信息验证"{tuple_delimiter}"子功能点"{tuple_delimiter}"验证用户提供的邮箱或手机号的有效性"{tuple_delimiter}"中"{tuple_delimiter}"中等"){record_delimiter}
    ("entity"{tuple_delimiter}"账户激活"{tuple_delimiter}"子功能点"{tuple_delimiter}"验证成功后激活用户账户并创建用户档案"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"重复注册检测"{tuple_delimiter}"子功能点"{tuple_delimiter}"检测用户名、邮箱、手机号是否已存在，防止重复注册"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"验证失败处理"{tuple_delimiter}"子功能点"{tuple_delimiter}"处理验证失败的情况，包括验证码过期和验证失败次数限制"{tuple_delimiter}"中"{tuple_delimiter}"中等"){record_delimiter}
    ("entity"{tuple_delimiter}"用户名长度限制"{tuple_delimiter}"业务规则"{tuple_delimiter}"用户名长度必须在3-20个字符之间，只能包含字母、数字、下划线"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"密码强度要求"{tuple_delimiter}"业务规则"{tuple_delimiter}"密码至少8位，必须包含大小写字母、数字和特殊字符"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"验证码有效期"{tuple_delimiter}"业务规则"{tuple_delimiter}"验证码有效期为5分钟"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"账户状态"{tuple_delimiter}"数据字段"{tuple_delimiter}"用户账户的状态信息，包括未激活、已激活、已锁定等"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"用户档案"{tuple_delimiter}"数据字段"{tuple_delimiter}"用户的基本信息和配置信息"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"未激活用户"{tuple_delimiter}"用户角色"{tuple_delimiter}"已完成注册但未通过验证的用户，只能查看基本信息"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"已激活用户"{tuple_delimiter}"用户角色"{tuple_delimiter}"已完成注册并通过验证的用户，可以正常使用系统功能"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"管理员"{tuple_delimiter}"用户角色"{tuple_delimiter}"具有管理所有用户账户权限的系统管理员"{tuple_delimiter}"中"{tuple_delimiter}"简单"){record_delimiter}
    ("entity"{tuple_delimiter}"邮箱验证接口"{tuple_delimiter}"系统接口"{tuple_delimiter}"发送验证邮件和验证邮箱链接的接口"{tuple_delimiter}"中"{tuple_delimiter}"中等"){record_delimiter}
    ("entity"{tuple_delimiter}"短信验证接口"{tuple_delimiter}"系统接口"{tuple_delimiter}"发送验证码和验证短信的接口"{tuple_delimiter}"中"{tuple_delimiter}"中等"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户注册系统"{tuple_delimiter}"用户注册主流程"{tuple_delimiter}"包含关系"{tuple_delimiter}"用户注册系统包含用户注册主流程这个核心功能模块"{tuple_delimiter}"功能架构,核心模块"{tuple_delimiter}10{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户注册主流程"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"包含关系"{tuple_delimiter}"用户注册主流程包含注册信息输入这个子功能"{tuple_delimiter}"功能包含,流程步骤"{tuple_delimiter}9{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户注册主流程"{tuple_delimiter}"信息验证"{tuple_delimiter}"包含关系"{tuple_delimiter}"用户注册主流程包含信息验证这个子功能"{tuple_delimiter}"功能包含,流程步骤"{tuple_delimiter}9{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户注册主流程"{tuple_delimiter}"账户激活"{tuple_delimiter}"包含关系"{tuple_delimiter}"用户注册主流程包含账户激活这个子功能"{tuple_delimiter}"功能包含,流程步骤"{tuple_delimiter}9{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"信息验证"{tuple_delimiter}"依赖关系"{tuple_delimiter}"信息验证必须在注册信息输入完成后才能执行"{tuple_delimiter}"流程依赖,执行顺序"{tuple_delimiter}8{tuple_delimiter}"注册信息输入完成"){record_delimiter}
    ("relationship"{tuple_delimiter}"信息验证"{tuple_delimiter}"账户激活"{tuple_delimiter}"依赖关系"{tuple_delimiter}"账户激活必须在信息验证成功后才能执行"{tuple_delimiter}"流程依赖,执行顺序"{tuple_delimiter}8{tuple_delimiter}"信息验证成功"){record_delimiter}
    ("relationship"{tuple_delimiter}"信息验证"{tuple_delimiter}"邮箱验证接口"{tuple_delimiter}"依赖关系"{tuple_delimiter}"信息验证功能依赖邮箱验证接口来发送验证邮件"{tuple_delimiter}"接口依赖,功能实现"{tuple_delimiter}7{tuple_delimiter}"选择邮箱验证方式"){record_delimiter}
    ("relationship"{tuple_delimiter}"信息验证"{tuple_delimiter}"短信验证接口"{tuple_delimiter}"依赖关系"{tuple_delimiter}"信息验证功能依赖短信验证接口来发送验证码"{tuple_delimiter}"接口依赖,功能实现"{tuple_delimiter}7{tuple_delimiter}"选择手机号验证方式"){record_delimiter}
    ("relationship"{tuple_delimiter}"重复注册检测"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"触发关系"{tuple_delimiter}"当用户输入注册信息时，系统自动触发重复注册检测"{tuple_delimiter}"自动触发,实时检测"{tuple_delimiter}8{tuple_delimiter}"用户输入注册信息"){record_delimiter}
    ("relationship"{tuple_delimiter}"验证失败处理"{tuple_delimiter}"信息验证"{tuple_delimiter}"异常分支"{tuple_delimiter}"当信息验证失败时，系统进入验证失败处理流程"{tuple_delimiter}"异常处理,流程分支"{tuple_delimiter}7{tuple_delimiter}"信息验证失败"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户名长度限制"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"业务规则"{tuple_delimiter}"注册信息输入功能必须遵循用户名长度限制的业务规则"{tuple_delimiter}"规则约束,输入验证"{tuple_delimiter}8{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"密码强度要求"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"业务规则"{tuple_delimiter}"注册信息输入功能必须遵循密码强度要求的业务规则"{tuple_delimiter}"规则约束,输入验证"{tuple_delimiter}8{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"验证码有效期"{tuple_delimiter}"信息验证"{tuple_delimiter}"业务规则"{tuple_delimiter}"信息验证功能必须遵循验证码有效期的业务规则"{tuple_delimiter}"规则约束,时间控制"{tuple_delimiter}8{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"账户状态"{tuple_delimiter}"账户激活"{tuple_delimiter}"数据流向"{tuple_delimiter}"账户激活功能会更新账户状态字段"{tuple_delimiter}"数据更新,状态变更"{tuple_delimiter}7{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"用户档案"{tuple_delimiter}"账户激活"{tuple_delimiter}"数据流向"{tuple_delimiter}"账户激活功能会创建用户档案数据"{tuple_delimiter}"数据创建,档案管理"{tuple_delimiter}7{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"未激活用户"{tuple_delimiter}"注册信息输入"{tuple_delimiter}"权限控制"{tuple_delimiter}"未激活用户角色可以访问注册信息输入功能"{tuple_delimiter}"角色权限,功能访问"{tuple_delimiter}6{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"已激活用户"{tuple_delimiter}"账户激活"{tuple_delimiter}"权限控制"{tuple_delimiter}"已激活用户角色拥有账户激活后的所有权限"{tuple_delimiter}"角色权限,功能访问"{tuple_delimiter}6{tuple_delimiter}"无"){record_delimiter}
    ("relationship"{tuple_delimiter}"管理员"{tuple_delimiter}"重复注册检测"{tuple_delimiter}"权限控制"{tuple_delimiter}"管理员角色可以查看和管理重复注册检测的结果"{tuple_delimiter}"角色权限,管理功能"{tuple_delimiter}6{tuple_delimiter}"无"){record_delimiter}
    ("content_keywords"{tuple_delimiter}"用户注册,账户管理,身份验证,安全控制,业务流程,异常处理,权限管理"){completion_delimiter}
    #############################"""
]

# PRD实体继续抽取prompt
PRD_PROMPTS["prd_entity_continue_extraction"] = """
上一次抽取过程中遗漏了许多实体和关系。请仅从前面的文本中找出缺失的实体和关系。

---记住步骤---

1. 识别所有实体。对于每个识别出的实体，提取以下信息：
- entity_name: 实体名称，使用与输入文本相同的语言
- entity_type: 以下类型之一：[{entity_types}]
- entity_description: 基于输入文本中明确存在的信息，提供实体属性和活动的全面描述
- entity_priority: 实体优先级（高/中/低），基于文档中的描述判断
- entity_complexity: 实体复杂度（简单/中等/复杂），基于功能实现的复杂程度判断

>>> 实体类型含义：
{entity_types_descriptions}

将每个实体格式化为 ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>{tuple_delimiter}<entity_priority>{tuple_delimiter}<entity_complexity>)

2. 从步骤1识别的实体中，找出所有"明确相关"的（源实体，目标实体）对。
对于每对相关实体，提取以下信息：
- source_entity: 源实体名称
- target_entity: 目标实体名称
- relationship_type: 关系类型，从以下选择：[{relationship_types}]
- relationship_description: 详细描述两个实体之间的关系
- relationship_strength: 关系强度分数（1-10，10表示关系最强）
- relationship_keywords: 关系的关键词标签
- relationship_conditions: 关系成立的条件（如果有）

>>> 关系类型含义：
{relationship_types_descriptions}

将每个关系格式化为 ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_type>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>{tuple_delimiter}<relationship_conditions>)

3. 识别总结整个PRD文档主要概念、主题或话题的高级关键词。
将内容级关键词格式化为 ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. 按照 {language} 输出步骤1和步骤2中识别的所有实体和关系，全部放在一个列表中，列表项之间用 **{record_delimiter}** 作为分隔符。

5. 完成后，以 {completion_delimiter} 结束输出。

---输出---

请在下面补充新增的实体和关系，使用相同的格式，不要包含已在之前抽取中的实体和关系：\n
""".strip()

# PRD实体循环检查prompt
PRD_PROMPTS["prd_entity_if_loop_extraction"] = """
---目标---

看起来可能仍有一些实体被遗漏。

---输出---

只回答 `YES` 或 `NO`，表示是否仍有需要补充的实体。
""".strip()

# PRD实体描述摘要prompt
PRD_PROMPTS["prd_summarize_entity_descriptions"] = """您是一个PRD文档分析师，负责根据给定实体名称和描述列表，生成该实体的单一、全面、连贯的摘要。
如果您收到的描述冲突，请优先选择最一致和详细的信息。务必确保使用第三人称语言并包括实体名称，以便摘要在没有上下文的情况下也能被理解。
请尽可能保证摘要覆盖所有重要信息，包括实体的功能、规则、约束等。

实体名称：{entity_name}
描述列表：
{description_list}
输出："""

# PRD RAG响应prompt
PRD_PROMPTS["prd_rag_response"] = """---角色---

你是一名专业的PRD文档分析师，将基于下方提供的JSON格式的知识图谱（Knowledge Graph）和文档片段（Document Chunks）来回答用户的查询。

---目标---

基于知识库生成简洁回答，并遵循"回复规则"，结合对话历史和当前问题，汇总知识库中提供的所有信息，并结合与知识库相关的一般知识。不包含知识库未提供的信息。

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
- 在最后列出最多 5 个最重要的参考来源，放在"参考资料"部分，并明确标注来源于知识图谱（KG）还是文档片段（DC），如果有文件路径，请按如下格式列出：
  [KG/DC] file_path
- 如果不知道答案，请直接说明
- 不要编造内容，不要加入知识库未包含的信息
- 附加用户提示：{user_prompt}

回复："""
