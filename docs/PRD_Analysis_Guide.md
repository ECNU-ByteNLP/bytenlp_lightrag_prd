# LightRAG PRD文档分析指南

## 概述

本指南介绍如何使用修改后的LightRAG框架进行PRD（产品需求文档）的功能点抽取和关系分析。LightRAG已经针对PRD文档进行了专门优化，能够更好地识别功能点、业务规则、前置条件等实体，以及它们之间的包含关系、依赖关系、触发关系等。

## 主要特性

### 1. 专门的PRD实体类型
- **主功能**: 代表系统的核心业务目标
- **父功能点**: 为需求主功能的并列模块，代表独立的核心业务功能
- **子功能点**: 必须从属于对应的父功能点，是父功能点的具体组成部分
- **业务规则**: 描述功能实现时必须遵循的业务逻辑和约束条件
- **前置条件**: 功能执行前必须满足的条件或状态
- **后置条件**: 功能执行完成后系统应达到的状态或结果
- **异常处理**: 描述功能执行过程中可能出现的异常情况及处理方式
- **数据字段**: 功能涉及的关键数据项，包括字段名称、类型、约束等
- **用户角色**: 参与功能执行的各类用户角色及其权限
- **系统接口**: 功能与其他系统或模块的交互接口

### 2. 专门的关系类型
- **包含关系**: 表示功能点之间的层次结构
- **依赖关系**: 表示功能点之间的依赖关系
- **触发关系**: 表示某个事件或条件触发功能执行的关系
- **数据流向**: 表示数据在功能点之间的传递和流转关系
- **权限控制**: 表示用户角色与功能点之间的权限关系
- **业务流程**: 表示功能点之间的执行顺序和流程关系
- **条件判断**: 表示功能执行的条件分支和判断逻辑
- **异常分支**: 表示功能执行异常时的处理分支

### 3. 优化的抽取能力
- 支持实体优先级分析（高/中/低）
- 支持实体复杂度评估（简单/中等/复杂）
- 支持关系条件判断
- 专门针对PRD文档结构的prompt优化

## 安装和配置

### 1. 环境要求
- Python 3.8+
- LightRAG框架
- LLM服务（OpenAI、Ollama等）
- Embedding服务

### 2. 配置文件
复制 `env.prd.example` 为 `.env` 并根据需要修改：

```bash
cp env.prd.example .env
```

主要配置项：
```bash
# LLM配置
LLM_BINDING=openai
LLM_MODEL=gpt-4o
LLM_BINDING_API_KEY=your_api_key

# Embedding配置
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIM=3072

# 存储配置
LIGHTRAG_KV_STORAGE=PGKVStorage
LIGHTRAG_GRAPH_STORAGE=PGGraphStorage
LIGHTRAG_VECTOR_STORAGE=PGVectorStorage

# PRD专用配置
WORKSPACE=prd_analysis
CHUNK_SIZE=1500
CHUNK_OVERLAP_SIZE=200
MAX_GLEANING=2
```

### 3. 数据库准备
如果使用PostgreSQL，需要：
1. 安装PostgreSQL 16.6+
2. 安装pgvector扩展
3. 创建数据库：`lightrag_prd`

## 使用方法

### 1. 基本使用

```python
import asyncio
from lightrag.lightrag import LightRAG
from lightrag.prompt import PROMPTS

async def main():
    # 创建LightRAG实例
    rag = LightRAG(
        working_dir="./rag_storage_prd",
        workspace="prd_analysis",
        
        # PRD专用配置
        addon_params={
            "language": "中文",
            "entity_types": PROMPTS["PRD_ENTITY_TYPES"],
            "relationship_types": PROMPTS["PRD_RELATIONSHIP_TYPES"],
            "example_number": 1,
        }
    )
    
    # 初始化存储
    await rag.initialize_storages()
    
    # 插入PRD文档
    result = await rag.insert_document("path/to/prd.docx")
    
    # 查询分析
    response = await rag.query("这个系统有哪些主要功能？")
    print(response)

# 运行
asyncio.run(main())
```

### 2. 使用示例脚本

运行提供的示例脚本：

```bash
python examples/lightrag_prd_analysis_demo.py
```

### 3. 使用Web UI

启动LightRAG服务器：

```bash
lightrag-server --config .env
```

然后在浏览器中访问 `http://localhost:9621` 使用Web界面。

## 最佳实践

### 1. 文档准备
- 确保PRD文档结构清晰，功能点层次分明
- 使用标准的文档格式（.docx、.pdf、.txt）
- 避免过于复杂的表格和图表

### 2. 配置优化
- 根据文档复杂度调整 `CHUNK_SIZE` 和 `CHUNK_OVERLAP_SIZE`
- 使用 `MAX_GLEANING=2` 或更高值以获得更完整的抽取结果
- 启用缓存以减少LLM调用成本

### 3. 查询策略
- 使用具体的问题描述
- 结合功能点和业务规则进行查询
- 利用关系信息进行深度分析

### 4. 结果分析
- 关注实体之间的层次关系
- 分析业务流程的完整性
- 检查异常处理是否覆盖全面

## 常见问题

### 1. 实体抽取不完整
**解决方案**：
- 增加 `MAX_GLEANING` 值
- 调整 `CHUNK_SIZE` 以保持功能点完整性
- 检查文档结构是否清晰

### 2. 关系识别不准确
**解决方案**：
- 确保文档中明确描述了功能点之间的关系
- 使用更详细的prompt描述
- 调整相似度阈值

### 3. 性能问题
**解决方案**：
- 使用PostgreSQL或Neo4j等生产级存储
- 启用缓存功能
- 调整并发参数

### 4. 内存不足
**解决方案**：
- 减少 `MAX_TOTAL_TOKENS` 值
- 调整 `TOP_K` 和 `CHUNK_TOP_K`
- 使用流式处理

## 高级功能

### 1. 自定义实体类型
可以在 `addon_params` 中自定义实体类型：

```python
addon_params={
    "entity_types": ["主功能", "子功能", "业务规则", "技术约束"],
    "relationship_types": ["包含", "依赖", "约束"],
}
```

### 2. 多语言支持
支持多种语言的PRD文档分析：

```python
addon_params={
    "language": "English",  # 或 "中文", "French" 等
}
```

### 3. 批量处理
支持批量处理多个PRD文档：

```python
documents = ["prd1.docx", "prd2.docx", "prd3.docx"]
for doc in documents:
    await rag.insert_document(doc)
```

## 输出格式

### 1. 实体输出
```json
{
    "entity_name": "用户注册",
    "entity_type": "主功能",
    "entity_description": "允许新用户创建账户的功能",
    "entity_priority": "高",
    "entity_complexity": "中等"
}
```

### 2. 关系输出
```json
{
    "source_entity": "用户注册",
    "target_entity": "信息验证",
    "relationship_type": "包含关系",
    "relationship_description": "用户注册功能包含信息验证步骤",
    "relationship_keywords": "功能包含,流程步骤",
    "relationship_strength": 9,
    "relationship_conditions": "无"
}
```

## 扩展开发

### 1. 添加新的实体类型
在 `lightrag/prompt.py` 中添加新的实体类型定义。

### 2. 自定义抽取逻辑
继承相关类并重写抽取方法。

### 3. 集成其他工具
可以集成其他PRD分析工具，如：
- 流程图生成
- 依赖关系可视化
- 风险评估

## 总结

LightRAG的PRD专用功能为产品需求文档分析提供了强大的支持。通过专门的实体类型定义、关系类型识别和优化的抽取算法，能够准确识别PRD文档中的功能点、业务规则和系统关系，为产品开发和项目管理提供有价值的 insights。

通过合理配置和最佳实践，LightRAG能够成为PRD文档分析的有力工具，帮助团队更好地理解需求、分析依赖关系、识别潜在风险，从而提高产品开发的质量和效率。
