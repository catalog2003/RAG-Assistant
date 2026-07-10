import time
from fastapi import APIRouter, HTTPException
from New.Backend.api.models.schemas import AskRequest, AskResponse, Source
from New.Backend.services.retriever import Retriever
from New.Backend.services.llm import build_prompt, ask_hf_llm
from New.Backend.services.history import history_manager
from New.Backend.utils import remove_duplicates

router = APIRouter(prefix="/ask", tags=["Question Answering"])

retriever = None

def initialize_ask_router(ret):
    global retriever
    retriever = ret

@router.post("/", response_model=AskResponse)
async def ask_question(request:AskRequest):

    start_time = time.time()

    if not retriever:
        raise HTTPException(500, "Retriever not initialized")
    
    if not request.question.strip():
        raise HTTPException(400,"Question cannot be empty")
    
    contexts = retriever.retrieve(request.question)
    if not contexts:
        return AskResponse(
            answer= "I couldn't find any relevant information in the documents.",
            sources=[],
            processing_time = time.time() - start_time
        )
    
    contexts = remove_duplicates(contexts)

    prompt = build_prompt(request.question, contexts)

    answer = ask_hf_llm(prompt)

    sources = [
        Source(
            document=ctx["document"],
            page=ctx["page"],
            score=ctx.get("score")
        )
        for ctx in contexts[:3]
    ]

    history_manager.add_message(request.session_id, "user", request.question)

    history_manager.add_message(request.session_id, "assistant", answer)    

    processing_time = time.time() - start_time
    
    return AskResponse(
        answer=answer,
        sources=sources,
        processing_time=processing_time
    )

@router.post("/stream")
async def ask_question_stream(request:AskRequest):

    from fastapi.responses import StreamingResponse
    async def generate():
        contexts = retriever.retrieve(request.question)
        if contexts:
            contexts = remove_duplicates(contexts)
            prompt = build_prompt(request.question, contexts)
        

    return StreamingResponse(generate(), media_type="text/plain")
    

