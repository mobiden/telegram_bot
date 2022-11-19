from typing import List

import pytest

from app.old_quiz.models import Theme, Question, Answer


@pytest.fixture
def answers(store) -> List[Answer]:
    return [
        Answer(title="1", is_correct=True),
        Answer(title="2", is_correct=False),
        Answer(title="3", is_correct=False),
        Answer(title="4", is_correct=False),
    ]


@pytest.fixture
async def theme_1(store) -> Theme:
    theme = await store.quizzes.create_theme(title="web-development")
    yield theme


@pytest.fixture
async def theme_2(store) -> Theme:
    theme = await store.quizzes.create_theme(title="backend")
    yield theme


@pytest.fixture
async def question_1(store, theme_1) -> Question:
    question = await store.quizzes.create_question(
        title="how are you?",
        theme_id=theme_1.id,
        answers=[
            Answer(
                title="well",
                is_correct=True,
            ),
            Answer(
                title="bad",
                is_correct=False,
            ),
        ],
    )
    yield question


@pytest.fixture
async def question_2(store, theme_1) -> Question:
    question = await store.quizzes.create_question(
        title="are you doing fine?",
        theme_id=theme_1.id,
        answers=[
            Answer(
                title="yep",
                is_correct=True,
            ),
            Answer(
                title="nop",
                is_correct=False,
            ),
        ],
    )
    yield question
