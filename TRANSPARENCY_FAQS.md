# AG2: Responsible AI FAQs

## What is AG2?
AG2 is a framework for simplifying the orchestration, optimization, and automation of LLM workflows. It offers customizable and conversable agents that leverage the strongest capabilities of the most advanced LLMs, like GPT-4, while addressing their limitations by integrating with humans and tools and having conversations between multiple agents via automated chat. AG2 is a spin-off of [AutoGen](https://github.com/microsoft/autogen) created by [a team consisting of AutoGen’s founders and contributors](https://github.com/ag2ai/ag2/blob/main/MAINTAINERS.md) of AutoGen.

## What can AG2 do?
AG2 is a framework for building a complex multi-agent conversation system by:
- Defining a set of agents with specialized capabilities and roles.
- Defining the interaction behavior between agents, i.e., what to reply with when an agent receives messages from another agent.

The agent conversation-centric design has numerous benefits, including that it:
-	Naturally handles ambiguity, feedback, progress, and collaboration.
-	Enables effective coding-related tasks, like tool use with back-and-forth troubleshooting.
-	Allows users to seamlessly opt in or opt out via an agent in the chat.
-	Achieves a collective goal with the cooperation of multiple specialists.

## 	What is/are AG2’s intended use(s)?
Please note that AG2 is an open-source library under active development and intended for  use for research purposes. It should not be used in any downstream applications without additional detailed evaluation of robustness, safety issues and assessment of any potential harm or bias in the proposed application.

AG2 is a generic infrastructure that can be used in multiple scenarios. The system’s intended uses include:

-	Building LLM workflows that solve more complex tasks: Users can create agents that interleave reasoning and tool use capabilities of the latest LLMs such as GPT-4o. To solve complex tasks, multiple agents can converse to work together (e.g., by partitioning a complex problem into simpler steps or by providing different viewpoints or perspectives).
-	Application-specific agent topologies: Users can create application specific agent topologies and patterns for agents to interact. The exact topology may depend on the domain’s complexity and semantic capabilities of the LLM available.
-	Code generation and execution: Users can implement agents that can assume the roles of writing code and other agents that can execute code. Agents can do this with varying levels of human involvement. Users can add more agents and program the conversations to enforce constraints on code and output.
-	Question answering: Users can create agents that can help answer questions using retrieval augmented generation.
-	End user and multi-agent chat and debate: Users can build chat applications where they converse with multiple agents at the same time.

While AG2 automates LLM workflows, decisions about how to use specific LLM outputs should always have a human in the loop. For example, you should not use AG2 to automatically post LLM generated content to social media.

## How was AG2 evaluated? What metrics are used to measure performance?
-	The current version of AG2 was evaluated on six applications to illustrate its potential in simplifying the development of high-performance multi-agent applications. These applications were selected based on their real-world relevance,  problem difficulty and problem solving capabilities enabled by AG2, and innovative potential.
-	These applications involve using AG2 to solve math problems, question answering, decision making in text world environments, supply chain optimization, etc. For each of these domains AG2 was evaluated on various success based metrics (i.e., how often the AG2 based implementation solved the task). And, in some cases, AG2 based approach was also evaluated on implementation efficiency (e.g., to track reductions in developer effort to build).
- The team has conducted tests where a “red” agent attempts to get the default AG2 assistant to break from its alignment and guardrails. The team has observed that out of 70 attempts to break guardrails, only 1 was successful in producing text that would have been flagged as problematic by Azure OpenAI filters. The team has not observed any evidence that AG2 (or GPT models as hosted by OpenAI or Azure) can produce novel code exploits or jailbreak prompts, since direct prompts to “be a hacker”, “write exploits”, or “produce a phishing email” are refused by existing filters.


## What are the limitations of AG2? How can users minimize the impact of AG2’s limitations when using the system?
AG2 relies on existing LLMs. Experimenting with AG2 retains the common limitations of large language models; including:

- Data Biases: Large language models, trained on extensive data, can inadvertently carry biases present in the source data. Consequently, the models may generate outputs that could be potentially biased or unfair.
-	Lack of Contextual Understanding: Despite their impressive capabilities in language understanding and generation, these models exhibit limited real-world understanding, resulting in potential inaccuracies or nonsensical responses.
-	Lack of Transparency: Due to the complexity and size, large language models can act as `black boxes,' making it difficult to comprehend the rationale behind specific outputs or decisions.
-	Content Harms: There are various types of content harms that large language models can cause. It is important to be aware of them when using these models, and to take actions to prevent them. It is recommended to leverage various content moderation services provided by different companies and institutions.
-	Inaccurate or ungrounded content: It is important to be aware and cautious not to entirely rely on a given language model for critical decisions or information that might have deep impact as it is not obvious how to prevent these models to fabricate content without high authority input sources.
-	Potential for Misuse: Without suitable safeguards, there is a risk that these models could be maliciously used for generating disinformation or harmful content.


Additionally, AG2's multi-agent framework may amplify or introduce additional risks, such as:
-	Privacy and Data Protection: The framework allows for human participation in conversations between agents. It is important to ensure that user data and conversations are protected and that developers use appropriate measures to safeguard privacy.
-	Accountability and Transparency: The framework involves multiple agents conversing and collaborating, it is important to establish clear accountability and transparency mechanisms. Users should be able to understand and trace the decision-making process of the agents involved in order to ensure accountability and address any potential issues or biases.
-	Trust and reliance: The framework leverages human understanding and intelligence while providing automation through conversations between agents. It is important to consider the impact of this interaction on user experience, trust, and reliance on AI systems. Clear communication and user education about the capabilities and limitations of the system will be essential.
-	Security & unintended consequences: The use of multi-agent conversations and automation in complex tasks may have unintended consequences. Especially, allowing LLM agents to make changes in external environments through code execution or function calls, such as installing packages, could pose significant risks. Developers should carefully consider the potential risks and ensure that appropriate safeguards are in place to prevent harm or negative outcomes, including keeping a human in the loop for decision making.

## What operational factors and settings allow for effective and responsible use of AG2?
-	Code execution: AG2 recommends using docker containers so that code execution can happen in a safer manner. Users can use function calls instead of free-form code to execute predefined functions only, increasing reliability and safety. Users can also tailor the code execution environment to their requirements.
-	Human involvement: AG2 prioritizes human involvement in multi agent conversation. The overseers can step in to give feedback to agents and steer them in the correct direction. Users can get a chance to confirm before code is executed.
-	Agent modularity: Modularity allows agents to have different levels of information access. Additional agents can assume roles that help keep other agents in check. For example, one can easily add a dedicated agent to play the role of a safeguard.
-	LLMs: Users can choose the LLM that is optimized for responsible use. For example, OpenAI's GPT-4o includes RAI mechanisms and filters. Caching is enabled by default to increase reliability and control cost. We encourage developers to review [OpenAI’s Usage policies](https://openai.com/policies/usage-policies) and [Azure OpenAI’s Code of Conduct](https://learn.microsoft.com/en-us/legal/cognitive-services/openai/code-of-conduct) when using their models.
-	Multi-agent setup: When using auto replies, the users can limit the number of auto replies, termination conditions etc. in the settings to increase reliability.
