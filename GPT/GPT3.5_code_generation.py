import openai
import math
import os
import sys
import csv
from tqdm import tqdm  

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def compute_normalized_probability(logprobs, length):
    joint_logprob = sum(logprobs)
    normalized_logprob = joint_logprob / length if length > 0 else joint_logprob
    return (math.exp(normalized_logprob),joint_logprob)

def query_openai(prompt, max_responses=5, max_tokens=2000):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,
        n=max_responses,
        logprobs=5
    )
    return response

def process_responses(response):
    results = []
    for choice in response['choices']:
        tokens = choice['logprobs']['tokens']
        token_logprobs = choice['logprobs']['token_logprobs']
        length = len(tokens)
        (normalized_prob,logprob) = compute_normalized_probability(token_logprobs, length)
        results.append({
            "response": choice['text'],
            "normalized_probability": normalized_prob,
            "logprob": logprob
        })
    return results

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_folder_path> <output_folder_path>")
        sys.exit(1)

    input_folder_path = sys.argv[1]
    output_folder_path = sys.argv[2]

    if not os.path.isdir(input_folder_path):
        print(f"Error: {input_folder_path} is not a valid directory.")
        sys.exit(1)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Collect all relevant files first
    problem_files = [
        f for f in os.listdir(input_folder_path) 
        if f.startswith("problem_") and f.endswith(".txt")
    ]

    # Use tqdm to show progress over the files
    for filename in tqdm(problem_files, desc="Processing problems", unit="file"):
        problem_id = filename[len("problem_"):-len(".txt")]
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, f"solution_{problem_id}.csv")

        with open(input_file_path, "r", encoding="utf-8") as file:
            coding_problem = file.read()

        # Query OpenAI
        # (You can comment out print statements if you just want the progress bar.)
        print(f"Querying OpenAI API for {filename}...")
        openai_response = query_openai(
            coding_problem + ". Please provide the solution as a Python function named solve() and omit any code comments in the solution."
        )

        # Process responses
        print(f"Processing responses for {filename}...")
        processed_results = process_responses(openai_response)

        # Write results to a CSV file
        with open(output_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            # Write header row
            writer.writerow(["id", "response_number", "response", "prob", "logprob"])
            
            for i, result in enumerate(processed_results, start=1):
                writer.writerow([
                    problem_id,
                    i,
                    result["response"],
                    f"{result['normalized_probability']:.4f}",
                    result["logprob"]
                ])

    print(f"All results written to {output_folder_path}")
