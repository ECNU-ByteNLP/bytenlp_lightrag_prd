#!/usr/bin/env python3
"""
LightRAG PRD文档分析示例

这个示例展示了如何使用LightRAG框架进行PRD文档的功能点抽取和关系分析。
专门针对产品需求文档进行了优化，能够识别功能点、业务规则、前置条件等实体，
以及它们之间的包含关系、依赖关系、触发关系等。

主要特性：
1. 专门的PRD实体类型定义（主功能、父功能点、子功能点、业务规则等）
2. 专门的关系类型定义（包含关系、依赖关系、触发关系等）
3. 优化的抽取prompt，更适合PRD文档结构
4. 支持实体优先级和复杂度分析
5. 支持关系条件判断

使用方法：
1. 确保已安装LightRAG和相关依赖
2. 配置LLM和Embedding服务（OpenAI、Ollama等）
3. 将PRD文档放入inputs目录
4. 运行此脚本进行分析

作者：LightRAG团队
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Any

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from lightrag.lightrag import LightRAG
from lightrag.prompt import PROMPTS
from lightrag.llm import openai_alike_model_complete
from lightrag.embedding import openai_embed
from lightrag.kg import JsonKVStorage, NetworkXStorage, NanoVectorDBStorage, JsonDocStatusStorage


async def create_prd_lightrag() -> LightRAG:
    """
    创建专门用于PRD分析的LightRAG实例
    
    Returns:
        LightRAG: 配置好的LightRAG实例
    """
    
    # 检查环境变量
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("请设置OPENAI_API_KEY环境变量")
    
    # 创建LightRAG实例，使用PRD专用配置
    rag = LightRAG(
        working_dir="./rag_storage_prd",
        workspace="prd_analysis",
        
        # 存储配置
        kv_storage="JsonKVStorage",
        graph_storage="NetworkXStorage", 
        vector_storage="NanoVectorDBStorage",
        doc_status_storage="JsonDocStatusStorage",
        
        # LLM配置
        llm_model_func=openai_alike_model_complete,
        llm_model_name="gpt-4o",
        llm_model_max_async=4,
        summary_max_tokens=15000,
        
        # 嵌入配置
        embedding_func=openai_embed,
        embedding_batch_num=16,
        embedding_func_max_async=12,
        
        # 文档处理配置
        chunk_token_size=1500,
        chunk_overlap_token_size=200,
        max_parallel_insert=3,
        entity_extract_max_gleaning=2,
        
        # 查询配置
        top_k=60,
        chunk_top_k=10,
        max_entity_tokens=15000,
        max_relation_tokens=15000,
        max_total_tokens=40000,
        cosine_better_than_threshold=0.2,
        
        # 缓存配置
        enable_llm_cache=True,
        enable_llm_cache_for_entity_extract=True,
        
        # PRD专用配置
        addon_params={
            "language": "中文",
            "entity_types": PROMPTS["PRD_ENTITY_TYPES"],  # 使用PRD专用实体类型
            "relationship_types": PROMPTS["PRD_RELATIONSHIP_TYPES"],  # 使用PRD专用关系类型
            "example_number": 1,  # 限制示例数量以减少LLM调用成本
        }
    )
    
    return rag


async def analyze_prd_document(rag: LightRAG, file_path: str) -> None:
    """
    分析PRD文档
    
    Args:
        rag: LightRAG实例
        file_path: 要分析的文档路径
    """
    
    print(f"开始分析PRD文档: {file_path}")
    
    try:
        # 初始化存储
        await rag.initialize_storages()
        
        # 处理文档
        print("正在处理文档...")
        result = await rag.insert_document(file_path)
        
        if result:
            print(f"文档处理成功！")
            print(f"提取的实体数量: {result.get('entities_count', 0)}")
            print(f"提取的关系数量: {result.get('relationships_count', 0)}")
            print(f"处理的文本块数量: {result.get('chunks_count', 0)}")
        else:
            print("文档处理失败")
            
    except Exception as e:
        print(f"文档处理过程中出现错误: {e}")
        raise


async def query_prd_knowledge(rag: LightRAG, query: str) -> None:
    """
    查询PRD知识库
    
    Args:
        rag: LightRAG实例
        query: 查询问题
    """
    
    print(f"\n查询问题: {query}")
    print("-" * 50)
    
    try:
        # 执行查询
        response = await rag.query(query)
        
        if response:
            print("查询结果:")
            print(response)
        else:
            print("未找到相关结果")
            
    except Exception as e:
        print(f"查询过程中出现错误: {e}")
        raise


async def explore_prd_graph(rag: LightRAG) -> None:
    """
    探索PRD知识图谱
    
    Args:
        rag: LightRAG实例
    """
    
    print("\n探索PRD知识图谱")
    print("-" * 50)
    
    try:
        # 获取图谱统计信息
        graph_stats = await rag.get_graph_statistics()
        
        if graph_stats:
            print("图谱统计信息:")
            print(f"实体数量: {graph_stats.get('nodes_count', 0)}")
            print(f"关系数量: {graph_stats.get('edges_count', 0)}")
            print(f"文本块数量: {graph_stats.get('chunks_count', 0)}")
            
            # 获取一些示例实体
            entities = await rag.get_entities(limit=5)
            if entities:
                print("\n示例实体:")
                for entity in entities:
                    print(f"- {entity.get('entity_name', 'Unknown')} ({entity.get('entity_type', 'Unknown')})")
                    
            # 获取一些示例关系
            relationships = await rag.get_relationships(limit=5)
            if relationships:
                print("\n示例关系:")
                for rel in relationships:
                    print(f"- {rel.get('src_id', 'Unknown')} -> {rel.get('tgt_id', 'Unknown')} ({rel.get('keywords', 'Unknown')})")
        else:
            print("无法获取图谱统计信息")
            
    except Exception as e:
        print(f"探索图谱过程中出现错误: {e}")
        raise


async def main():
    """
    主函数
    """
    
    print("LightRAG PRD文档分析示例")
    print("=" * 50)
    
    try:
        # 创建LightRAG实例
        print("正在创建LightRAG实例...")
        rag = await create_prd_lightrag()
        
        # 检查inputs目录
        inputs_dir = Path("./inputs")
        if not inputs_dir.exists():
            print("inputs目录不存在，请创建并放入PRD文档")
            return
            
        # 查找PRD文档
        prd_files = list(inputs_dir.glob("*.docx")) + list(inputs_dir.glob("*.pdf")) + list(inputs_dir.glob("*.txt"))
        
        if not prd_files:
            print("inputs目录中没有找到PRD文档，请放入.docx、.pdf或.txt文件")
            return
            
        print(f"找到 {len(prd_files)} 个文档文件")
        
        # 分析第一个文档
        first_file = prd_files[0]
        await analyze_prd_document(rag, str(first_file))
        
        # 探索知识图谱
        await explore_prd_graph(rag)
        
        # 示例查询
        example_queries = [
            "这个系统有哪些主要功能？",
            "用户注册流程包含哪些步骤？",
            "有哪些业务规则需要遵循？",
            "系统如何处理异常情况？",
            "不同用户角色有什么权限？"
        ]
        
        print("\n执行示例查询...")
        for query in example_queries:
            await query_prd_knowledge(rag, query)
            print("\n" + "="*50 + "\n")
            
    except Exception as e:
        print(f"程序执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 清理资源
        if 'rag' in locals():
            try:
                await rag.finalize_storages()
                print("已清理资源")
            except Exception as e:
                print(f"清理资源时出现错误: {e}")


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
