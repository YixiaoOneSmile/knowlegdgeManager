from llama_index.readers.web import SimpleWebPageReader
from llama_index.llms.ollama import Ollama
from llama_index.core import SummaryIndex

llm = Ollama(model="qwen2.5:32b",base_url="http://175.146.122.49:8083")

# Step 1: Load HTML data from the web
reader = SimpleWebPageReader(html_to_text=True)
documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://developer.aliyun.com/article/1357654"]
)
print(documents[0])
# 创建索引
index = SummaryIndex.from_documents(documents)

# 设置日志等级为DEBUG以获取更详细的输出
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query("总结一下?")
print(response)
