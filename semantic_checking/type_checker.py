class TypeCheckerVisitor:
    def __init__(self, context, errors) -> None:
        self.context = context
        self.errors = errors