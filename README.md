<h2 align="center">Тестовое</h2>


## Что сделал

### 1.
    1) Реализовал модели
    2) Зайдя на страницу если пользователь зарегистрирован ему вывидутся его продукты.
    3) Нажав на продукт вывидутся уроки прикрепленные к продуктам.
    4) Нажав на урок выведится его видео.
    5) Посмотрев видео больше 10 секунд, в модели обновится запись даты просмотра
    6) Когда видео просмотрено больше 80%, в модели обновится is_viewed=True


### 2.1 api/v1/lesson-views/

 
```json
[
{
    "product": {
        "name": "Курсы шитья",
        "lessons": [
            {
                "name": "Урок 2",
                "duration_seconds": 604,
                "lesson": [
                    {
                        "is_viewed": false,
                        "watched_at": "2023-09-24T01:32:20.106047Z",
                        "current_position_sec": 262
                    }
                ]
            },
            {
                "name": "Урок 3",
                "duration_seconds": 450,
                "lesson": []
            },
            {
                "name": "Урок шитья",
                "duration_seconds": 442,
                "lesson": []
            }
        ]
    }
},
{
    "product": {
        "name": "Курс по шахматам",
        "lessons": [
            {
                "name": "Урок 2",
                "duration_seconds": 604,
                "lesson": [
                    {
                        "is_viewed": false,
                        "watched_at": "2023-09-24T01:32:20.106047Z",
                        "current_position_sec": 262
                    }
                ]
            },
            {
                "name": "Урок 4",
                "duration_seconds": 333,
                "lesson": []
            }
        ]
    }
}
]
```


### 2.2 api/v1/product/\<int:pk>

```json
{
    "name": "Курсы шитья",
    "lessons": [
        {
            "name": "Урок 2",
            "duration_seconds": 604,
            "lesson": [
                {
                    "is_viewed": false,
                    "watched_at": "2023-09-24T01:32:20.106047Z",
                    "current_position_sec": 262
                }
            ]
        },
        {
            "name": "Урок 3",
            "duration_seconds": 450,
            "lesson": []
        },
        {
            "name": "Урок шитья",
            "duration_seconds": 442,
            "lesson": []
        }
    ]
}
```

### 2.3 api/v1/product-stats/

```json
[
    {
        "id": 2,
        "name": "Курс Джанго",
        "viewed_lessons_count": 6,
        "total_viewing_time": 1362,
        "total_users_product": 3,
        "acquisition_percentage": 100.0
    },
    {
        "id": 3,
        "name": "Курс Джфнго 2",
        "viewed_lessons_count": 4,
        "total_viewing_time": 908,
        "total_users_product": 2,
        "acquisition_percentage": 66.66666666666666
    },
    {
        "id": 4,
        "name": "Курсы шитья",
        "viewed_lessons_count": 2,
        "total_viewing_time": 524,
        "total_users_product": 2,
        "acquisition_percentage": 66.66666666666666
    },
    {
        "id": 5,
        "name": "Курс по шахматам",
        "viewed_lessons_count": 2,
        "total_viewing_time": 524,
        "total_users_product": 2,
        "acquisition_percentage": 66.66666666666666
    }
]
```


**requirements:**
- Python >= 3.10
- Django == 4.2.5
- djangorestframework == 3.14.0



