# COMSM3201-MSc-Project-Computer-Science



## Assessing Correctness in LLM-Based Code Generation



### Abstract

The objective of this project is to assess the correctness of Large Language Models (LLMs) in code generation tasks. Tools other than unit testing will be utilised to provide a method that can be integrated into existing LLM workflows. The implementation will use entropy as a metric to identify the level of uncertainty of a given set of responses. Symbolic clustering will be implemented to group responses according to their meaning. After the entropy of the grouped responses is computed, this project will aim to identify a correlation between a high uncertainty and incorrect responses. Therefore, the LLM's responses will be verified against the correctness revealed by unit tests to determine the validity of low entropy as an indicator of correctness. This project will distinguish itself from existing research by clustering responses based on semantic equivalence using another language model, rather than implementing symbolic execution.



### Introduction

The key objective of this project is to assess the correctness of LLM responses by separating them based on semantic equivalence, using entropy as a measure of uncertainty. I hypothesise that entropy level will be a strong indicator of uncertainty, and therefore, incorrectness of the LLM’s responses. This is due to previous research that demonstrates this correlation with the alternative response clustering method of symbolic execution (David & Sharma, 2025, p. 1). Therefore, this project must retain this result while employing a different implementation. The outcome of this will be important in confirming the value of clustering for semantic equivalence and the overall merit of entropy as an indicator of incorrectness. Another challenge is in using natural language generation techniques in a way that accurately determines the correctness of the LLM’s code generation responses. Code generation introduces new difficulties, particularly in checking for semantic equivalence (David & Sharma, 2025, p. 2). This research can be used as basis to integrate tools into LLMs that estimate the correctness of LLM responses and therefore avoid generating responses that are associated with a high level of entropy. I will verify my results with unit testing to ensure that there is a strong correlation between my hypothesis and the actual correctness of the LLM.



### Related work 

Previous research has implemented a Neuro-symbolic tool and found that it offered an effective alternative to scaling model size (Princis, David, & Mycroft, 2025, p. 10). This research found that their ‘Xander’ tool outperformed its 4 times larger counterpart in SQL query generation (Princis, David, & Mycroft, 2025, p. 1). It also found that symbolic approaches can be more accurate at detecting errors in queries than neural approaches (Princis, David, & Mycroft, 2025, p. 7). 

Farquhar et al. proposed entropy as a marker for uncertainty to detect hallucinations in LLM natural language generation by detecting when prompts are most likely to produce confabulations (Farquhar et al, 2024). This research also considered semantic equivalence by computing uncertainty at the level of meaning (Farquhar et al, 2024).

This project will build on the contribution of the paper “Assessing correctness in LLM-based code generation via uncertainty estimation”, in being the first to explore estimating the uncertainty of LLM-based code generation to assess correctness (David & Sharma, 2025, p. 3). It adapted techniques from natural language generation research to find a strong negative correlation between uncertainty and correctness (David & Sharma, 2025, p. 18). This paper uses symbolic execution, meaning that symbolic variables are used to represent inputs, generating constraints that describe program behaviour (David & Sharma, 2025, p. 5). Therefore, this project's implementation will differ from this method by using a second language model to group responses into semantically equivalent cluster.



### Project Timeline

| Task | Approximate Timeline |
|------|-----------------------|
| Background reading and repository creation/management | 3rd June – 10th June (1 week) |
| Running LLM and API on code generation dataset | 11th June – 18th June (1 week) |
| Implementing symbolic clustering | 19th June – 9th July (3 weeks) |
| Computing uncertainty | 10th July – 23rd July (2 weeks) |
| Evaluation (compare entropy and correctness) | 24th July – 30th July (1 week) |
| Collect statistics and presentation | 31st July – 6th August (1 week) |
| Refinement and write-up | 7th August – 28th August (3 weeks) |



### Implementation

For the implementation of the project, the GPT 3.5 API will be run to gather responses to a set of code generation tasks. The next step will be to implement symbolic clustering, grouping responses according to their meaning, rather than their syntax. These clusters will be determined by running a Llama 3.2 model, a smaller language model that will be prompted with the initial sets of responses. Once these clusters are obtained, their entropy will be computed to allow for evaluation on the correctness of the GPT LLM.



### Evaluation

The evaluation will utilise unit testing to act as a verification of my results and reaffirm high entropy as a strong indicator of incorrectness. If my hypothesis holds, I will demonstrate a statistical correlation between the correctness estimated by the level of entropy and the actual correctness revealed by unit testing. I plan to cross-check the levels of entropy with the results from unit testing to observe their correlation. This could lead to a further evaluation of the value in grouping responses by semantic equivalence. A possible limitation of this approach is that a response could display a high level of entropy and unit testing can fail due to different issues with the response. Therefore, it is important that both sets of results are analysed carefully and the specific reasons for failed unit tests are identified, to mitigate this.



### References

Princis, H., David, C., & Mycroft, A. (2025). Enhancing SQL query generation with neurosymbolic reasoning. Proceedings of the AAAI Conference on Artificial Intelligence, 39(19), 19959–19968. https://doi.org/10.1609/aaai.v39i19.34198

Sharma, A., & David, C. (2025). Assessing correctness in LLM-based code generation via uncertainty estimation (arXiv:2502.11620) [Preprint]. https://doi.org/10.48550/arXiv.2502.11620

Farquhar, S., Kossen, J., Kuhn, L., et al. (2024). Detecting hallucinations in large language models using semantic entropy. Nature, 630(8015), 625–630. https://doi.org/10.1038/s41586-024-07421-0



