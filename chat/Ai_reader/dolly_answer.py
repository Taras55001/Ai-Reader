from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import pickle
from pdf.models import UploadedFile


def gen_text(context: str, question: str) -> str:
    template = """Question: {question}

    Answer: Let's think step by step."""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    repo_id = "databricks/dolly-v2-3b"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
    )
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    res = llm_chain.run(f"{context}. {question}")
    return res


def answer(filename: UploadedFile, question: str) -> str:
    vector_store = pickle.load(filename.vector_db)

    context = vector_store.similarity_search(query=question, k=3)
    return gen_text(context, question)
