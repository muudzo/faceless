import pytest
from src.generators.script_gen import ScriptGenerator

def test_script_generation():
    gen = ScriptGenerator(max_length=100)
    title = "Mars"
    explanation = "The Red Planet is cold and dusty."
    script = gen.generate_short_script(title, explanation)
    
    assert "Mars" in script
    assert "Subscribe" in script
    assert len(script) > 50

def test_script_cleaning():
    gen = ScriptGenerator()
    text = "Hello (extra info) world."
    script = gen.generate_short_script("Test", text)
    assert "(extra info)" not in script
