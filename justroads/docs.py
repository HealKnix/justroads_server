from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)


class MarkDocumentation:
    def __new__(cls):
        tag = 'Метка'
        return {
            'list': extend_schema(
                tags=[tag],
                description="Получить список всех меток"
            ),
            'retrieve': extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name='id',
                        description='Идентификатор метки',
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретную метку по ID"
            ),
            'create': extend_schema(
                tags=[tag],
                description="Создать новую метку"
            ),
        }


class DefectStatusDocumentation:
    def __new__(cls):
        tag = 'Статус дефекта'
        return {
            'list': extend_schema(
                tags=[tag],
                description="Получить список всех статусов дефектов"
            ),
            'retrieve': extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name='id',
                        description='Идентификатор статуса дефекта',
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный статус дефекта по ID"
            ),
            'create': extend_schema(
                tags=[tag],
                description="Создать новый статус дефекта"
            ),
        }


class DefectDocumentation:
    def __new__(cls):
        tag = 'Дефект'
        return {
            'list': extend_schema(
                tags=[tag],
                description="Получить список всех дефектов"
            ),
            'retrieve': extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name='id',
                        description='Идентификатор дефекта',
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретный дефект по ID"
            ),
            'create': extend_schema(
                tags=[tag],
                description="Создать новый дефект"
            ),
        }


class MarkAnnotationDocumentation:
    def __new__(cls):
        tag = 'Аннотация метки'
        return {
            'list': extend_schema(
                tags=[tag],
                description="Получить список всех аннотаций метки"
            ),
            'retrieve': extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name='id',
                        description='Идентификатор аннотации метки',
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Получить конкретную аннотацию метки по ID"
            ),
            'create': extend_schema(
                tags=[tag],
                description="Создать новую аннотацию метки"
            ),
            'partial_update': extend_schema(
                tags=[tag],
                parameters=[
                    OpenApiParameter(
                        name='id',
                        description='Идентификатор аннотации метки',
                        required=True,
                        type=int,
                        location=OpenApiParameter.PATH,
                    )
                ],
                description="Частично обновить существующую аннотацию метки"
            ),
        }
