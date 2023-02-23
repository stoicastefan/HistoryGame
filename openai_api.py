import openai


class OpenaiApi:
    def __init__(self):
        pass

    def request_answer_openai(self, prompt, temperature, tokens):
        openai.api_key = "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"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=tokens,
            best_of=1
        )

        return response.choices[0].text.strip()

    def get_a_list_of_answers(self, prompt, temperature, tokens):
        response_as_top = self.request_answer_openai(prompt, temperature, tokens)

        list_of_answers = response_as_top.split("\n")

        return list_of_answers
