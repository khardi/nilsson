import abc

import sqlite3
import redis


class Idea:
    def __init__(self):
        self.idea_id = None
        self.title = None
        self.description = None
        self.rating = None
        self.votes = None
        self.email = None

    def add_rating(self, rating: float):
        self.rating += float(rating)

    def __str__(self):
        return 'Idea(idea_id={}, title={}, rating={})'.format(self.idea_id, self.title, self.rating)


class IdeaRepository(abc.ABC):

    @abc.abstractmethod
    def find_by_id(self, idea_id: str):
        pass

    @abc.abstractmethod
    def update(self, idea: Idea):
        pass


class Sqlite3IdeaRepository(IdeaRepository):

    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def find_by_id(self, idea_id: str):
        # finding the idea in the database
        sql = 'SELECT * from Ideas where IdeaId = ?'
        row = self.cursor.execute(sql, idea_id).fetchone()
        if not row:
            raise ValueError('Idea does not exist')

        # Building the Idea from database
        idea_id, title, description, rating, votes, email = row
        idea = Idea()
        idea.idea_id = idea_id
        idea.title = title
        idea.description = description
        idea.rating = rating
        idea.votes = votes
        idea.email = email

        return idea

    def update(self, idea: Idea):
        update_statement = "UPDATE Ideas SET Rating='{}' WHERE IdeaId='{}'"
        self.cursor.execute(update_statement.format(idea.rating, idea.idea_id))
        self.connection.commit()


class RedisIdeaRepository(IdeaRepository):

    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def find_by_id(self, idea_id: str):
        title = self.client.hmget(idea_id, 'title')[0].decode()
        description = self.client.hmget(idea_id, 'description')[0].decode()
        rating = float(self.client.hmget(idea_id, 'rating')[0])
        votes = float(self.client.hmget(idea_id, 'votes')[0])
        email = self.client.hmget(idea_id, 'email')[0].decode()

        idea = Idea()
        idea.idea_id = idea_id
        idea.title = title
        idea.description = description
        idea.rating = rating
        idea.votes = votes
        idea.email = email

        return idea

    def update(self, idea: Idea):
        idea_id = idea.idea_id

        idea_dict = dict(
            idea_id=idea.idea_id,
            title=idea.title,
            description=idea.description,
            rating=idea.rating,
            votes=idea.votes,
            email=idea.email
        )

        self.client.hmset(idea_id, idea_dict)


class IdeaController:

    def __init__(self, request: dict):
        self.request = request

    def rate_action(self):
        idea_id = self.request.get('id')
        new_rating = self.request.get('rating')

        # idea_repository = Sqlite3IdeaRepository('../db.sqlite3')
        idea_repository = RedisIdeaRepository()

        # find idea
        idea = idea_repository.find_by_id(idea_id)
        if not idea:
            raise ValueError('Idea does not exist')

        # add user rating
        idea.add_rating(new_rating)

        # save rating to repository
        idea_repository.update(idea)

        return idea


if __name__ == '__main__':
    request = {
        'id': '1',
        'rating': 4
    }

    controller = IdeaController(request)
    result = controller.rate_action()

    print(result)
