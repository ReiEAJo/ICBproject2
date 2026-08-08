# yes24/test_ragas_evaluator.py
import unittest
from ragas_evaluator import calculate_context_precision, evaluate_rag_response


class TestRagasEvaluator(unittest.TestCase):
    def test_context_precision_basic(self):
        query = "파이썬 기초 입문 서적 추천"
        contexts = [
            "Do it! 점프 투 파이썬 - 파이썬 프로그래밍 입문서",
            "자바 스프링 파이프라인 구축"
        ]
        precision = calculate_context_precision(query, contexts)
        self.assertTrue(0.0 <= precision <= 1.0)
        self.assertTrue(precision > 0.0)

    def test_evaluate_rag_response_fallback(self):
        retrieved_books = [
            {"goods_name": "Do it! 점프 투 파이썬", "document": "파이썬 기초 프로그래밍 베스트셀러 도서"}
        ]
        res = evaluate_rag_response(
            question="파이썬 입문책 추천해줘",
            retrieved_books=retrieved_books,
            response="친절한 도서 검색 도우미입니다. Do it! 점프 투 파이썬을 추천합니다.",
            ground_truth="Do it! 점프 투 파이썬",
            api_key=None
        )
        self.assertIn("faithfulness", res)
        self.assertIn("answer_relevance", res)
        self.assertIn("context_precision", res)
        self.assertIn("context_recall", res)
        self.assertIn("ragas_score", res)
        self.assertTrue(0.0 <= res["ragas_score"] <= 100.0)


if __name__ == "__main__":
    unittest.main()
