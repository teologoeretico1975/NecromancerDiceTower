#!/usr/bin/env python3
"""
Agent 02: Technical Papercraft Engineer

Generates a technical specification for the Necromancer Dice Tower
using Claude Sonnet 4 and the project state as context.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic


def load_project_state() -> str:
    """Read the project state file as context."""
    project_state_path = Path("00_Project_Control/project_state.md")
    if not project_state_path.exists():
        raise FileNotFoundError(f"Project state file not found: {project_state_path}")
    
    with open(project_state_path, "r", encoding="utf-8") as f:
        return f.read()


def generate_technical_specification(project_state: str) -> str:
    """
    Call Claude Sonnet 4 to generate a technical specification.
    
    Args:
        project_state: The project state content as context
        
    Returns:
        The generated technical specification
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key) if hasattr(anthropic, 'Anthropic') else anthropic.Client(api_key=api_key)

    system_prompt = (
        "You are a technical papercraft engineer. Use the project state provided as "
        "source of truth. Do not contradict its technical and commercial constraints."
    )
    
    user_message = f"""Based on the following project state, generate a comprehensive 
technical specification for the Necromancer Dice Tower printable papercraft PDF kit.

The specification should include:
- Overall tower dimensions and structure
- Detailed component breakdown (body pieces, ramps, base/tray)
- Paper requirements and cutting specifications
- Fold and glue instructions and locations
- Assembly sequence and build order
- Dice entry size and exit positions
- Page layout strategy (how many A4 sheets needed)
- Cut/fold/glue legend requirements
- Scale check square placement
- Quality assurance checkpoints

PROJECT STATE:
{project_state}

Generate the specification in Markdown format, ready to be saved directly as a 
technical specification document."""
    
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    fallback_model = os.getenv("ANTHROPIC_MODEL_FALLBACK", "claude-2.1")

    def call_model(m: str):
        return client.messages.create(
            model=m,
            max_tokens=4000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )

    try:
        message = call_model(model)
    except Exception as e:
        # If model not found, try to obtain a valid model from the API and retry
        err = str(e)
        if "not_found" in err or "model" in err or getattr(e, "status_code", None) == 404:
            try:
                models_page = client.models.list()
                first_model = None
                for m in models_page:
                    # ModelInfo may expose 'id' or 'name'
                    first_model = getattr(m, 'id', None) or getattr(m, 'name', None) or str(m)
                    if first_model:
                        break
                if not first_model:
                    first_model = fallback_model
            except Exception:
                first_model = fallback_model

            message = call_model(first_model)
        else:
            raise

    # support multiple response shapes; prefer text
    try:
        return message.content[0].text
    except Exception:
        # fallback if response shape differs
        return getattr(message, 'text', str(message))


def save_specification(content: str, output_path: str) -> None:
    """
    Save the technical specification to a file.
    
    Args:
        content: The specification content
        output_path: Path to save the file to
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)


def main() -> None:
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not found in .env file")
        sys.exit(1)
    
    print("Agent 02: Technical Papercraft Engineer")
    print("=" * 50)
    print()
    
    try:
        print("📖 Loading project state...")
        project_state = load_project_state()
        print(f"   Project state loaded ({len(project_state)} characters)")
        print()
        
        print("🤖 Calling Claude Sonnet 4 to generate technical specification...")
        specification = generate_technical_specification(project_state)
        print(f"   Specification generated ({len(specification)} characters)")
        print()
        
        print("💾 Saving specification to file...")
        output_path = "01_Technical_Template/specs/technical_spec_v001.md"
        save_specification(specification, output_path)
        print(f"   ✅ Saved to: {output_path}")
        print()
        
        print("=" * 50)
        print("✨ Technical specification generation complete!")
        print(f"   Output: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except anthropic.APIError as e:
        print(f"Error calling Anthropic API: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
