# yes24/groq_bot.py
import os
import re
from groq import Groq
from dotenv import load_dotenv

# groq_bot.py 동일 경로의 .env 우선 로드 후 기본 load_dotenv 실행
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
load_dotenv()



def get_groq_api_key(user_input_key=None):
    """
    Retrieves Groq API Key from environment (.env) or user UI input.
    """
    env_key = os.getenv("GROQ_API_KEY", "").strip()
    if env_key:
        return env_key
    if user_input_key and user_input_key.strip():
        return user_input_key.strip()
    return None


SYSTEM_PROMPT = """친절한 도서 검색 도우미입니다.

당신은 YES24 IT/모바일 분야 베스트셀러 도서 데이터를 바탕으로 사용자 질문에 친절하고 명확하게 답변하는 AI 도서 상담원입니다.

[엄격한 답변 규칙]
1. 반드시 아래에 제공되는 [검색된 YES24 베스트셀러 도서 목록]에 실제 존재하는 도서 정보만을 기반으로 답변해야 합니다.
2. 질문자가 요청하는 조건, 특정 기술, 저자, 또는 주제에 부합하는 도서가 [검색된 YES24 베스트셀러 도서 목록]에 존재하지 않거나 관련성이 매우 낮다면, 절대 외부 도서를 지어내거나 추측해서 추천하지 말고 "죄송합니다. 요청하신 조건이나 주제에 해당하는 도서가 YES24 베스트셀러 목록에 없습니다."라고 분명히 답변해 주세요.
3. 조건에 맞는 도서가 있는 경우:
   - "친절한 도서 검색 도우미입니다"라는 인사를 첫 문장에 전달하며 답변을 시작하세요.
   - 도서의 기본 정보(도서명, 저자, 출판사, 판매가, 평점 등)를 명확하게 제시하세요.
   - **해당 도서를 추천하는 구체적인 이유(추천 이유)와 핵심 내용**을 상세히 설명해 주세요.
"""


def generate_rag_answer(user_query, chat_history, retrieved_books, api_key, model_name="llama-3.3-70b-versatile", temperature=0.2, top_p=1.0):
    """
    Generates RAG chatbot response using Groq API and ChromaDB retrieved context.
    """
    if not api_key:
        return "❌ Groq API Key가 설정되지 않았습니다. .env 파일에 GROQ_API_KEY를 설정하거나 UI에서 API Key를 입력해 주세요."

    client = Groq(api_key=api_key)

    # Format retrieved books context
    context_str = ""
    if retrieved_books:
        context_str += "[검색된 YES24 베스트셀러 도서 목록]\n"
        for idx, book in enumerate(retrieved_books, 1):
            name = book.get('goods_name', '')
            author = book.get('author', '')
            publisher = book.get('publisher', '')
            price_val = book.get('price_sale', 0)
            try:
                if isinstance(price_val, str):
                    cleaned_price = re.sub(r'[^\d.]', '', price_val)
                    price = float(cleaned_price) if cleaned_price else 0.0
                else:
                    price = float(price_val) if price_val is not None else 0.0
            except Exception:
                price = 0.0
            rating = book.get('rating', 0)
            sim = book.get('similarity_pct', 0)
            bm25_rank = book.get('bm25_rank', '-')
            rrf_score = book.get('rrf_score', 0)
            doc = book.get('document', '')

            context_str += f"{idx}. 도서명: {name} | 저자: {author} | 출판사: {publisher} | 판매가: {price:,.0f}원 | 평점: {rating}점 (유사도: {sim}%, 키워드순위: {bm25_rank}, RRF점수: {rrf_score})\n"
            context_str += f"   - 상세설명: {doc}\n\n"
    else:
        context_str = "[검색된 YES24 베스트셀러 도서 목록]\n(검색된 관련 도서 없음)\n"


    # Construct API message payload
    api_messages = [
        {"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context_str}
    ]

    # Append recent chat history (up to last 6 turns)
    for msg in chat_history[-6:]:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Append current user query if not present
    if not chat_history or chat_history[-1]["content"] != user_query:
        api_messages.append({"role": "user", "content": user_query})

    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=api_messages,
            temperature=float(temperature),
            top_p=float(top_p),
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Groq API 호출 중 오류가 발생했습니다: {str(e)}"


from ragas_evaluator import evaluate_rag_response


def generate_rag_answer_with_eval(user_query, chat_history, retrieved_books, api_key, model_name="llama-3.3-70b-versatile", temperature=0.2, top_p=1.0, ground_truth=None, do_eval=True):
    """
    Generates RAG answer and evaluates quality metrics using RAGAS evaluator.
    """
    answer = generate_rag_answer(
        user_query=user_query,
        chat_history=chat_history,
        retrieved_books=retrieved_books,
        api_key=api_key,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p
    )
    eval_res = None
    if do_eval and not answer.startswith("❌"):
        eval_res = evaluate_rag_response(
            question=user_query,
            retrieved_books=retrieved_books,
            response=answer,
            ground_truth=ground_truth,
            api_key=api_key,
            model_name=model_name,
            temperature=temperature,
            top_p=top_p
        )
    return answer, eval_res

