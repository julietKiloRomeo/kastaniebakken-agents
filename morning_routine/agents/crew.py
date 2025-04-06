from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from morning_routine.agents.tools.custom_tool import FITool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


# Initialize the tool
fi_tool = FITool()

@CrewBase
class MorningRoutine():
    """MorningRoutine crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def intra_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['intra_scraper'],
            tools=[fi_tool],
            verbose=True
        )

    @agent
    def schedule_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['schedule_reader'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def todo_task(self) -> Task:
        return Task(
            config=self.tasks_config['todo_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the MorningRoutine crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            verbose=True,
            manager_llm="gpt-4o",  # Specify which LLM the manager should use
            process=Process.hierarchical,  
            max_iterations=5,
            planning=True, 
        )
