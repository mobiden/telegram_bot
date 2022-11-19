from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import request_schema, response_schema, querystring_schema


from app.garden.schemes import (
    FloraAddSchema, FloraTypeAddSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class FloraTypeAddView(AuthRequiredMixin, View):
    @request_schema(FloraTypeAddSchema)
    @response_schema(FloraTypeAddSchema)
    async def post(self):

        type = self.data["type"]
        existing_type = await self.store.store_flora.get_flora_type(type)
        if existing_type:
            raise HTTPConflict
        new_type = await self.store.store_flora.create_flora_type(type=type)

        return json_response(data=FloraTypeAddSchema().dump(new_type))


class FloraNameAddView(AuthRequiredMixin, View):
    @request_schema(FloraAddSchema)
    @response_schema(FloraAddSchema)
    async def post(self):

        name = self.data["name"]
        type = self.data["type"]
        planting_time = self.data["planting_time"]
        harvest_time = self.data["harvest_time"]
        existing_name = await self.store.store_flora.get_flora_by_name(name)
        if existing_name:
            raise HTTPConflict
        new_flora = await self.store.store_flora.create_flora(
                name = name,
                type = type,
                planting_time = planting_time,
                harvest_time = harvest_time,
                    )
        return json_response(data=FloraAddSchema().dump(new_flora))



class Flora_Operation_AddView(AuthRequiredMixin, View):
    pass



#
"""
class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        return json_response(data=ThemeListSchema().dump({"themes": themes}))


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        existing_question = await self.store.quizzes.get_question_by_title(title)
        if existing_question:
            raise HTTPConflict

        theme_id = self.data["theme_id"]
        theme = await self.store.quizzes.get_theme_by_id(id_=theme_id)
        if not theme:
            raise HTTPNotFound

        if len(self.data["answers"]) < 2:
            raise HTTPBadRequest

        parsed_answers = []
        correct = []
        for answer in self.data["answers"]:
            answer = Answer(title=answer["title"], is_correct=answer["is_correct"])
            if answer.is_correct and True in correct:
                raise HTTPBadRequest
            correct.append(answer.is_correct)
            parsed_answers.append(answer)

        if not any(correct):
            raise HTTPBadRequest

        question = await self.store.quizzes.create_question(
            title=title,
            theme_id=theme_id,
            answers=parsed_answers,
        )
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions(
            theme_id=self.data.get("theme_id")
        )
        return json_response(
            data=ListQuestionSchema().dump(
                {
                    "questions": questions,
                }
            )     )
"""