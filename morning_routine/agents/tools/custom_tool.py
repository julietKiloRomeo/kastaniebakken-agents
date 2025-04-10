from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from morning_routine import scraper

class FIToolInput(BaseModel):
    """Input schema for FICustomTool."""
    argument: str = Field(..., description="the name of the student to find the schedule for") # this is a lie :)

class FITool(BaseTool):
    name: str = "Intra tool"
    description: str = (
        "Read the weekly schedule from forældreintra"
    )
    args_schema: Type[BaseModel] = FIToolInput

    def _run(self, argument: str) -> str:
        # Implementation goes here
        return scraper.read_the_schedule()

class FileWriterInput(BaseModel):
    """Input schema for FICustomTool."""
    rel_path: str = Field(description="the relative path of the file to write.")
    content: str = Field(description="the content to write to the file using f.write()")

import pathlib

class FileWriter(BaseTool):
    name: str = "File writer tool"
    description: str = (
        "Write text to a file using f.write(content)"
    )
    args_schema: Type[BaseModel] = FileWriterInput

    def _run(self, rel_path: str, content: str) -> str:
        # Ensure the output directory exists
        output_dir = pathlib.Path("crew_output")
        output_dir.mkdir(exist_ok=True)
        
        # Get the full path
        path = output_dir / rel_path
        
        # Ensure parent directories exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # If file exists, generate a unique filename
        if path.exists():
            # Split filename and extension
            stem = path.stem
            suffix = path.suffix
            parent = path.parent
            
            # Try numbered suffixes until we find an available filename
            counter = 1
            while path.exists():
                new_filename = f"{stem}-{counter:03d}{suffix}"
                path = parent / new_filename
                counter += 1
        
        # Write content to the file
        with path.open("w") as f:
            f.write(content)
            
        return str(path)
