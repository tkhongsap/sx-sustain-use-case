from typing import List
from pydantic import BaseModel, Field

class PromptListTool:
    class Valves(BaseModel):
        priority: int = Field(default=20, description="Priority level for tool execution.")
    
    class UserValves(BaseModel):
        max_prompts: int = Field(default=10, description="Maximum number of prompts to display.")
    
    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()

        self.prompts = [
            "/economic-growth-and-expansion - Economic Growth and Expansion",
            "/environmental-milestones - Environmental Milestones",
            "/foundation-and-early-development - Foundation and Early Development",
            "/thaibev-history-article - Article on ThaiBev's History",
            "/community-commitment-deep-dive - Community Commitment Deep Dive",
            "/governance-and-ethical-business-practices - Governance and Ethical Business Practices",
            "/innovation-and-future-goals - Innovation and Future Goals",
            "/introduction-of-sustainability-initiatives - Introduction of Sustainability Initiatives",
        ]
    
    async def run(self, __user__: dict = {}, __event_emitter__=None) -> str:
        """
        This tool returns a list of predefined prompts available for users.
        It supports configurable priority and max number of prompts via valves.

        :param __user__: Dictionary containing user details
        :param __event_emitter__: Event emitter to send status or messages to the chat
        :return: String containing the list of predefined prompt descriptions
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status", 
                    "data": {"description": "Fetching the list of prompts...", "done": False}
                }
            )

        max_prompts = self.user_valves.max_prompts
        prompt_list = self.prompts[:max_prompts]

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status", 
                    "data": {"description": "Prompt list fetched.", "done": True}
                }
            )

        result = "Available prompts:\n" + "\n".join(prompt_list)

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "message", 
                    "data": {"content": result}
                }
            )

        return result

class Tools:
    prompt_list = PromptListTool()