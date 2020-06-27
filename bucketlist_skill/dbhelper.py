from flask_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_app_id = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<User {} {}>".format(self.id, self.user_app_id)

    @staticmethod
    def add_new_user(user_id):
        user = User(user_app_id=user_id)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user(user_id):
        user = db.session.query(User).filter_by(user_app_id=user_id).first()
        return user

    @staticmethod
    def delete_user(user_id):
        user = db.session.query(User).filter_by(user_app_id=user_id).first()
        db.session.delete(user)
        db.session.commit()


class Desire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String, unique=False, nullable=False)
    text = db.Column(db.String, unique=False, nullable=False)
    published = db.Column(db.Bool, unique=False, nullable=False)
    owner_id = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return "<Desire {} {} {} {}>".format(self.id, self.tags, self.text, self.published)

    @staticmethod
    def add_new_standard_desire(text, category_id, tags):
        standard_desire = Desire(text=text, category_id=category_id, tags=tags)
        db.session.add(standard_desire)
        db.session.commit()
        return standard_desire

    @staticmethod
    def get_standard_desire(desire_id):
        standard_desire = db.session.query(Desire).filter_by(id=desire_id).first()
        return standard_desire

    @staticmethod
    def delete_standard_desire(desire_id):
        standard_desire = db.session.query(Desire).filter_by(id=desire_id).first()
        db.session.delete(standard_desire)
        db.session.commit()


class UsersDesire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=False, nullable=False)
    desire_id = db.Column(db.Integer, unique=False, nullable=False)
    completed = db.Column(db.Bool, unique=False, nullable=False)

    def __repr__(self):
        return "<UsersDesire {} {} {} {}>".format(self.id, self.user_id, self.desire_id, self.completed)

    @staticmethod
    def add_new_users_desire(user_id, desire_id, category_id):
        users_desire = UsersDesire(user_id=user_id, desire_i=desire_id, category_id=category_id)
        db.session.add(users_desire)
        db.session.commit()
        return users_desire

    @staticmethod
    def get_users_desire(desire_id):
        users_desire = db.session.query(UsersDesire).filter_by(desire_id=desire_id).first()
        return users_desire

    @staticmethod
    def delete_users_desire(desire_id):
        users_desire = db.session.query(UsersDesire).filter_by(desire_id=desire_id).first()
        db.session.delete(users_desire)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
