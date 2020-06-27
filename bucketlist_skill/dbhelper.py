from flask_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_app_id = db.Column(db.Integer, unique=False, nullable=False)

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


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<Category {} {}>".format(self.id, self.name)

    @staticmethod
    def add_new_category(name):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def get_category(category_id):
        category = db.session.query(Category).filter_by(id=category_id).first()
        return category

    @staticmethod
    def delete_category(category_id):
        category = db.session.query(Category).filter_by(id=category_id).first()
        db.session.delete(category)
        db.session.commit()


class StandardDesire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<StandardDesire {} {} {}>".format(self.id, self.category_id, self.text)

    @staticmethod
    def add_new_standard_desire(text, category_id):
        standard_desire = StandardDesire(text=text, category_id=category_id)
        db.session.add(standard_desire)
        db.session.commit()
        return standard_desire

    @staticmethod
    def get_standard_desire(standard_desire_id):
        standard_desire = db.session.query(StandardDesire).filter_by(id=standard_desire_id).first()
        return standard_desire

    @staticmethod
    def delete_standard_desire(standard_desire_id):
        standard_desire = db.session.query(StandardDesire).filter_by(id=standard_desire_id).first()
        db.session.delete(standard_desire)
        db.session.commit()


class UsersDesire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    text = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return "<UsersDesire {} {} {} {}>".format(self.id, self.category_id, self.user_id, self.text)

    @staticmethod
    def add_new_users_desire(text, category_id):
        users_desire = UsersDesire(text=text, category_id=category_id)
        db.session.add(users_desire)
        db.session.commit()
        return users_desire

    @staticmethod
    def get_users_desire(users_desire_id):
        users_desire = db.session.query(UsersDesire).filter_by(id=users_desire_id).first()
        return users_desire

    @staticmethod
    def delete_users_desire(users_desire_id):
        users_desire = db.session.query(UsersDesire).filter_by(id=users_desire_id).first()
        db.session.delete(users_desire)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
