from model import BaseModel, engine


def init_db():
    import model.teacher
    import model.teacher_test
    import model.user
    import model.price
    BaseModel.metadata.create_all(engine)


def drop_db():
    import model.teacher
    import model.teacher_test
    import model.user
    import model.price
    BaseModel.metadata.drop_all(engine)


if __name__ == '__main__':
    init_db()
