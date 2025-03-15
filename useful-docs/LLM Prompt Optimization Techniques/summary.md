# Optimizing LLM Prompts for Adherence & Clarity (Summary)

## Additional Docs

- [Automatic Prompt Optimization with “Gradient Descent”
and Beam Search by MS Azure AI team](https://arxiv.org/pdf/2305.03495)

- [Prompt engineering techniques - repo by NirDiamant](https://github.com/NirDiamant/Prompt_Engineering/tree/main/all_prompt_engineering_techniques)

## Structure for Clear Instructions
- Start with clear, prioritized instructions upfront, using clear delimiters (`### Instructions`, `### Content`).
- Define a clear role or persona for the model (e.g., *“You are an expert educational architect”*).
- Use mandatory language (e.g., **must**, **ensure**), and phrase instructions positively (state what to do, rather than just what not to).

## Reducing Ambiguity & Maintaining Flexibility
- Be detailed and explicit (e.g., specify desired formats and structures clearly).
- Define ambiguous terms explicitly (e.g., specify hours as weekly or daily clearly).
- Avoid over-constraining; balance structure with some flexibility for creativity.
- Optionally, give concise examples showing the desired specificity-flexibility balance.

## Effectively Enforce Rules & Guidelines
- Present requirements as checklists or numbered points for easier compliance.
- Use visual emphasis (e.g., bold, ALL CAPS, or icons) for critical rules.
- Provide format examples or schema templates directly within the prompt.
- State prohibitions positively by clearly instructing the correct alternative behavior.

## Enhance Multi-step Execution Reliability
- Break down prompts into clearly enumerated sub-steps for focused execution.
- Encourage explicit step-by-step reasoning or calculation (e.g., "show calculations clearly as comments").
- Utilize scaffolded multi-turn prompts (outline first, then details).
- Clearly prompt final self-verification checks explicitly, ensuring step adherence and accuracy.

## Ensuring Consistent Outputs Across Different LLMs
- Use universally understood formats (JSON, Markdown) for clarity across LLMs.
- Include brief output examples to guide consistent formatting.
- Simplify language to a clear, universal understanding level, avoiding idioms or complexities.
- Control generation randomness (use low-temperature settings, fixed seeds if possible).
- Iteratively test prompts across different LLMs, refining wording based on actual responses.