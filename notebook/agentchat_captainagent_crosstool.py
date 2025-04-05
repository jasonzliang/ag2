# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] vscode={"languageId": "plaintext"}
# # Cross-Framework LLM Tool for CaptainAgent
# In this tutorial, we demonstrate how to integrate LLM tools from [LangChain Tools](https://python.langchain.com/v0.1/docs/modules/tools), [CrewAI Tools](https://github.com/crewAIInc/crewAI-tools/tree/main) into CaptainAgent. The developers just need to use one line of code to convert them into [AG2 tools](https://docs.ag2.ai/docs/use-cases/notebooks/notebooks/tools_interoperability), and then pass it to CaptainAgent while instantiation, simple as that.

# %% [markdown]
# ## Langchain Tool Integration
# Langchain readily provides a number of tools at hand. These tools can be integrated into AG2 framework through interoperability.
#
# ### Installation
# To integrate LangChain tools into the AG2 framework, install the required dependencies:
#
# ```bash
# pip install -U ag2[openai,interop-langchain]
# ```
#
# > **Note:** If you have been using `autogen` or `pyautogen`, all you need to do is upgrade it using:  
# > ```bash
# > pip install -U autogen[openai,interop-langchain]
# > ```
# > or  
# > ```bash
# > pip install -U pyautogen[openai,interop-langchain]
# > ```
# > as `pyautogen`, `autogen`, and `ag2` are aliases for the same PyPI package.  
#
#
# Additionally, this notebook uses LangChain's [DuckDuckGo Search Tool](https://python.langchain.com/docs/integrations/tools/ddg/), which requires the `duckduckgo-search` package. Install it with:
#
# ```bash
# pip install duckduckgo-search
# ```
#
# ### Preparation
# Import necessary modules and tools.
# - [DuckDuckGoSearchRun](https://python.langchain.com/api_reference/community/tools/langchain_community.tools.ddg_search.tool.DuckDuckGoSearchRun.html) and [DuckDuckGoSearchAPIWrapper](https://python.langchain.com/api_reference/community/utilities/langchain_community.utilities.duckduckgo_search.DuckDuckGoSearchAPIWrapper.html#langchain_community.utilities.duckduckgo_search.DuckDuckGoSearchAPIWrapper): Tools for querying DuckDuckGo.
# - `Interoperability`: This module acts as a bridge, making it easier to integrate LangChain tools with AG2’s architecture.

# %%
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from autogen.interop import Interoperability

# %% [markdown]
# ### Configure the agents
# Load the config for LLM, which include API key and model.

# %%
import autogen

config_path = "OAI_CONFIG_LIST"
llm_config = autogen.LLMConfig.from_json(path=config_path, temperature=0).where(model=["gpt-4o"])

# %% [markdown]
# ### Tool Integration
# We use `Interoperability` to convert the LangChain tool into a format compatible with the AG2 framework.

# %%
interop = Interoperability()

api_wrapper = DuckDuckGoSearchAPIWrapper()
langchain_tool = DuckDuckGoSearchRun(api_wrapper=api_wrapper)
ag2_tool = interop.convert_tool(tool=langchain_tool, type="langchain")

# %% [markdown]
# Then add the tools to CaptainAgent, the main difference from original CaptainAgent initialization is to pass the tool as a list into the `tool_lib` argument. This will let the agents within the nested chat created by CaptainAgent all equipped with the tools. THey can write python code to call the tools and observe the results.

# %%
from autogen import UserProxyAgent
from autogen.agentchat.contrib.captainagent import CaptainAgent

# build agents
captain_agent = CaptainAgent(
    name="captain_agent",
    llm_config=llm_config,
    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
    agent_lib="captainagent_expert_library.json",
    tool_lib=[ag2_tool],  # The main difference lies here: we pass the converted tool to the agent
    agent_config_save_path=None,
)
captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER")

# %%
res = captain_user_proxy.initiate_chat(
    captain_agent,
    message="Call a group of experts and search for the word of the day Merriham Webster December 26, 2024",
)

# %% [markdown]
# ## CrewAI Tool Integration
# CrewAI also provides a variety of powerful tools designed for tasks such as web scraping, search, code interpretation, and more. The full list of available tools in CrewAI can be observed [here](https://github.com/crewAIInc/crewAI-tools/tree/main).
#
# ### Installation
# Install the required packages for integrating CrewAI tools into the AG2 framework.
# This ensures all dependencies for both frameworks are installed.
#
# ```bash
# pip install -U ag2[openai,interop-crewai]
# ```
#
# > **Note:** If you have been using `autogen` or `pyautogen`, all you need to do is upgrade it using:  
# > ```bash
# > pip install -U autogen[openai,interop-crewai]
# > ```
# > or  
# > ```bash
# > pip install -U pyautogen[openai,interop-crewai]
# > ```
# > as `pyautogen`, `autogen`, and `ag2` are aliases for the same PyPI package.  
#
# ### Tool Integration
# Integrating CrewAI tools into AG2 framework follows a similar pipeline as shown below.

# %%
from crewai_tools import ScrapeWebsiteTool

from autogen.interop import Interoperability

interop = Interoperability()
crewai_tool = ScrapeWebsiteTool()
ag2_tool = interop.convert_tool(tool=crewai_tool, type="crewai")

# %% [markdown]
# ### Adding tools to CaptainAgent
# The process is identical to the above, pass the converted tool to `tool_lib` argument, and all the agents created by CaptainAgent gets access to the tools.

# %%
from autogen import UserProxyAgent
from autogen.agentchat.contrib.captainagent import CaptainAgent

# build agents
captain_agent = CaptainAgent(
    name="captain_agent",
    llm_config=llm_config,
    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
    agent_lib="captainagent_expert_library.json",
    tool_lib=[ag2_tool],
    agent_config_save_path=None,  # If you'd like to save the created agents in nested chat for further use, specify the save directory here
)
captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER")

# %%
message = "Call experts and Scrape the website https://ag2.ai/, analyze the content and summarize it"
result = captain_user_proxy.initiate_chat(captain_agent, message=message)

# %%
print(result.summary)
