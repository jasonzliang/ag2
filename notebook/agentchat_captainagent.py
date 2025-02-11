#!/usr/bin/env python
# coding: utf-8

# # CaptainAgent
# By: Jiale Liu, Linxin Song, Jieyu Zhang, Shaokun Zhang
# 
# In this notebook, we introduce CaptainAgent, an agent enhanced with the capability to call AutoBuild to break down and solve complex tasks. AutoBuild can initiate a group chat between a group of experts and converse to solve the task. The experts in nested chat can be retrieved from agent library. The agents can be equipped with tools for advanced coding.
# 
# ````{=mdx}
# :::info Requirements
# Install `ag2` with CaptainAgent:
# ```bash
# pip install ag2[captainagent]
# ```
# 
# For more information, please refer to the [installation guide](/docs/installation/Installation).
# :::
# ````

# ## Setup API endpoint
# In order to setup API, you should create a OAI_CONFIG_LIST file. The config list should look like the following:
# ```python
# config_list = [
#     {
#         'model': 'gpt-4o-mini',
#         'api_key': '<your OpenAI API key here>',
#     },
#     {
#         'model': 'gpt-3.5-turbo',
#         'api_key': '<your Azure OpenAI API key here>',
#         'base_url': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-08-01-preview',
#     },
#     {
#         'model': 'gpt-3.5-turbo-16k',
#         'api_key': '<your Azure OpenAI API key here>',
#         'base_url': '<your Azure OpenAI API base here>',
#         'api_type': 'azure',
#         'api_version': '2024-08-01-preview',
#     },
# ]
# ```
# 
# ````{=mdx}
# :::tip
# Learn more about configuring LLMs for agents [here](/docs/topics/llm_configuration).
# :::
# ````

# In[1]:


import autogen

config_path = "OAI_CONFIG_LIST"
config_list = autogen.config_list_from_json(
    config_path, filter_dict={"model": ["gpt-4o"]}
)  # You can modify the filter_dict to select your model


# ## Using CaptainAgent without libraries
# We begin with demonstrating how to use CaptainAgent without retrieving from libaries. In this case, CaptainAgent will automatically generate a set of experts according to its identified subtask and initate the group chat. By default, the backbone of the LLM is set to `gpt-4o`. For instructions on configuring the backbone, refer to docs on [`nested_mode`](https://docs.ag2.ai/docs/topics/captainagent/configurations).

# In[2]:


from autogen import UserProxyAgent
from autogen.agentchat.contrib.captainagent import CaptainAgent

llm_config = {"temperature": 0, "config_list": config_list}

## build agents
captain_agent = CaptainAgent(
    name="captain_agent",
    llm_config=llm_config,
    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
    agent_config_save_path=None,  # If you'd like to save the created agents in nested chat for further use, specify the save directory here
)
captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER")


# In[3]:


result = captain_user_proxy.initiate_chat(
    captain_agent,
    message="Find a recent paper about large language models on arxiv and find its potential applications in software.",
    max_turns=1,
)


# ## Building Agents from library & Retrieve tools from tool library
# One significant feature of CaptainAgent is that the agents and tools can be retrieved from a dedicated library. When CaptainAgent starts building experts for group chat, it will retrieve and select from agent library, then assign tools retreived from tool library to the experts.
# 
# For agent library, refer to [`captainagent_expert_library.json`](https://github.com/ag2ai/ag2/blob/main/notebook/captainagent_expert_library.json) for samples. You can refer to [docs](https://docs.ag2.ai/docs/topics/captainagent/agent_library) on how to customize your own expert library.
# 
# For tool library, we provide a set of tools [here](https://github.com/ag2ai/ag2/tree/main/autogen/agentchat/contrib/captainagent/tools/README.md), the tools are categorized into three types: data analysis, information_retrieval, math. If you are using the tools, you should [install the requirements](https://github.com/ag2ai/ag2/tree/main/autogen/agentchat/contrib/captainagent/tools/README.md#how-to-use) for them.

# ### Using Agent Library Only
# Below is an example that retrieves experts from library and build nested chat accordingly.
# 

# In[5]:


from autogen import UserProxyAgent
from autogen.agentchat.contrib.captainagent import CaptainAgent

# build agents
captain_agent = CaptainAgent(
    name="captain_agent",
    llm_config=llm_config,
    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
    agent_lib="captainagent_expert_library.json",
    agent_config_save_path=None,  # If you'd like to save the created agents in nested chat for further use, specify the save directory here
)
captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER")

query = "find papers on LLM applications from arxiv in the last week, create a markdown table of different domains. After collecting the data, point out future research directions in light of the collected data."

result = captain_user_proxy.initiate_chat(captain_agent, message=query)


# ## Using Both Agent Library and Tool Library
# Now let's retrieve from both agent library and tool library while building experts for nested chat.
# 
# To run the following demo, it is required to install the dependencies from the tool library and obtain BING search api and Rapid API key for tools in library to fully function. Please follow the instructions [here](https://docs.ag2.ai/docs/topics/captainagent/tool_library).

# In[ ]:


# The function requires BING api key and Rapid API key to work. You can follow the instructions from docs to get one.
import os

from autogen import UserProxyAgent
from autogen.agentchat.contrib.captainagent import CaptainAgent

os.environ["BING_API_key"] = ""  # set your bing api key here, if you donot need search engine, you can skip this step
os.environ["RAPID_API_KEY"] = (
    ""  # set your rapid api key here, in order for this example to work, you need to subscribe to the youtube transcription api(https://rapidapi.com/solid-api-solid-api-default/api/youtube-transcript3)
)

## build agents
captain_agent = CaptainAgent(
    name="captain_agent",
    llm_config=llm_config,
    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
    agent_lib="captainagent_expert_library.json",
    tool_lib="default",
    agent_config_save_path=None,  # If you'd like to save the created agents in nested chat for further use, specify the save directory here
)
captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER")

query = """# Task
Your task is to solve a question given by a user.

# Question
Examine the video at https://www.youtube.com/watch?v=1htKBjuUWec.

What does Teal'c say in response to the question "Isn't that hot?"
""".strip()
result = captain_user_proxy.initiate_chat(captain_agent, message=query)


# The ground truth answer to the question is 'Extremely', which the CaptainAgent answers correctly. Notably, with the assistance of tools, the agent can answer video-related questions. This shows the huge potential of what user customized tools can bring.

# # Further Reading
# For a full list of the configurables and the functionalities in CaptainAgent, please refer [here](https://docs.ag2.ai/docs/topics/captainagent/configurations).
# 
# For how to customize your own agent library, check [here](https://docs.ag2.ai/docs/topics/captainagent/agent_library).
# 
# For how to implement your own tool library that suits your need, check the documents [here](https://docs.ag2.ai/docs/topics/captainagent/tool_library).
# 
