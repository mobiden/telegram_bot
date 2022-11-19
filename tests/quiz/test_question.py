from typing import List

from asyncpg import (
    NotNullViolationError,
    ForeignKeyViolationError,
    UniqueViolationError,
)

from app.old_quiz.models import Question, Answer, Theme, QuestionModel, AnswerModel
from app.store import Store
from tests.quiz import question2dict
from tests.utils import ok_response
import pytest
from tests.utils import check_empty_table_exists


class TestQuestionsStore:
    async def test_table_exists(self, cli):
        await check_empty_table_exists(cli, "questions")
        await check_empty_table_exists(cli, "answers")

    async def test_create_question(
        self, cli, store: Store, theme_1: Theme, answers: List[Answer]
    ):
        question_title = "title"
        question = await store.quizzes.create_question(
            question_title, theme_1.id, answers
        )
        assert type(question) is Question

        questions = await QuestionModel.query.gino.all()
        assert len(questions) == 1
        assert question.title == question_title and question.id == 1

        answers_models = await AnswerModel.query.gino.all()
        assert len(answers_models) == len(answers)

    async def test_create_question_no_theme(
        self, cli, store: Store, answers: List[Answer]
    ):
        question_title = "title"
        with pytest.raises(ForeignKeyViolationError):
            await store.quizzes.create_question(question_title, 1, answers)

    async def test_create_question_none_theme_id(
        self, cli, store: Store, answers: List[Answer]
    ):
        question_title = "title"
        with pytest.raises(NotNullViolationError):
            await store.quizzes.create_question(question_title, None, answers)

    async def test_create_question_unique_title_constraint(
        self, cli, store: Store, question_1: Question, answers: List[Answer]
    ):
        with pytest.raises(UniqueViolationError):
            await store.quizzes.create_question(
                question_1.title, question_1.theme_id, answers
            )

    async def test_get_question_by_title(self, cli, store: Store, question_1: Question):
        assert question_1 == await store.quizzes.get_question_by_title(question_1.title)

    async def test_list_questions(
        self, cli, store: Store, question_1: Question, question_2: Question
    ):
        questions = await store.quizzes.list_questions()
        assert questions == [question_1, question_2]

    async def test_check_cascade_delete(self, store: Store, question_1: Question):
        await QuestionModel.delete.where(
            QuestionModel.id == question_1.id
        ).gino.status()
        objs = await AnswerModel.query.gino.all()

        assert len(objs) == 0


class TestQuestionAddView:
    async def test_success(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data=question2dict(
                Question(
                    id=data["data"]["id"],
                    title="How many legs does an octopus have?",
                    theme_id=1,
                    answers=[
                        Answer(title="2", is_correct=False),
                        Answer(title="8", is_correct=True),
                    ],
                )
            )
        )

    async def test_unauthorized(self, cli):
        resp = await cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": 1,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_theme_not_found(self, authed_cli):
        resp = await authed_cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": 1,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 404

    async def test_all_answers_are_correct(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": True,
                    },
                    {
                        "title": "8",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 400

    async def test_all_answers_are_incorrect(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": False,
                    },
                    {
                        "title": "8",
                        "is_correct": False,
                    },
                ],
            },
        )
        assert resp.status == 400

    async def test_only_one_answer(self, authed_cli, theme_1):
        resp = await authed_cli.post(
            "/store_flora.add_question",
            json={
                "title": "How many legs does an octopus have?",
                "theme_id": theme_1.id,
                "answers": [
                    {
                        "title": "2",
                        "is_correct": True,
                    },
                ],
            },
        )
        assert resp.status == 400
        data = await resp.json()
        assert data["status"] == "bad_request"


class TestQuestionListView:
    async def test_unauthorized(self, cli):
        resp = await cli.get("/store_flora.list_questions")
        assert resp.status == 401
        data = await resp.json()
        assert data["status"] == "unauthorized"

    async def test_empty(self, authed_cli):
        resp = await authed_cli.get("/store_flora.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"questions": []})

    async def test_one_question(self, authed_cli, question_1):
        resp = await authed_cli.get("/store_flora.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(data={"questions": [question2dict(question_1)]})

    async def test_several_questions(self, authed_cli, question_1, question_2):
        resp = await authed_cli.get("/store_flora.list_questions")
        assert resp.status == 200
        data = await resp.json()
        assert data == ok_response(
            data={"questions": [question2dict(question_1), question2dict(question_2)]}
        )
