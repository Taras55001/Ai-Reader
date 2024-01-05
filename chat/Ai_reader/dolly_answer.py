from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from transformers.utils import logging
import pickle
from pdf.models import UploadedFile

logging.set_verbosity_error


def gen_text(context: str, question: str) -> str:
    # template = """
    # Question: {question}
    # Amswer: .......

    # """

    # prompt = PromptTemplate(template="", input_variables=["question"])
    repo_id = "databricks/dolly-v2-12b"
    llm = HuggingFaceHub(
        repo_id=repo_id,
        model_kwargs={"temperature": 0, "max_length": 455},
    )
    # llm_chain = LLMChain(prompt=prompt, llm=llm)
    # res = llm_chain.run(question=question)
    chain = load_qa_chain(llm, chain_type="stuff")
    res = chain.run(input_documents=context, question=question)
    return res


def answer(filename: UploadedFile, question: str) -> str:
    vector_store = pickle.load(filename.vector_db)

    context = vector_store.similarity_search(query=question, k=3)
    return gen_text(context, question)
