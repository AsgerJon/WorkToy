#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
import os
import openai


def generate_unit_tests(filename):
  # Read the Python file content
  with open(filename, 'r') as file:
    code = file.read()

  # Define the prompt for generating unit tests
  prompt = f"Write comprehensive unit tests for the following Python " \
           f"code:\n\n{code}"

  # Set up OpenAI API credentials
  openai.api_key = os.getenv('OPENAI_API_KEY')  # Replace with your OpenAI
  # API
  # key

  # Generate unit tests using OpenAI API
  response = openai.Completion.create(
    engine='davinci-codex',
    prompt=prompt,
    max_tokens=1000,
    temperature=0.7,
    n=1,
    stop=None,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )

  # Get the generated unit tests from the API response
  unit_tests = response.choices[0].text.strip()

  # Write the unit tests to a file
  unit_tests_filename = f"{filename.split('.')[0]}_tests.py"
  with open(unit_tests_filename, 'w') as file:
    file.write(unit_tests)

  return unit_tests_filename
