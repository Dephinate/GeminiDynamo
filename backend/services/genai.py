import tqdm
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_vertexai import VertexAI
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from vertexai.generative_models import GenerativeModel
import json


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiProcessor:
    def __init__(self,model_name, project) -> None:
        self.model = VertexAI(model_name=model_name, temperature=0, project=project)
        self.project = project

    def generate_document_summary(self,documents, **args):
        chain_type = "map_reduce" if len(documents)>10 else "stuff"
        chain = load_summarize_chain(llm=self.model,chain_type=chain_type,**args)
        return chain.run(documents)
    
    def count_total_tokens(self, docs: list):
        temp_model = GenerativeModel(model_name="gemini-1.0-pro")
        total = 0
        for doc in tqdm.tqdm(docs):
            total += temp_model.count_tokens(doc.page_content).total_billable_characters
        return total
    
    def get_model(self):
        return self.model
    


class YoutubeProcessor:
    def __init__(self, genai_processor: GeminiProcessor):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 0
        )
        self.genai_processor = genai_processor

    def retrieve_youtube_documents(self, video_url: str,verbose = False):
        loader = YoutubeLoader.from_youtube_url(video_url,**{"add_video_info":True})
        docs = loader.load()
        print("Docs:",len(docs))
        chunks = self.text_splitter.split_documents(docs)

        author = chunks[0].metadata["author"]
        title = chunks[0].metadata["title"]
        length = chunks[0].metadata["length"]
        total_size = len(chunks)


        if verbose:
            total_billable_characters= self.genai_processor.count_total_tokens(chunks)
            logger.info(f"author: {author}\ntitle: {title}\nlength: {length}\ntotal_length: {total_size}\ntotal_billable_characters: {total_billable_characters}")

        return chunks
    
    def find_key_concepts(self, documents: list, sample_size:int = 2, verbose = False):
        # Divide the docs into groups
        num_of_docs = len(documents)

        if sample_size > num_of_docs:
            raise ValueError("Group size is larger than the number of documents")
        
        # If sample size not specified, set default to 5. 
        if sample_size == 0:
            sample_size = 5
            logger.info(f"No sample size specified. Setttig default sample to 5. Sample size: {sample_size}")
        # Number of groups to be formed or in how many parts will the document list be divided

        # If less than 5 documents and no sample size specified then there will be only one group
        if sample_size > num_of_docs:
            groups = [documents]
        else:
            number_of_groups = num_of_docs // sample_size + (num_of_docs % sample_size > 0)
            groups = [documents[i:i+number_of_groups] for i in range (0, num_of_docs ,number_of_groups)]

        if len(groups[0]) >10:
            raise ValueError(f"Each group has {len(groups[0])} documents, which is more than 10, output quality will be degraded significantly. Increase the sample_size parameter to reduce the number of documents per group.")
        if len(groups[0]) >5:
            logger.warning("Each group has more than 5 documents and output quality is likely to be degraded. Consider increasing the sample size.")


        # extract key points from each group
        batch_concepts = []
        batch_cost = 0

        logger.info(f"Finding key concepts....")

        for group in tqdm.tqdm(groups):
            group_content = ""
            group_content = (",").join([doc.page_content for doc in group])
            prompt = PromptTemplate(
            template="""
            Find and define key concepts or terms found in the text. 
            Respond in the following format as a JSON object without any backticks, separating each concept with a comma:
            {{"concept": "definition", "concept": "definition", ...}}:
            
            {text}
            """,
            input_variables=["text"]
            )

            # Create chain
            chain = prompt | self.genai_processor.model
            output_concept = chain.invoke({"text":group_content})
            batch_concepts.append(output_concept)

            # Analyse cost
            if verbose == True:
                group_input_char = len(group_content)
                group_input_cost = (len(group_content)/100) * 0.000125

                logger.info(f"Running chain on {len(group)} documents")
                logger.info(f"Total input characters: {group_input_char}")
                logger.info(f"Total input cost: {group_input_cost}")

                group_output_char = len(output_concept)
                group_output_cost = (len(output_concept)/100) * 0.000125

                logger.info(f"Total output characters: {group_output_char}")
                logger.info(f"Total output cost: {group_output_cost}")

                batch_cost += group_input_cost + group_output_cost
                logger.info(f"Total group cost: {group_input_cost+group_output_cost}")
        

        processed_concepts = [concept.replace("```json", "").replace("```", "").replace("\n```", "").replace("\n```json", "") for concept in batch_concepts]
        processed_concepts = [json.loads(concept) for concept in processed_concepts]

        
        logger.info(f"Total Analysis cost: ${batch_cost}")
        return processed_concepts
        
                


            
        

        
                                                