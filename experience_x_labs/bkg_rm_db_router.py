class SecondDBRouter:
    """
    A router to control all database operations on models in the
    imagex application.
    """

    def db_for_read(self, model, **hints):
        """
        Point all operations on models in the imagex application to the 'second_db' database.
        """
        if model._meta.app_label == 'imagex':
            return 'second_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Point all operations on models in the imagex application to the 'second_db' database.
        """
        if model._meta.app_label == 'imagex':
            return 'second_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects in the imagex application.
        """
        if (
            obj1._meta.app_label == 'imagex'
            or
            obj2._meta.app_label == 'imagex'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the 'second_db' database only appears in the 'imagex'
        application.
        """
        if app_label == 'imagex':
            return db == 'second_db'
        return None
