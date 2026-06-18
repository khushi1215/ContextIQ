from backend.rag.generator import AnswerGenerator

context = """
AWS may modify this Agreement at any time.

The modified terms become effective upon posting.

If you continue using AWS after the effective date,
you agree to the modified terms.
"""

query = "Who is the CEO of Microsoft?"

generator = AnswerGenerator()

answer = generator.generate(
    query,
    context,
)

print("\nANSWER\n")

print(answer)