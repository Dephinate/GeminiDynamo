import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,HttpUrl
from vertexai.generative_models import GenerativeModel
from services.genai import YoutubeProcessor, GeminiProcessor

# class to validate HttpUrls requests coming from frontend
class VideoAnalysisRequest(BaseModel):
    youtube_link: HttpUrl

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    # allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["Content-Type", "Authorization"],
)
@app.get("/")
def health():
    return{"status": "ok"}

genai_processor = GeminiProcessor(
    model_name="gemini-pro",
    project="rich-agency-421922"
)


@app.post("/analyze_video")
def analyze_video(request: VideoAnalysisRequest):
    from langchain_community.document_loaders import YoutubeLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    link = str(request.youtube_link)
    # print("Request",link, type(link))


    youtubeProcessor = YoutubeProcessor(genai_processor = genai_processor)
    docs = youtubeProcessor.retrieve_youtube_documents(video_url=link,verbose=True)
    print("num_of_docs: ",len(docs))

    key_concepts = youtubeProcessor.find_key_concepts(documents=docs[:20], sample_size=5, verbose=True)

    # summary = geminiProcessor.generate_document_summary(documents=docs[0:5], verbose=True)

    return{
        "key_concepts": key_concepts
    }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)